from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class VectorDatabase:
    def __init__(self, file_path):
        self.chunk_size = 100
        self.chunk_overlap = 80
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.file_path = file_path

    def text_loader(self):
        file_type = open(self.file_path).name[-4:]
        if file_type == ".txt":
            print("text")
            return TextLoader(self.file_path).load()
        elif file_type == ".pdf":
            print("pdf")
            return PyPDFLoader(self.file_path).load()
        elif file_type == "docx":
            print("docx")
            return Docx2txtLoader(self.file_path).load()

    def splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,
                                                       chunk_overlap=self.chunk_overlap)
        chunks = text_splitter.split_documents(self.text_loader())
        return chunks

    def vector_store(self):
        vectorstore = FAISS.from_documents(self.splitter(),
                                           embedding=self.embeddings
                                           )
        return vectorstore

    def add_documents(self, new_document):
        return self.vector_store().add_documents(new_document)


VectorDatabase("document_files/6ea9ab1baa0efb9e19094440c317e21b.pdf").vector_store()
