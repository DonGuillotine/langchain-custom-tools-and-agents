from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from bs4 import BeautifulSoup
import requests
from decouple import config
import random
import requests


BITLY_API_TOKEN = config("BITLY_API_TOKEN")

llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), temperature=0)


search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    )
]


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


class WebPageTool(BaseTool):
    name = "Get Webpage"
    description = "Useful for when you need to get the content from a specific webpage"

    def _run(self, webpage: str):
        response = requests.get(webpage)
        html_content = response.text
        
        def strip_html_tags(html_content):
            soup = BeautifulSoup(html_content, "html.parser")
            stripped_text = soup.get_text()
            return stripped_text
        
        stripped_content = strip_html_tags(html_content)
        
        if len(stripped_content) > 4000:
            stripped_content = stripped_content[:4000]
            return stripped_content

    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")

page_getter = WebPageTool()


class UrlShortnerTool(BaseTool):
    name = "Shorten URL"
    description = "Useful for when you need to shorten a URL"

    def _run(self, url: str):
        global BITLY_API_TOKEN

        api_url = 'https://api-ssl.bitly.com/v4/shorten'
        headers = {
            'Authorization': f'Bearer {BITLY_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        data = {
            'long_url': url
        }

        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            short_url = response.json()['id']
            return short_url
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


    def _arun(self, url: str):
        raise NotImplementedError("This tool does not support async")

url_shortner = UrlShortnerTool()


my_tools = [math_tool, random_tool, page_getter, url_shortner]


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


conversational_agent.run("What are the top headlines from https://www.bbc.co.uk today?")