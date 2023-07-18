from langchain import OpenAI 
from langchain.chat_models import ChatAnthropic
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.utilities import SerpAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from decouple import config
import random


llm = ChatAnthropic(anthropic_api_key=config("ANTHROPIC_API_KEY"), temperature=0)

search = DuckDuckGoSearchRun()
# defining a single tool
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    )
]


# search = SerpAPIWrapper(serpapi_api_key=config("SERPAPI_API_KEY"))
# tools = [
#     Tool(
#         name = "Current Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events or the current state of the world"
#     ),
# ]


#  Custom Tool Created
def math_difficulty(input=""):
    return "The Conclusion is math is easy"


math_tool = Tool(
    name="Math Difficulty",
    func=math_difficulty,
    description="Useful for when you want to find the difficulty of Math. Input should be easymath"
)


def random_number(input=""):
    return random.randint(0,5)


random_tool = Tool(
    name="Random Number",
    func=random_number,
    description="Useful for when you want to find a random number. Input should be random"
)

my_tools = [search, math_tool, random_tool]


# k=3 is max number of previous conversations saved
memory = ConversationBufferWindowMemory(memory_key='chat_history', k=3, return_messages=True)


conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=my_tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)

conversational_agent.run("Who is the current weather in South of Nigeria?")