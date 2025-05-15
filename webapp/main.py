from dotenv import load_dotenv
from ollama import Client
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import json

load_dotenv()

model_id = 'granite3.3'

with open('tools.json') as file:
    tools = json.load(file)

tool_descriptions = "\n".join(
    f"- {tool['name']}: {tool['description']}" for tool in tools
)

def reset():
    with open('system_prompt.txt') as file:
        system_message = file.read()

    global messages, tool_descriptions
    messages = [{'role': 'system', 'content': system_message}]

app = FastAPI()
templates = Jinja2Templates(directory='templates')

llm = Client()
messages = []
reset()

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    reset()
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/message')
async def message(request: Request):
    global messages, tools
    data = await request.json()
    user_input = data.get('message', '')
    silent = data.get('silent', False)

    messages.append({'role': 'user', 'content': user_input})

    def stream_response():
        collected = ''
        tool_called = None

        for chunk in llm.chat(model=model_id, messages=messages, stream=True, tools=tools):
            content = chunk.get('message', {}).get('content', '')
            if content:
                collected += content
                for tool in tools:
                    if tool['name'].lower() in content.lower():
                        yield 'data: <tool-called>\n\n'
                        tool_called = tool['name']
                        break

                yield f'data: {content}\n\n'

        if tool_called:
            yield f'data: {run_tool(tool_called, user_input)}\n\n'
        if not silent:
            messages.append({'role': 'assistant', 'content': collected})
        else:
            messages.pop()

        print('-------')
        print(json.dumps(messages, indent=4))
        print('-------')

    return StreamingResponse(stream_response(), media_type='text/event-stream')

def run_tool(name, query):
    return f"<b>{name}: {query}</b> tool executed."

@app.get('/reset_conversation')
async def reset_conversation():
    reset()
