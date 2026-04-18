"""
backend/main.py
FastAPI application entry point.
Mounts all routers and configures CORS.

Run with:
    uvicorn main:app --reload --port 8000
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from api.routers import analyze, graph, node, query, onboarding, reports, voice, stress, timeline

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# ── App ───────────────────────────────────────────────────────────────────────
settings = get_settings()

app = FastAPI(
    title="git-filter API",
    description="Repository Architecture Navigator — Analysis & Intelligence Backend",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers (all prefixed with /api/v1) ───────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(analyze.router, prefix=API_PREFIX)
app.include_router(graph.router, prefix=API_PREFIX)
app.include_router(node.router, prefix=API_PREFIX)
app.include_router(query.router, prefix=API_PREFIX)
app.include_router(onboarding.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(voice.router, prefix=API_PREFIX)
app.include_router(stress.router, prefix=API_PREFIX)
app.include_router(timeline.router, prefix=API_PREFIX)


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check():
    from ai.ollama_client import is_ollama_available, list_available_models
    ollama_ok = is_ollama_available()
    models = list_available_models() if ollama_ok else []
    return {
        "status": "ok",
        "ollama_available": ollama_ok,
        "ollama_models": models,
        "configured_model": settings.ollama_model,
    }


@app.get("/", tags=["root"])
async def root():
    return {
        "name": "git-filter API",
        "version": "1.0.0",
        "docs": "/docs",
    }
