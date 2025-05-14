from crewai import Crew
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from flask import render_template
from ollama import Client
from pydantic import BaseModel
from tools import available_tools
from textwrap import dedent
from yaml import safe_load

import asyncio
import json
import pandas as pd

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

class Data(BaseModel):
    records: list

templates = Jinja2Templates(directory="templates")
model_id = 'granite3.3'
llm = Client()
messages = []
reset()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    df = pd.read_csv('data/over_65_by_county.csv')
    data = df.to_dict(orient='records')
    return templates.TemplateResponse('example_bootstrap.html', {"request": request, "data": data})

@app.get("/work", response_class=JSONResponse)
async def do_work():
    return {"message": "I worked"}

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    try:
        payload = json.loads(data)
        crew_name = payload["crew"]
        topic = payload["topic"]
        year = payload["year"]
    except Exception as e:
        await websocket.send_text(f"Error parsing input: {e}")
        await websocket.close()
        return

    await websocket.send_text(f'Running "{crew_name}" for topic "{topic}" ({year})...')
    await asyncio.sleep(0.1)

    inputs = { 'topic': topic, 'current_year': year}
    result = run_crew(crew_name, inputs)

    await websocket.send_text(result)
    await asyncio.sleep(0.1)
    await websocket.close()

@app.get('/reset_conversation')
async def reset_conversation():
    reset()
    pass

def run_crew(crew_name: str, inputs: dict | None = None) -> str:
    with open(f'crews/{crew_name}.yaml') as file:
        settings = safe_load(file)

    agents_data = settings.get('agents', None)
    tasks_data = settings.get('tasks', None)
    crew_settings = settings.get('crew', None)

    if inputs is None:
        inputs_settings = settings.get('inputs', None)
    else:
        inputs_settings = inputs

    verbose_settings = settings.get('verbose', False)

    if agents_data is None or tasks_data is None or crew_settings is None:
        return '<b>Error: Invalid crew settings</b>'

    for agent in agents_data:
        if 'tools' in agent:
            agent['tools'] = [available_tools[tool_name] for tool_name in agent['tools']]

    crew = Crew(
        config={
            'crew': crew_settings,
            'agents': agents_data,
            'tasks': tasks_data
        },
        verbose=verbose_settings
    )

    result = crew.kickoff(inputs=inputs_settings)
    return str(result)