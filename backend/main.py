from fastapi import FastAPI
from plot import generate_plot
from model import PlotRequest

app = FastAPI(title="PlotMind API")

@app.get("/")
def get_home():
    return{
        "message":"PlotMind API is running"
    }

@app.post("/Plot")
def plot_graph(request: PlotRequest):   
    try:
        data = generate_plot(request.query)

    
        return data 
    except Exception as e:
        print(f"error bcz { e }")
        return {
            "error": str(e)
        }