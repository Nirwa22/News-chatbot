from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class VectorDatabase:
    def __init__(self):
        self.chunk_size = 100
        self.chunk_overlap = 80
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def text_loader_splitter(self, file_path):
        file_type = open(file_path).name[-4:]
        if file_type == ".txt":
            print("text")
            with open(file_path, encoding="utf-8") as file:
                text = file.read()
            chunks = self.text_splitter.create_documents(self.text_splitter.split_text(text))
            return chunks
        elif file_type == ".pdf":
            print("pdf")
            text = PyPDFLoader(file_path).load()
            chunks = self.text_splitter.split_documents(text)
            return chunks
        elif file_type == "docx":
            print("docx")
            text = Docx2txtLoader(file_path).load()
            chunks = self.text_splitter.split_documents(text)
            return chunks
        else:
            return {"message": "Invalid file type"}

    def vector_store(self, filepath):
        vectorstore = FAISS.from_documents(self.text_loader_splitter(filepath), embedding=self.embeddings)
        return vectorstore

    def save_database(self, path, file_path):
        return FAISS.save_local(self.vector_store(file_path), path)

    def access_vectorstore(self, path):
        vs = FAISS.load_local(path, embeddings=self.embeddings)
        return vs

    def add_documents(self, new_document, file_path):
        return self.vector_store(file_path).add_documents(new_document)


VectorDatabase("document_files/History.txt", "Vectordb").vector_store()

