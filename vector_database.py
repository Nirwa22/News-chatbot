from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
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

    def text_loader_splitter(self, file):
        file_type = open(file).name[-4:]
        if file_type == ".txt":
            print("text")
            with open(file, encoding="utf-8") as file:
                text = file.read()
            chunks = self.text_splitter.create_documents(self.text_splitter.split_text(text))
            return chunks
        elif file_type == ".pdf":
            print("pdf")
            text = PyPDFLoader(file).load()
            chunks = self.text_splitter.split_documents(text)
            return chunks
        elif file_type == "docx":
            print("docx")
            text = Docx2txtLoader(file).load()
            chunks = self.text_splitter.split_documents(text)
            return chunks
        else:
            return {"message": "Invalid file type"}

    def vector_store(self, file):
        vectorstore = FAISS.from_documents(self.text_loader_splitter(file), embedding=self.embeddings)
        return vectorstore


# vb = VectorDatabase().vector_store("document_files/History.txt")
# vb.add_documents(VectorDatabase().text_loader_splitter("document_files/a_chronology_of_key_events_ (1).docx"))
# vb.add_documents(VectorDatabase().text_loader_splitter("document_files/6ea9ab1baa0efb9e19094440c317e21b.pdf"))
# vb.save_local(folder_path="vector_store")

