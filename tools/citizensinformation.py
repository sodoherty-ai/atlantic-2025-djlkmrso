from crewai.tools import tool
import requests
from bs4 import BeautifulSoup

@tool("citizens_information_search")
def citizens_information_search(query: str, max_results: int = 3) -> list:
    """
    Searches the Citizens Information website (Ireland's public services and rights resource) for a given query
    and returns structured results with titles, URLs, and descriptions.

    Inputs:
    - query (str): What you want to search for.
    - max_results (int, optional): Maximum number of search results to return. Defaults to 10.

    Returns:
    - A list of search results, each with a title, link, and short description.
    """

    print('Using Tool: Search Citizens Information')

    no_results = []
    params = {'query': query}
    try:
        response = requests.get('https://www.citizensinformation.ie/en/search_wagtail/', params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results_div = soup.find("div", id="results")

        results = []
        for index, result in enumerate(results_div.find_all("div", class_="result")):
            entry = {}
            for child in result.find_all(["a", "div"], recursive=False):
                class_name = child.get("class")[0] if child.get("class") else None
                if class_name:
                    entry[class_name] = child.get_text(strip=True)
            results.append(entry)

            if index >= max_results:
                break

        return results

    except requests.exceptions.HTTPError as e:
        pass

    return no_results
