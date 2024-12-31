from prompt import template
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tools.gmail_tool import tool_gmail
from tools.rag_tool import tool_rag
from tools.news_tool import tool_news
from tools.googleapi_search import google_search_tool
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class AgentReact:
    def __init__(self):
        self.tool_kit = [tool_news, google_search_tool, tool_rag, tool_gmail]
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, stream=True)
        # self.prompt = hub.pull("hwchase17/react")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.template = template

    def agent_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.template),
             MessagesPlaceholder(variable_name="chat_history")])
        return prompt_template

    def create_agent(self):
        agent = create_react_agent(self.llm,
                                   self.tool_kit,
                                   self.agent_prompt())
        return agent

    def agent_execution(self, query):
        agent_executor = AgentExecutor(agent=self.create_agent(),
                                       tools=self.tool_kit,
                                       verbose=True,
                                       handle_parsing_errors=True,
                                       memory=self.memory,
                                       max_execution_time=40)
                                       # max_iterations=1)
        response = agent_executor.invoke({"input": query})
        self.memory = self.memory.save_context({"input": query}, {"output": response["output"]})
        return response


# print(AgentReact().agent_execution("what was my last question"))
# print(json.loads("Action Input:"))
