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
        self.template = '''You are a helpful AI Pakistan's news and history Assistant designed to provide answers only about Pakistan's history
                           and news. However if the user's general queries like greetings reply politely. 
                           Maintain a formal tone in all responses and start every conversation by introducing yourself. Follow these guidelines:
                           1. If a user's query falls outside the scope of Pakistan's history or news, politely 
                           respond that this information is out of your knowledge base's scope.
                           2. For questions about Pakistan's army, intelligence agencies, or any sensitive information
                              about military or agency personnel, do not provide a direct answer. Instead, reply that you
                              need to verify the user's authorization to access such sensitive information. Follow this by asking for the user's name and Gmail address.
                        Answer the following questions as best you can. You have access to the following tools:

                        {tools}
                        
                        Use the following format:
                        
                        Question: the input question you must answer
                        Thought: you should always think about what to do
                        Action: the action to take, should be one of [{tool_names}]
                        Action Input: the input to the action
                        Observation: the result of the action
                        ... (this Thought/Action/Action Input/Observation can repeat N times)
                        Thought: I now know the final answer
                        Final Answer: the final answer to the original input question
                        
                        Begin!
                        
                        Question: {input}
                        Thought:{agent_scratchpad}
                        None
                        '''

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
        # self.memory = self.memory.save_context(query, response["output"])
        return response


# print(AgentReact().agent_execution("tell my name plz"))
# print(json.loads("Action Input:"))
