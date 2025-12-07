"""Interview prep route - Generate interview questions."""

import logging
from fastapi import APIRouter, Depends, HTTPException

from src.presentation.schemas.requests import InterviewPrepRequest
from src.presentation.schemas.responses import InterviewPrepResponse, InterviewQuestionResponse
from src.presentation.api.dependencies import get_orchestrator
from src.application.orchestrator import CareerCoachOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Interview Prep"])


@router.post("/interview-prep", response_model=InterviewPrepResponse)
async def generate_interview_prep(
    request: InterviewPrepRequest,
    orchestrator: CareerCoachOrchestrator = Depends(get_orchestrator),
):
    """
    Generate interview preparation questions.

    Creates personalized interview questions based on:
    - Candidate's resume
    - Job requirements
    - Skill gaps

    Args:
        request: Resume text, job posting, and optional skill gaps

    Returns:
        Interview questions organized by category
    """
    try:
        result = await orchestrator.generate_interview_prep(
            resume_text=request.resume_text,
            job_text=request.job_text,
            skill_gaps=request.skill_gaps,
        )

        return InterviewPrepResponse(
            job_title=result["job_title"],
            questions=[
                InterviewQuestionResponse(**q)
                for q in result["questions"]
            ],
        )
    except Exception as e:
        logger.error(f"Interview prep generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Interview prep generation failed: {str(e)}"
        )
