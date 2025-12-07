"""API request and response schemas."""

from .requests import (
    JobPostingInput,
    AnalyzeRequest,
    ATSScoreRequest,
    MatchJobsRequest,
    InterviewPrepRequest,
    CoachingTipsRequest,
)
from .responses import (
    HealthResponse,
    UploadResponse,
    ATSResultResponse,
    SkillGapResponse,
    JobMatchResponse,
    BestFitResponse,
    AnalyzeResponse,
    InterviewQuestionResponse,
    InterviewPrepResponse,
    CoachingTipResponse,
    CoachingTipsResponse,
    ErrorResponse,
)

__all__ = [
    # Requests
    "JobPostingInput",
    "AnalyzeRequest",
    "ATSScoreRequest",
    "MatchJobsRequest",
    "InterviewPrepRequest",
    "CoachingTipsRequest",
    # Responses
    "HealthResponse",
    "UploadResponse",
    "ATSResultResponse",
    "SkillGapResponse",
    "JobMatchResponse",
    "BestFitResponse",
    "AnalyzeResponse",
    "InterviewQuestionResponse",
    "InterviewPrepResponse",
    "CoachingTipResponse",
    "CoachingTipsResponse",
    "ErrorResponse",
]
