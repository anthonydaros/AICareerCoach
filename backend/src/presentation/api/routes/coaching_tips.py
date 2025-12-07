"""Coaching tips route - Generate career coaching tips."""

import logging
from fastapi import APIRouter, Depends, HTTPException

from src.presentation.schemas.requests import CoachingTipsRequest
from src.presentation.schemas.responses import CoachingTipsResponse, CoachingTipResponse
from src.presentation.api.dependencies import get_orchestrator
from src.application.orchestrator import CareerCoachOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Coaching"])


@router.post("/coaching-tips", response_model=CoachingTipsResponse)
async def generate_coaching_tips(
    request: CoachingTipsRequest,
    orchestrator: CareerCoachOrchestrator = Depends(get_orchestrator),
):
    """
    Generate personalized career coaching tips.

    Creates actionable advice based on:
    - Candidate's resume
    - Target job postings
    - Match results

    Returns tips in three categories:
    - Quick wins (immediate actions)
    - Skill gaps to address
    - Application strategy

    Args:
        request: Resume text, job postings, and optional match results

    Returns:
        Career coaching tips organized by category
    """
    try:
        result = await orchestrator.generate_coaching_tips(
            resume_text=request.resume_text,
            job_postings=[
                {"id": jp.id, "text": jp.text}
                for jp in request.job_postings
            ],
            match_results=request.match_results,
        )

        return CoachingTipsResponse(
            tips=[
                CoachingTipResponse(**t)
                for t in result["tips"]
            ],
        )
    except Exception as e:
        logger.error(f"Coaching tips generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Coaching tips generation failed: {str(e)}"
        )
