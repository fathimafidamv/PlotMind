from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st 
import numpy as np
import json
import sympy as sp
import matplotlib.pyplot as plt



load_dotenv()

llm = ChatGroq( model="openai/gpt-oss-120b")

st.title("PlotMind📉")
st.caption("Malayalam AI Joke Chatbot 😂")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query=st.chat_input("Ask Anything ...!")
if query:
    st.session_state.messages.append(
        {
            "role":"user" , "content":query
        }
    )
    st.chat_message("user",avatar="🐧").markdown(query )

    prompt = f"""
    You are a mathematical plotting assistant.

    Understand the user's request and extract the mathematical function
    and x range.

    Return ONLY valid JSON.

    Required format:

    {{
        "function": "x**2",
        "x_min": -10,
        "x_max": 10
    }}

    Rules:
    - Convert ^ into **.
    - Use Python/SymPy compatible expressions.
    - If no x range is given, use -10 to 10.
    - Do not include markdown.
    - Do not include explanations.

    USER REQUEST:
    {query}
    """

    response = llm.invoke(prompt)
    result =json.loads(response.content)
    function = result["function"]
    x_min = result["x_min"]
    x_max = result["x_max"]

    x = sp.symbols("x")
    expr = sp.sympify(function)
    f = sp.lambdify(x,expr,"numpy")
    x_value = np.linspace(x_min,x_max,500)
    y_value = f(x_value)
    fig,ax = plt.subplots()
    ax.plot(x_value,y_value)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    st.pyplot(fig)
    st.session_state.messages.append(
        {
            "role":"ai", "content":result
        }
    )

    st.chat_message("ai",avatar="👩‍🏫").markdown(result)