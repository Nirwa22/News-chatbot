# from agent.agent_prompt import agent_prompt
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
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
        self.prompt = hub.pull("hwchase17/react")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def agent_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Answer the following questions as best you can.\n"
                       ".You have access to the following tools:{tools}"
                       "\n\nUse the following format:"
                       "\n\nQuestion: the input question you must answer"
                       "\nThought: you should always think about what to do"
                       "\nAction: the action to take, should be one of [{tool_names}]."
                       "\nAction Input: the input to the action"
                       "\nObservation: the result of the action)"
                       "\n\n... (this Thought/Action/Action Input/Observation can repeat 5 times)"
                       "\nThought: I now know the final answer"
                       "\nOutput formatting"
                       "Length: [Specify character or word count]"
                       "Structure: [Bullets, paragraph, JSON]"
                       "Style & Tone: [Use clear, concise, and straightforward language]"
                       "Even if you are using Google search tool or News tool provide answer"
                       "in form of paragraph in every case.Now, complete "
                       "the [Task] and follow the instructions strictly."
                       "\nFinal Answer: the final answer to the original input question.Always "
                       "provide a single line answer. Set a very formal tone."
                       "\n\nBegin!"
                       "\n\nQuestion: {input}"
                       "\nThought:{agent_scratchpad}"),
        #     Always provide the source
        # from where the
        # final
        # answer
        # has
        # been
        # derived.For
        # example\n
        # "
        # "if Action: Rag_tool then at the end of the final answer you must mention Source: Vector database\n"
        # "else mention Source: Internet"
            ("placeholder", "{chat_history}")])
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
        response = str(agent_executor.invoke({"input": query}))
        return str(response)


print(Agent().agent_execution("who is voldemort")["output"])
# print(Agent().agent_execution("tell my name"))
# print(json.loads("Action Input:"))
