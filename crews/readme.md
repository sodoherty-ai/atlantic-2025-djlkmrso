# Crews

## Purpose
This document details how crew files are structured. Each `yaml` file contains all the requirements 
you need to run a crew. 

## Recommended Reading 
- [Building effective agents](https://docs.crewai.com/guides/agents/crafting-effective-agents)

## YAML file components

### Debugging
If `verbose` is set to `true` then you can see how the crew is thinking while working. But it can get
very noisy.

### Crew
- [Reference Attributes](https://docs.crewai.com/concepts/crews#crew-attributes)

Here you setup your crew and what they need to do. You have to specify `agents`, `tasks` and
`process` to take.

### Agents
- [Reference Attributes](https://docs.crewai.com/concepts/agents#agent-attributes)

Think of agents as people you need to employ to work on your crew. The minimum settings are:

- `name`
- `role`
- `goal`
- `tools` (Optional)

### Tasks
- [Reference Attributes](https://docs.crewai.com/concepts/tasks#task-attributes)

The tasks are what your agents need to complete. The minimum settings are:

- `name`
- `description`
- `expected_output`
- `agent`
- `output_file` (Optional)

Apart from the final output, the `output_file` can also be used to debug tasks
as you go. 

**Please try** to keep your outputs in the `crew_output` folder.

**Important!:** The `agent` name must use the `role` value. (I need to figure out how to
fix this).

## Tools available

| Tool Identifier | Description                                                                                                                                                                        |
|----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `web_search` | Will use DuckDuckGo to do a search. Returns:<br><li>Title <br><li>URL<br><li>Snippet description.                                                                                  |
| `read_web_page` | Will read a web page and return the text content.                                                                                                                                  
| `citizens_information_search` | Will search Citizens Information and return the top 3 searchs (unless requested, max is 10).<br><br>The search results format:<br><li>Title<br/><li>Link<br/><li>Short description |

