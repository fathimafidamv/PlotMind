from fastapi import FastAPI
from langchain_groq import ChatGroq
from model import PlotRequest
from plot import generate_plot

app = FastAPI(title="PlotMind API")


@app.get("/")
def get_home():
    return{
        "message":"PlotMind API is running"
    }

@app.post("/Plot")
def plot(request: PlotRequest):   
    try:
       data = generate_plot(request.query)
       return data
    except Exception as e:
        print(f"error bcz { e }")
        return {
            "error": str(e)
        }