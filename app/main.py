from fastapi import FastAPI
from app.routers import salary

app = FastAPI(
    title="Salary Prediction API",
    description="API that predicts salary based on job posting ID",
    version="1.0.0"
)

app.include_router(salary.router, prefix="/predict", tags=["predictions"])

@app.get("/")
async def root():
    return {"message": "Salary Prediction API"} 