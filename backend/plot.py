import numpy as np 
import sympy as sp

from langchain_core.tools import tool

@tool
def generate_plot(function:str,x_min:float=-10 , x_max:float=10):
    """
    Generate graph data for a mathematical function.
    """
    try:
        x = sp.symbols("x")
        expr = sp.sympify(function)
        f = sp.lambdify(x , expr , "numpy")

        x_value = np.linspace(x_min, x_max ,500)
        y_value = f(x_value)


        return {
            "function": function ,
            "x_min": x_min ,
            "x_max": x_max 
            }
    except Exception as e:
        return{
            "error":f"could not generate plot:{e}"
        }

