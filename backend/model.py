from pydantic import BaseModel

class PlotRequest(BaseModel):
    query: str