from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
import os

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")


class NewsTool:
    name = "News tool"
    description = """Use this tool when you have to answer queries regarding Pakistan's news.
                     Input to this tool will be a string query."""

    def __init__(self):
        self.search_method = SerpAPIWrapper()
        pass

    def search_function(self, query):
        return self.search_method.run(query)


tool_news = Tool.from_function(name=NewsTool().name,
                               description=NewsTool().description,
                               func=NewsTool().search_function,
                               return_direct=True
                               )