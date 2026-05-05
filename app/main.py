from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Skill-Routed Multi-Agent Hiring System",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "AI Resume Screener API is running"
    }