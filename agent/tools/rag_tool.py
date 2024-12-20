from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.tools import Tool
from langchain_community.vectorstores import FAISS
# from vector_database import VectorDatabase
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class RagTool:
    name = "Rag_tool"
    description = """Use this tool only when the query is related to the vector database content, For general queries
                    outside the scope of vector database do not use this tool whatsoever """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
        self.retriever = FAISS.load_local("vector_store",
                                          embeddings=self.embeddings,
                                          allow_dangerous_deserialization=True)
        self.prompt =

    def retriever(self, query):
        new_retriever = self.retriever.as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.7, "k": 1})
        system_prompt = "you are a humorous ai assistant.Answer base on the following retrieved documents: {context}"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                   ("human", "{input}")])
        response = create_retrieval_chain(new_retriever, create_stuff_documents_chain(self.llm, prompt))
        return response.invoke({"input": query})

    # def add_embeddings(self, data):
    #     vb = VectorDatabase(data).vector_store()
    #     return vb.add_documents(data)


tool_rag = Tool.from_function(name=RagTool.name,
                              description=RagTool.description,
                              func=RagTool.retriever,
                              return_direct=True)

