from langchain_community.tools import DuckDuckGoSearchResults
from crewai.tools import tool

@tool("web_search")
def web_search(query: str, max_results: int = 10) -> list:
    """
    Search the web for information on a given topic.

    Args:
        query (str): The search query.
        max_results (int, optional): Maximum number of search results to return. Defaults to 10.
    """

    print('Using Tool: DuckDuckGo Search')

    response = DuckDuckGoSearchResults(
        max_results=max_results,
        output_format="list"
    ).run(query)

    return response
