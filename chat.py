from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
# from langchain.retrievers.document_compressors import LLMChainExtractor
# from langchain_community.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain import hub
# from vector_database import VectorDatabase
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
retriever = FAISS.load_local("vector_store",
                             embeddings=embeddings,
                             allow_dangerous_deserialization=True)
new_retriever = retriever.as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.7, "k": 1})
system_Prompt = "you are a humorous ai assistant.Answer base on the following retrieved documents: {context}"
prompt = ChatPromptTemplate.from_messages([("system", system_Prompt),
                                            ("human", "{input}")])

response = create_retrieval_chain(new_retriever, create_stuff_documents_chain(llm, prompt))
print(response.invoke({"input": "who is ayub ali khan"}))

