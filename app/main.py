"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.routes import router


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

    @app.on_event("startup")
    async def on_startup() -> None:
        await init_db()

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
