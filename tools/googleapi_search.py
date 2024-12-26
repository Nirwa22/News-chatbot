from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import os

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)

class GoogleSearchTool:
    name = "Google search tool"
    description = """Use this tool when you can not find relevant content related to Pakistan's history
                     in vector database. For input queries outside the scope of pakistan's news and history
                     you must not use this tool at all. Input to this tool will be a string query. Output must
                     be a 5-6 line paragraph"""

    def __init__(self):
        self.search_method = SerpAPIWrapper()
        pass

    def search_function(self, query):
        return self.search_method.run(query)


google_search_tool = Tool.from_function(
    name=GoogleSearchTool().name,
    description=GoogleSearchTool().description,
    func=GoogleSearchTool().search_function,
    return_direct=True
)

# r = GoogleSearchTool().search_function("who is Nawaz Sharif")
# print(r)
# print(type(r))