from dotenv import load_dotenv
import os
from ollama import Client
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from textwrap import dedent


def reset():
    global messages
    messages = [
        {'role': 'system',
         'content': dedent('''
             You are a helpful assistant. Answer questions briefly and naturally in a conversational way, 
             responding one message at a time. Respond using HTML, for example CODE, PRE, and BR. 
             ''').strip()
         }
    ]


app = FastAPI()
templates = Jinja2Templates(directory='templates')

load_dotenv()  # take environment variables from .env.

model_id = os.getenv('MODEL')
print(model_id)

llm = Client()
messages = []
reset()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    reset()
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/message')
async def message(request: Request):
    global messages
    data = await request.json()
    user_input = data.get('message', '')
    messages.append({'role': 'user', 'content': user_input})

    def stream_response():
        collected = ''
        for chunk in llm.chat(model=model_id, messages=messages, stream=True):
            content = chunk.get('message', {}).get('content', '')
            if content:
                collected += content
        yield f'data: {collected}\n\n'

        messages.append({'role': 'assistant', 'content': collected})

    return StreamingResponse(stream_response(), media_type='text/event-stream')


@app.get('/reset_conversation')
async def reset_conversation():
    reset()
    pass
