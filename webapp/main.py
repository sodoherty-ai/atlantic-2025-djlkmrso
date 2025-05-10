from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import asyncio
from yaml import safe_load
from tools import available_tools
from crewai import Crew
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    df = pd.read_csv('data/over_65_by_county.csv')
    data = df.to_dict(orient='records')

    return templates.TemplateResponse('index.html', {"request": request, "data": data})

@app.get("/work", response_class=JSONResponse)
async def do_work():
    return {"message": "I worked"}

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