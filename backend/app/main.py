from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, projects, jobs, download

app = FastAPI(
    title="AI Product Studio API",
    description="Private-cloud business automation suite",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(download.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "AI Product Studio v3.0", "status": "running"}
