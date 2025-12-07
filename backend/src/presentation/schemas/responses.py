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


class SeniorityScoresResponse(BaseModel):
    """Seniority score breakdown."""
    experience: float = Field(..., ge=0, le=1)
    complexity: float = Field(..., ge=0, le=1)
    autonomy: float = Field(..., ge=0, le=1)
    skills: float = Field(..., ge=0, le=1)
    leadership: float = Field(..., ge=0, le=1)
    impact: float = Field(..., ge=0, le=1)


class SeniorityResponse(BaseModel):
    """Detected seniority level response."""
    level: str = Field(..., description="Seniority level: junior, mid, or senior")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    years_experience: float = Field(..., ge=0, description="Total years of experience")
    scores: SeniorityScoresResponse = Field(..., description="Breakdown of scoring criteria")
    indicators: list[str] = Field(default_factory=list, description="Reasons for classification")


class GapResponse(BaseModel):
    """Employment gap information."""
    after_company: str = Field(..., description="Company before the gap")
    before_company: str = Field(..., description="Company after the gap")
    start_year: int = Field(..., description="Gap start year")
    end_year: int = Field(..., description="Gap end year")
    months: int = Field(..., description="Gap duration in months")


class TimelineEntryResponse(BaseModel):
    """Career timeline entry."""
    company: str = Field(..., description="Company name")
    title: str = Field(..., description="Job title")
    start_year: int = Field(..., description="Start year")
    end_year: Optional[int] = Field(default=None, description="End year (null if current)")
    duration_months: int = Field(..., description="Duration in months")
    seniority_level: int = Field(..., ge=1, le=8, description="Seniority level (1-8)")


class StabilityResponse(BaseModel):
    """Career stability analysis response."""
    score: int = Field(..., ge=0, le=100, description="Stability score (0-100)")
    flags: list[str] = Field(default_factory=list, description="Detected stability flags")
    indicators: list[str] = Field(default_factory=list, description="Reasons for score deductions")
    positive_notes: list[str] = Field(default_factory=list, description="Positive career patterns")
    avg_tenure_months: float = Field(..., ge=0, description="Average tenure per company in months")
    total_companies: int = Field(..., ge=0, description="Total number of companies")
    companies_in_5_years: int = Field(..., ge=0, description="Companies in last 5 years")
    consecutive_short_jobs: int = Field(..., ge=0, description="Consecutive jobs under 12 months")
    gaps: list[GapResponse] = Field(default_factory=list, description="Employment gaps > 6 months")


class AnalyzeResponse(BaseModel):
    """Full analysis response."""
    ats_result: ATSResultResponse
    job_matches: list[JobMatchResponse]
    best_fit: Optional[BestFitResponse] = None
    seniority: Optional[SeniorityResponse] = None
    stability: Optional[StabilityResponse] = None


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
