import numpy as np 
import sympy as sp
import json 
from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b")

def generate_plot(function:str):
    prompt="""
    Generate graph data for a mathematical function.
    You are a mathematical plotting assistant. 
    Understand the user's request and extract the mathematical function 
    and x range. Return ONLY valid JSON. 
    Required format: {{ "function": "x**2", "x_min": -10, "x_max": 10 }} 
    Rules: - Convert ^ into **. 
    - Use Python/SymPy compatible expressions. 
    - If no x range is given, use -10 to 10. - Do not include markdown. 
    - Do not include explanations. 
    USER REQUEST: 
    {query}
    """
    response = llm.invoke(prompt)
    data = json.loads(response.content)
    function=data["function"]
    x_min=data["x_min"]
    x_max=data["x_max"]
    try:
        x = sp.symbols("x")
        expr = sp.sympify(function)
        f = sp.lambdify(x , expr , "numpy")

        x_value = np.linspace(x_min, x_max ,500)
        y_value = f(x_value)


        return {
            "function": function ,
            "x_min": x_min ,
            "x_max": x_max ,
            "x_value": x_value.tolist(),
            "y_value":y_value.tolist()
            }
    except Exception as e:
        return{
            "error":f"could not generate plot:{e}"
        }

