from crewai_tools import ScrapeWebsiteTool
from crewai.tools import tool

@tool("read_web_page")
def read_web_page(url: list|str) -> list:
    """
    Read a web page and return its content.

    Args:
        url(str|list): The URL of the web page or a list of URLs.

    Returns:
        List of strings containing the content of the urls.
    """

    headers = {
        'User-Agent': 'CrewAIBot/1.0'
    }

    if isinstance(url, str):
        urls = [url]
    else:
        urls = url

    results = []
    for u in urls:
        scraper = ScrapeWebsiteTool(
            website_url=u,
            headers=headers
        )
        content = scraper.run()
        results.append(content)

    return results
