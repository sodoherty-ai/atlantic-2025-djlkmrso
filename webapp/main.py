from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

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
