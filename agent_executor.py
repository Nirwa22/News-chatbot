# from agent.agent_prompt import agent_prompt
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from tools.gmail_tool import tool_gmail
from tools.rag_tool import tool_rag
from tools.news_tool import tool_news
from tools.googleapi_search import google_search_tool
from dotenv import load_dotenv
import json
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class AgentReact:
    def __init__(self):
        self.tool_kit = [tool_news, google_search_tool, tool_rag, tool_gmail]
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, stream=True)
        self.prompt = hub.pull("hwchase17/react")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.template = '''You are a very helpful AI Assistant.
                            Always reply in a formal manner and in form of a paragraph.
                            Answer the following questions as best you can.
                            You have access to the following tools:
                            {tools} but do not take a tool's output as final output. Modify it to
                            a representable form by following the below instructions:
                            1. Output must be paragraph based
                            For queries outside the scope of Pakistan's news and history do
                            not use the tools whatsoever and do not reply at all.

                            Use the following format:

                            Question: the input question you must answer
                            Thought: you should always think about what to do
                            Action: the action to take, should be one of [{tool_names}]
                            Action Input: the input to the action
                            Observation: the result of the action
                            ... (this Thought/Action/Action Input/Observation can repeat N times)
                            Thought: I now know the final answer but I need to make sure it is in paragraph form.If not
                            then use the llm to do so.
                            Final Answer: the final answer to the original input question. Must be a paragraph always
                            ans set a poetic tone

                            Begin!

                            Question: {input}
                            Thought:{agent_scratchpad}'''

    def agent_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.template)])
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
                                       memory=self.memory)
        response = agent_executor.invoke({"input": query})
        return response


print(AgentReact().agent_execution("who is current army's cheif officer")["output"])
# print(json.loads("Action Input:"))
