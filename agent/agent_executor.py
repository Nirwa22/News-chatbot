# from agent.agent_prompt import agent_prompt
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
# from tools.gmail_tool import
# from tools.rag_tool import
from tools.news_tool import tool_news
from tools.googleapi_search import google_search_tool
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self):
        self.tool_kit = [tool_news, google_search_tool]
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
        self.agent_prompt = hub.pull("hwchase17/react")
        # self.memory = memory

    def create_agent(self):
        agent = create_react_agent(llm=self.llm,
                                   tools=self.tool_kit,
                                   prompt=self.agent_prompt)
        return agent

    def agent_execution(self, query):
        agent_executor = AgentExecutor(agent=self.create_agent(),
                                       tools=self.tool_kit,
                                       verbose=True,
                                       handle_parsing_errors=True)
        return agent_executor.invoke({"input": query})


print(Agent().agent_execution("who is harry potter"))