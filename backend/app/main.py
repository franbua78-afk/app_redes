from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from .settings import settings
from .routers import health, auth, videos, schedule, analytics, upload, templates, system
from .startup import init_db


app = FastAPI(title="AI Shorts Studio", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(schedule.router)
app.include_router(analytics.router)
app.include_router(upload.router)
app.include_router(templates.router)
app.include_router(system.router)


@app.get("/")
async def root():
    return JSONResponse({"service": "ai-shorts-studio", "status": "ok"})

