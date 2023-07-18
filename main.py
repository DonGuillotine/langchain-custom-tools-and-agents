from langchain import OpenAI 
from langchain.chat_models import ChatAnthropic
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools import BaseTool
from decouple import config


llm = ChatAnthropic(anthropic_api_key=config("ANTHROPIC_API_KEY"), temperature=0)

search = SerpAPIWrapper(serpapi_api_key=config("SERPAPI_API_KEY"))
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]


#  Custom Tool Created
def math_is_easy(input=""):
    return "The Conclusion is math is easy"


