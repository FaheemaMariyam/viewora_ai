#Entry point of the FastAPI AI service.
from fastapi import FastAPI

app = FastAPI(title="Viewora AI Service")

@app.get("/health")
def health():
    return {"status": "FastAPI is running"}

@app.post("/ai/area-insights")
def area_insights(data: dict):
    return {
        "message": "Response from FastAPI microservice",
        "input": data,
        "growth_score": 8.3,
        "rental_potential": "High"
    }
#latter  move to app/