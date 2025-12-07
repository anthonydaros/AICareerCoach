"""API routes."""

from .upload import router as upload_router
from .analyze import router as analyze_router
from .interview_prep import router as interview_router
from .coaching_tips import router as coaching_router

__all__ = [
    "upload_router",
    "analyze_router",
    "interview_router",
    "coaching_router",
]
