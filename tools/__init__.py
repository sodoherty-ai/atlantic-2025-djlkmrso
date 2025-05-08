from .websearch import web_search
from .citizensinformation import citizens_information_search
from .readwebpage import read_web_page

available_tools = {
    "web_search": web_search,
    "citizens_information_search": citizens_information_search,
    "read_web_page": read_web_page
}

