from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api import analysis_endpoints

app = FastAPI()

# Include API routers
app.include_router(analysis_endpoints.router, prefix="/api/v1")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/static/index.html")
