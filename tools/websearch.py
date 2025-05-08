from duckduckgo_search.exceptions import DuckDuckGoSearchException
from langchain_community.tools import DuckDuckGoSearchResults
from crewai.tools import tool

@tool("web_search")
def web_search(query: str, max_results: int = 10) -> list:
    """
    Search the web for information on a given topic.

    Args:
        query (str): The search query.
        max_results (int, optional): Maximum number of search results to return (maximum is 10).

    Returns:
        An array of dictionaries. If the array is empty, then no results were found, or an error occurred.
    """

    print('Using Tool: DuckDuckGo Search')

    if max_results > 10: max_results = 10
    try:
        response = DuckDuckGoSearchResults(
            max_results=max_results,
            output_format="list"
        ).run(query)
    except DuckDuckGoSearchException as e: # To handle rate limits.
        response = []

    return response
