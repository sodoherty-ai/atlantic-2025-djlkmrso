from argparse import ArgumentParser
from yaml import safe_load
from crewai import Crew
from tools import available_tools
from dotenv import load_dotenv
from os import environ

# Langfuse
from base64 import b64encode
import openlit

parser = ArgumentParser()
parser.add_argument('crew_identifier', type=str, help='Name of crew to run. It must match the file in the crews folder')
parser.add_argument('--ask-for-inputs', action='store_true', help='Change inputs before running the crew.')

args = parser.parse_args()
load_dotenv()

if 'LITELLM_LOG' in environ:
    import litellm
    litellm._turn_on_debug()

if 'LANGFUSE_HOST' in environ:
    auth = b64encode(
        f"{environ['LANGFUSE_PUBLIC_KEY']}:{environ['LANGFUSE_SECRET_KEY']}".encode()
    ).decode()

    environ.update({
        'OTEL_EXPORTER_OTLP_ENDPOINT': environ['LANGFUSE_HOST'],
        'OTEL_EXPORTER_OTLP_HEADERS':  f'Authorization=Basic {auth}',
    })

    openlit.init(disable_batch=True)

crew_identifier = args.crew_identifier
with open(f'crews/{crew_identifier}.yaml') as file:
    settings = safe_load(file)

agents_data = settings.get('agents', None)
tasks_data = settings.get('tasks', None)
crew_settings = settings.get('crew', None)
inputs_settings = settings.get('inputs', None)
verbose_settings = settings.get('verbose', False)

if agents_data is None or tasks_data is None or crew_settings is None:
    print(f'Invalid or incomplete configuration in crews/{crew_identifier}.yaml')
    exit(1)

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

if args.ask_for_inputs:
    print('Before I kick off, I need to get some information to give to the crew.')
    print('Please enter the values, or just hit enter for the default.')
    print()

    for key, value in inputs_settings.items():
        new_value = input(f'{key} [{value}]> ')
        if new_value and new_value.strip() != '':
            inputs_settings[key] = new_value
    print()

print()
print()
print('Getting a crew together. 🚶‍♂️ 🚶‍♀️ 🚶 🚶 ')

crew.kickoff(inputs=inputs_settings)

print('[ CrewAI: Finished ]')
