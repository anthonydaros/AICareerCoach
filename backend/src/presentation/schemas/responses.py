"""API response schemas."""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str = "AI Career Coach Backend"


class UploadResponse(BaseModel):
    """File upload response."""
    filename: str = Field(..., description="Uploaded filename")
    content_type: str = Field(..., description="File content type")
    text_content: str = Field(..., description="Extracted text content")
    char_count: int = Field(..., description="Character count of extracted text")


class MatchLevel(str, Enum):
    """Job match quality level."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ATSResultResponse(BaseModel):
    """ATS score result response."""
    total_score: float = Field(..., ge=0, le=100)
    skill_score: float = Field(..., ge=0)
    experience_score: float = Field(..., ge=0)
    education_score: float = Field(..., ge=0)
    certification_score: float = Field(..., ge=0)
    keyword_score: float = Field(..., ge=0)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    format_issues: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)


class SkillGapResponse(BaseModel):
    """Skill gap response."""
    skill: str
    is_required: bool
    suggestion: str
    learning_resources: list[str] = Field(default_factory=list)


class JobMatchResponse(BaseModel):
    """Job match result response."""
    job_id: str
    job_title: str
    company: Optional[str] = None
    match_percentage: float = Field(..., ge=0, le=100)
    match_level: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    skill_gaps: list[SkillGapResponse] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    is_best_fit: bool = False


class BestFitResponse(BaseModel):
    """Best fit recommendation response."""
    job_id: str
    job_title: str
    match_percentage: float
    recommendation: str


class AnalyzeResponse(BaseModel):
    """Full analysis response."""
    ats_result: ATSResultResponse
    job_matches: list[JobMatchResponse]
    best_fit: Optional[BestFitResponse] = None


class InterviewQuestionResponse(BaseModel):
    """Interview question response."""
    question: str
    category: str
    why_asked: str
    what_to_say: list[str] = Field(default_factory=list)
    what_to_avoid: list[str] = Field(default_factory=list)


class InterviewPrepResponse(BaseModel):
    """Interview prep response."""
    job_title: str
    questions: list[InterviewQuestionResponse]


class CoachingTipResponse(BaseModel):
    """Coaching tip response."""
    category: str
    title: str
    description: str
    action_items: list[str] = Field(default_factory=list)
    priority: str = "medium"


class CoachingTipsResponse(BaseModel):
    """Coaching tips response."""
    tips: list[CoachingTipResponse]


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    error_type: Optional[str] = None
