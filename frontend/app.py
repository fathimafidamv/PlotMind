import streamlit as st 
from dotenv import load_dotenv
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import os


load_dotenv()
BACKEND_URL = os.getenv("Backend_url")

st.title("PlotMind 📈 ")
st.caption("Function ploting AI assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask anything...!")
if query:
    st.session_state.messages.append(
        {
            "role":"user" , "content": query
        }
    )
    st.chat_message("user",avatar="🐧").markdown(query)

    with st.spinner("please wait..."):
        BACKEND_URL="http://127.0.0.1:8000"
        url = f"{BACKEND_URL}/Plot"
        response = requests.post(
            f"{BACKEND_URL}/Plot",
            json={"query":query}
        )

        result = response.json()
        if "error" in result:
            st.error(result["error"])
        else:
            st.chat_message("assistant",  avatar="👩‍🏫").markdown(
               f"y ={ result['function']} ,\n"
               f"x_min = {result['x_min']} , \n"
               f"x_max = {result['x_max']}"
            )
            st.session_state.messages.append(
                {
                    "role":"ai" , 
                    "content": f"y={result['function']} \n\n"
                               f"x_min = {result['x_min']} \n\n"
                               f"x_max = {result['x_max']}"
                }
            )
            x_value = np.array(result['x_value'])
            y_value = np.array(result['y_value'])

            fig , ax = plt.subplots()
            ax.plot(x_value , y_value)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Graph of y = {result['function']}")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

