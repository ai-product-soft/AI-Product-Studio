from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import projects, jobs, auth, health, download
from app.api import llm, mcp, approvals, notifications, services, social, leads, proposals, showcases, payments
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="AI Product Studio API", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(download.router, prefix="/api/download", tags=["Download"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM"])
app.include_router(mcp.router, prefix="/api/mcp", tags=["MCP"])
app.include_router(approvals.router, prefix="/api/approvals", tags=["Approvals"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(services.router, prefix="/api/services", tags=["Services"])
app.include_router(social.router, prefix="/api/social", tags=["Social"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(proposals.router, prefix="/api/proposals", tags=["Proposals"])
app.include_router(showcases.router, prefix="/api/showcases", tags=["Showcases"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "AI Product Studio v4.0 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
