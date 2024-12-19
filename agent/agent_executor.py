# from agent.agent_prompt import agent_prompt
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
# from tools.gmail_tool import
from tools.rag_tool import tool_rag
from tools.news_tool import tool_news
from tools.googleapi_search import google_search_tool
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class Agent:
    def __init__(self):
        self.tool_kit = [tool_news, google_search_tool, tool_rag]
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
        self.agent_prompt = hub.pull("hwchase17/react")
        # self.memory = memory

    def create_agent(self):
        agent = create_react_agent(self.llm,
                                   self.tool_kit,
                                   self.agent_prompt)

        return agent

    def agent_execution(self, query):
        agent_executor = AgentExecutor.from_agent_and_tools(agent=self.create_agent(),
                                                            tools=self.tool_kit,
                                                            verbose=True,
                                                            handle_parsing_errors=True)
        response = str(agent_executor.invoke({"input": query}))
        return response


print(Agent().agent_execution("what happened in 1947 for pakistan"))