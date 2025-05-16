from dotenv import load_dotenv
from ollama import Client
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import json
from os import environ as env
from yaml import safe_load
from tools import available_tools
from crewai import Crew
from langfuse import Langfuse

load_dotenv()

# Lang fuse code
user_id = env['LANGFUSE_ID']
langfuse = Langfuse(
    public_key=env['LANGFUSE_PUBLIC_KEY'],
    secret_key=env['LANGFUSE_SECRET_KEY'],
    host='https://cloud.langfuse.com'
)
trace = None

model_id = 'granite3.3'

with open('tools.json') as file:
    tools = json.load(file)

tool_descriptions = ''
for tool in tools:
    tool_descriptions += (
        f"If the user asks about:\n"
        f"- {tool['description']}\n"
        f"Even if phrased indirectly (e.g., 'what can I get?', 'is there help for my parents?', 'is there support for me?')\n"
        f"Then respond ONLY with:\n"
        f"{tool['name']}(topic: str)\n\n"
    )

def reset():
    global messages, tool_descriptions, tools, trace, silent, span, user_id

    with open('system_prompt.txt') as file:
        system_message = file.read()

    system_message = system_message.format(tool_descriptions=tool_descriptions)

    if trace:
        span = trace.span(name='conversation_reset', metadata={
            'messages': messages
        })
        span.end()

    trace = langfuse.trace(
        name='HAL Session started',
        user_id=user_id
    )
    span = trace.span(
        name='system_prompt',
        input=system_message,
        metadata = {
            'tools': tools,
            'tools_descriptions': tool_descriptions
        }
    )

    messages = [
        { 'role': 'system', 'content': system_message},
        { 'role': 'user', 'content': 'Hi, I am over 65 and live in Ireland. All my questions will relate to that'},
        { 'role': 'assistant', 'content': 'Ok I will remember this and check my tools first before responding.' }
    ]


app = FastAPI()
templates = Jinja2Templates(directory='templates')

llm = Client()
messages = []

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    reset()
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/message')
async def message(request: Request):
    global messages, tools, span

    data = await request.json()
    user_input = data.get('message', '')
    silent = data.get('silent', False)

    messages.append({'role': 'user', 'content': user_input})

    def stream_response():
        global span
        try:
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
                    if not tool_called:
                        yield f'data: {content}\n\n'
        finally:
            span = trace.span(
                name='ollama-called',
                input=user_input,
                output=collected,
                metadata={
                    'silent': silent,
                    'tool_called': tool_called,
                    'messages': messages
                }
            )

            if tool_called:
                yield 'data: <running-crew>\n\n'
                yield f'data: {run_tool(tool_called, user_input)}\n\n'
                yield 'data: <crew-finished>\n\n'
            if not silent:
                messages.append({'role': 'assistant', 'content': collected})
            else:
                messages.pop()

    return StreamingResponse(stream_response(), media_type='text/event-stream')


def run_tool(name, query):
    return run_crew(name, query)


@app.get('/reset_conversation')
async def reset_conversation():
    reset()

def run_crew(crew_name: str, question: str) -> str:
    try:
        global span

        with open(f'crews/{crew_name}.yaml') as file:
            settings = safe_load(file)

        agents_data = settings.get('agents', None)
        tasks_data = settings.get('tasks', None)
        crew_settings = settings.get('crew', None)

        new_question = f'For the over 65 {question}'
        input_settings = { 'topic': new_question }

        verbose_settings = settings.get('verbose', False)

        if agents_data is None or tasks_data is None or crew_settings is None:
            error_message = '<b>Error: Invalid crew settings</b>'
            span = trace.span(
                name='crew-invalid',
                input=crew_name,
                output=error_message,
            )
            return error_message

        span = trace.span(
            name='crew-called',
            input=crew_name,
            output=new_question,
            metadata={
                'agents': agents_data,
                'tasks': tasks_data,
                'crew': crew_settings,
                'question': question,
                'shaped': new_question,
                'verbose': verbose_settings
            }
        )

        for agent in agents_data:
            span = trace.span(
                name=f"Agent: {agent['name']}",
                input=agent['role'],
                output=agent['goal'],
                metadata={
                    'backstory': agent['backstory'],
                    'tools': agent.get('tools', [])
                }
            )

        for task in tasks_data:
            span = trace.span(
                name=f"Task: {task['name']}",
                input=task['description'],
                output=task['expected_output'],
                metadata=task
            )

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

        result = crew.kickoff(inputs=input_settings)

        parent_span = trace.span(
            name='crew-completed',
            input=crew_name,
            output=str(result),
            metadata=result.model_dump()
        )

        return f'Here is what the crew found on what you asked.<br><br>{str(result.raw)}'
    except Exception as e:
        span = trace.span(
            name='crew-failed',
            input=crew_name,
            output=str(e),
        )
        return f'The crew sent to do the job failed. {type(e).__name__}: {str(e)}'
