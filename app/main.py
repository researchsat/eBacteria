from fastapi import FastAPI
from app.api import analysis_endpoints

app = FastAPI()

app.include_router(analysis_endpoints.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Microbial Analysis SaaS API"}
