from langchain import OpenAI 
from langchain.chat_models import ChatAnthropic
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from decouple import config


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

obj = search.run("How do I treat an ant sting?")
print(obj)