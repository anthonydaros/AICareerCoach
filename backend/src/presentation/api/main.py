"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.presentation.api.routes import (
    upload_router,
    analyze_router,
    interview_router,
    coaching_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting AI Career Coach API...")
    settings = get_settings()
    logger.info(f"Using LLM: {settings.openai_model} at {settings.openai_base_url}")
    yield
    logger.info("Shutting down AI Career Coach API...")


# Create FastAPI application
app = FastAPI(
    title="AI Career Coach API",
    description="""
    AI-powered career assistant API.

    Features:
    - Resume ATS compatibility scoring
    - Multi-job matching and ranking
    - Interview preparation questions
    - Career coaching tips

    **Powered by Ollama with OpenAI-compatible API**
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
settings = get_settings()
origins = settings.get_allowed_origins_list()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(interview_router)
app.include_router(coaching_router)


@app.get("/health", tags=["System"])
async def health_check():
    """Check API health status."""
    return {
        "status": "healthy",
        "service": "AI Career Coach Backend",
        "version": "1.0.0",
    }


@app.get("/", tags=["System"])
async def root():
    """API root endpoint."""
    return {
        "message": "AI Career Coach API",
        "docs": "/docs",
        "health": "/health",
    }
