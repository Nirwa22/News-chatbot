# from agent.agent_prompt import agent_prompt
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
# from tools.gmail_tool import
from tools.rag_tool import tool_rag
from tools.news_tool import tool_news
from tools.googleapi_search import google_search_tool
from dotenv import load_dotenv
import json
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class Agent:
    def __init__(self):
        self.tool_kit = [tool_news, google_search_tool, tool_rag]
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, stream=True)
        self.agent_prompt = hub.pull("hwchase17/react")
        self.memory = ConversationBufferMemory(memory_key="chat_history")

    def create_agent(self):
        agent = create_react_agent(self.llm,
                                   self.tool_kit,
                                   self.agent_prompt)

        return agent

    def agent_execution(self, query):
        agent_executor = AgentExecutor(agent=self.create_agent(),
                                       tools=self.tool_kit,
                                       verbose=True,
                                       handle_parsing_errors=True,
                                       memory=self.memory)
        response = str(agent_executor.invoke({"input": self.memory}))
        # self.memory.asave_context({"input": query}, {"output": response})
        return str(response)


print(Agent().agent_execution("hi i am sara"))
# print(json.loads("Action Input:"))
