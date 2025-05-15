from dotenv import load_dotenv
from ollama import Client
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import json
import re
import ast

load_dotenv()

model_id = 'granite3.3'

with open('tools.json') as file:
    tools = json.load(file)

tool_descriptions = "\n".join(
    f"- {tool['name']}: {tool['description']}" for tool in tools
)

system_message = f'''Your name is HAL which stands for Health Assistant Lead. Your role is to assist the elderly in
questions they may have about themselves. You are a helpful assistant with access to special functions (tools). You 
never respond in markdown, using HTML formatted text instead (except where tool calling).

Before answering, always check if the user's question can be answered by one of these tools:

{tool_descriptions}

- If a tool can answer the question follow these steps EXACTLY:
  1. If more information is needed, ask only for the missing details.
  2. Respond with a single function call using the most relevant topic. Do not return multiple calls or lists.
  3. Do nothing else.

- If no tool matches, answer the question briefly without mentioning any tool. 

NEVER mention or suggest a tool unless you are directly calling it.

Respond using one of these formats:
- Tools function call. Example: 

    citizens_information(topic="disability allowance")

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
    messages.append({'role': 'user', 'content': user_input})

    def stream_response():
        collected = ''

        for chunk in llm.chat(model=model_id, messages=messages, stream=True, tools=tools):
            content = chunk.get('message', {}).get('content', '')
            if content:
                collected += content

        messages.append({'role': 'assistant', 'content': collected})

        # Detect tool call
        match = re.match(r'(\w+)\((.*?)\)', collected.strip())
        if match:
            tool_name, arg_str = match.groups()
            try:
                arg_dict = ast.literal_eval(f"dict({arg_str})")
                print(f"Tool call detected: {tool_name} with {arg_dict}")

                result = run_tool(tool_name, arg_dict)

                messages.append({
                    'role': 'tool',
                    'name': tool_name,
                    'content': result
                })

                # Only yield the tool response, not the function call
                yield f'data: {result}\n\n'
                return
            except Exception as e:
                print(f"Tool call parsing failed: {e}")

        # If no tool call, stream the full collected content
        yield f'data: {collected}\n\n'

        print('-------')
        print(json.dumps(messages, indent=4))
        print('-------')

    return StreamingResponse(stream_response(), media_type='text/event-stream')

def run_tool(name, args):
    if name == "citizens_information":
        topic = args.get("topic", "unknown")
        return f"<b>Citizens Info:</b> {topic}<br>This would be the actual answer."
    return f"<b>{name}:</b> tool executed with args {args}"

@app.get('/reset_conversation')
async def reset_conversation():
    reset()
