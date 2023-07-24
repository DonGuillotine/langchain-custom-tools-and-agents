from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper
from decouple import config


llm = OpenAI(openai_api_key=config('OPENAI_API_KEY'), temperature=0)
zapier = ZapierNLAWrapper(zapier_nla_api_key=config('ZAPIER_NLA_API_KEY'))
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(
    toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)