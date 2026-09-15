from langchain.agents import create_agent
from calculation import calculction
from plot import generate_plot
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-120b")
tools=[
    calculction, generate_plot
]

SYSTEM_PROMPT = """
You are PlotMind.
Use calculation for mathematical calculations and symbolic problems.
Use generate_plot only when the user explicitly asks for a graph or plot.
Never plot unless the user asks.
"""

def get_agents():
    agents = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agents
agent = get_agents()