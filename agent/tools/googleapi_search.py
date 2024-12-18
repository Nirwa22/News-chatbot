from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
import os

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")


class GoogleSearchTool:
    name = "Google search tool"
    description = """Use this tool when you can not find relevant content related to Pakistan's history
                     in vector database. Input to this tool will be a string query."""

    def __init__(self, query):
        self.query = query
        pass

    def search_function(self):
        return SerpAPIWrapper().run(self.query)


google_search_tool = Tool.from_function(
    name=GoogleSearchTool.name,
    description=GoogleSearchTool.description,
    func=GoogleSearchTool.search_function,
    return_direct=True
)

