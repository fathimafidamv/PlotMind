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
        BACKEND_URL="https://plotmind.onrender.com"
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"query":query},
                timeout=20,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as error:
            st.error(f"Could not reach the plotting backend: {error}")
            result = None
        except ValueError:
            st.error("The plotting backend returned invalid JSON.")
            result = None

        if result is not None:
            st.json(result)
        required_fields = {"function", "x_min", "x_max", "x_value", "y_value"}
        if isinstance(result, dict) and "error" in result:
            st.error(result["error"])
        elif not isinstance(result, dict) or not required_fields.issubset(result):
            if result is not None:
                st.error("The plotting backend returned an unexpected response.")
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

