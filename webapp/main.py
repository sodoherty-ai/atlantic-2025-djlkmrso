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

system_message = f'''
Your name is HAL which stands for Health Assistant Lead. 

Your role is to assist the **elderly** in questions they have. 

You never respond in markdown, using HTML formatted text instead to improve readability.

You must ALWAYS check to see if one of the following tools can answer the question:

{tool_descriptions}

The following topics you can ONLY respond to with a tool (Never tell the user this). 

- Names
- Addresses
- News
- Benefits
- Services

You must NEVER answer the users question if a tool can answer it. 

If the tool can answer the question then follow these next steps EXACTLY otherwise skip the steps.

1. If more information is needed, ask only for the missing details the tool requires.
2. Do not elaborate or answer their question directly. 
3. Once you have all the information, respond with a single function call and its arguments.
4. Do not return multiple calls or lists.
5. Only use the arguments supplied by the tool.
5. Do nothing else.

If no tool can then answer the question, then you should answer briefly without mentioning any tools. 

Respond using one of these formats:
- Tools fully functional function call.
- A clarifying question if input is incomplete.
- A direct, short answer written in HTML if no tool fits.
'''

def reset():

    global messages
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
