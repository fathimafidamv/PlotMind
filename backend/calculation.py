import sympy as sp
from langchain_core.tools import tool

@tool
def calculction(expression : str):
    """ Solve mathematical expression and symbolic algebra/calculus problem accurately """
    try:
        exp = sp.sympify(expression)
        result = sp.simplify(exp)
        final_result=result.content
        return str(final_result)
    except Exception as e:
        print("Could not calculate expression: {e} ")
