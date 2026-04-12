"""FastAPI application entry point."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.api.routes import router

# Resolve paths relative to the project root (one level above this file)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FRONTEND_DIR = os.path.join(_BASE_DIR, "frontend")
_GENERATED_DIR = os.path.join(_BASE_DIR, "generated")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="PPT Generator",
        description="AI-powered PowerPoint presentation generator using Claude.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(router, prefix="/api/v1")

    # Serve generated .pptx files so the frontend can download them
    os.makedirs(_GENERATED_DIR, exist_ok=True)
    app.mount("/generated", StaticFiles(directory=_GENERATED_DIR), name="generated")

    # Serve the frontend SPA
    if os.path.isdir(_FRONTEND_DIR):
        app.mount("/static", StaticFiles(directory=_FRONTEND_DIR), name="frontend-static")

    @app.on_event("startup")
    async def on_startup() -> None:
        await init_db()

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """Serve the frontend UI."""
        index = os.path.join(_FRONTEND_DIR, "index.html")
        if os.path.isfile(index):
            return FileResponse(index, media_type="text/html")
        return {"message": "PPT Generator API", "docs": "/docs"}

    return app


app = create_app()
