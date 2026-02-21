"""
Seed Agents - Autonomous Agent SaaS Platform
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import settings
from app.routes import agents, workflow, telegram, api

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(agents.router)
app.include_router(workflow.router)
app.include_router(telegram.router)
app.include_router(api.router)

# Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Seed Agents</h1><p>Frontend not found.</p>")


@app.get("/health")
async def health():
    from app.services.database import db
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "agents_count": len(db.agents),
        "workflows_count": len(db.workflows),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
