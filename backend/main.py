from fastapi import FastAPI
from langchain_groq import ChatGroq
from agent import agent
from model import ChatRequest

app = FastAPI(title="PlotMind API")

@app.get("/")
def get_home():
    return{
        "message":"PlotMind API is running"
    }

@app.post("/chat")
def chat(request: ChatRequest):   
    try:
        response = agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":request.query
                    }
                ]
            }
        )
        final_message  = response["messages"][-1]
        return {
            "answer":final_message.content
        }
    except Exception as e:
        print(f"error bcz { e }")
        return {
            "error": str(e)
        }