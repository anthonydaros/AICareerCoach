"""Analyze routes - Main analysis endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException

from src.presentation.schemas.requests import AnalyzeRequest, ATSScoreRequest, MatchJobsRequest
from src.presentation.schemas.responses import AnalyzeResponse, ATSResultResponse, JobMatchResponse
from src.presentation.api.dependencies import get_orchestrator
from src.application.orchestrator import CareerCoachOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    request: AnalyzeRequest,
    orchestrator: CareerCoachOrchestrator = Depends(get_orchestrator),
):
    """
    Perform full career analysis.

    This is the main endpoint that:
    1. Parses the resume
    2. Parses all job postings
    3. Calculates ATS score
    4. Matches resume against all jobs
    5. Identifies best fit

    Args:
        request: Resume text and job postings

    Returns:
        Full analysis with ATS score, job matches, and best fit recommendation
    """
    try:
        result = await orchestrator.analyze(
            resume_text=request.resume_text,
            job_postings=[
                {"id": jp.id, "text": jp.text}
                for jp in request.job_postings
            ],
        )
        return AnalyzeResponse(**result)
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/ats-score", response_model=ATSResultResponse)
async def calculate_ats_score(
    request: ATSScoreRequest,
    orchestrator: CareerCoachOrchestrator = Depends(get_orchestrator),
):
    """
    Calculate ATS compatibility score only.

    Lighter endpoint when you only need the ATS score
    without full job matching.

    Args:
        request: Resume text and single job posting

    Returns:
        ATS score breakdown
    """
    try:
        result = await orchestrator.analyze(
            resume_text=request.resume_text,
            job_postings=[{"id": "ats-job", "text": request.job_text}],
        )
        return ATSResultResponse(**result["ats_result"])
    except Exception as e:
        logger.error(f"ATS score calculation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"ATS calculation failed: {str(e)}")


@router.post("/match-jobs", response_model=list[JobMatchResponse])
async def match_jobs(
    request: MatchJobsRequest,
    orchestrator: CareerCoachOrchestrator = Depends(get_orchestrator),
):
    """
    Match resume against multiple job postings.

    Returns job matches sorted by match percentage.

    Args:
        request: Resume text and job postings

    Returns:
        List of job matches ranked by compatibility
    """
    try:
        result = await orchestrator.analyze(
            resume_text=request.resume_text,
            job_postings=[
                {"id": jp.id, "text": jp.text}
                for jp in request.job_postings
            ],
        )
        return [JobMatchResponse(**m) for m in result["job_matches"]]
    except Exception as e:
        logger.error(f"Job matching failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")
