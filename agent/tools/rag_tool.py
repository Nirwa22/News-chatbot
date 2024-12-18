from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from vector_database import VectorDatabase
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class RagTool:
    name = "Rag_tool"
    description = """Use this tool only when the query is related to the vector database content, For general queries
                    outside the scope of vector database do not use this tool whatsoever """
    def __init__(self, data, query, embedding_model):
        # self.data = data
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.embedding_model = embedding_model
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
        self.query = query

    def retriever(self):
        retriever = VectorDatabase().access_vectorstore("Vectordb")
        new_retriever = retriever.as_retriever(search_type="mmr")
        answer = new_retriever.invoke(self.query)
        return answer

    def add_embeddings(self, data):
        vb = VectorDatabase().add_documents(data, "")
        return vb.add_documents(data)


    def rag_response(self):
