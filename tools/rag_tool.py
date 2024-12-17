from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from vector_database import VectorDatabase
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

vectordatabase

class RagTool:
    name = "Rag_tool"
    description = """Use this tool only when the query is related to the vector database content, For general queries
                    outside the scope of vector database do not use this tool whatsoever """
    def __init__(self, data, query, embedding_model, llm):
        self.data = data
        self.query = query
        self.embedding_model = embedding_model
        self.llm = llm

    def add_embeddings(self):
        return vector_database.add_documents(self.data)


    def rag_response(self):
