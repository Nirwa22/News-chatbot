from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from vector_database import VectorDatabase
import json
import os

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)


class GoogleSearchTool:
    name = "Google search tool"
    description = """Use this tool when you can not find relevant content related to Pakistan's history
                     in vector database. For input queries outside the scope of pakistan's news and history
                     you must not use this tool at all. For general queries use your own knowledge database.
                     Input to this tool will be a string query"""

    def __init__(self):
        self.search_method = SerpAPIWrapper()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)

    def search_function(self, query):
        retrieved_content_from_google = json.dumps(self.search_method.run(query))
        retriever = VectorDatabase().text_loader_splitter_vs(retrieved_content_from_google)
        new_retriever = retriever.as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.7, "k": 1})
        system_prompt = "Answer based on the following retrieved documents: {context}"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                   ("human", "{input}")])
        response = create_retrieval_chain(new_retriever, create_stuff_documents_chain(self.llm, prompt))
        return response.invoke({"input": query})["answer"]


google_search_tool = Tool.from_function(
    name=GoogleSearchTool().name,
    description=GoogleSearchTool().description,
    func=GoogleSearchTool().search_function,
    return_direct=True
)