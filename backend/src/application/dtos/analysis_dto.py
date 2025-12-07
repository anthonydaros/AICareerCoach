"""Analysis-related DTOs."""

from typing import Optional
from pydantic import BaseModel, Field

from .job_dto import JobPostingInput


class AnalyzeRequest(BaseModel):
    """Request for full analysis."""
    resume_text: str = Field(..., min_length=100, description="Resume text content")
    job_postings: list[JobPostingInput] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="List of job postings to analyze"
    )


class ATSResultDTO(BaseModel):
    """ATS score result DTO."""
    total_score: float
    skill_score: float
    experience_score: float
    education_score: float
    certification_score: float
    keyword_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    format_issues: list[str]
    improvement_suggestions: list[str]


class SkillGapDTO(BaseModel):
    """Skill gap DTO."""
    skill: str
    is_required: bool
    suggestion: str
    learning_resources: list[str] = Field(default_factory=list)


class JobMatchDTO(BaseModel):
    """Job match result DTO."""
    job_id: str
    job_title: str
    company: Optional[str]
    match_percentage: float
    match_level: str
    matched_skills: list[str]
    missing_skills: list[str]
    skill_gaps: list[SkillGapDTO]
    strengths: list[str]
    concerns: list[str]
    is_best_fit: bool = False


class BestFitDTO(BaseModel):
    """Best fit recommendation DTO."""
    job_id: str
    job_title: str
    match_percentage: float
    recommendation: str


class InterviewQuestionDTO(BaseModel):
    """Interview question DTO."""
    question: str
    category: str
    why_asked: str
    what_to_say: list[str]
    what_to_avoid: list[str] = Field(default_factory=list)


class CoachingTipDTO(BaseModel):
    """Coaching tip DTO."""
    category: str
    title: str
    description: str
    action_items: list[str]
    priority: str = "medium"


class AnalyzeResponse(BaseModel):
    """Response for full analysis."""
    ats_result: ATSResultDTO
    job_matches: list[JobMatchDTO]
    best_fit: Optional[BestFitDTO]


class InterviewPrepRequest(BaseModel):
    """Request for interview prep."""
    resume_text: str = Field(..., min_length=100)
    job_text: str = Field(..., min_length=50)
    skill_gaps: list[str] = Field(default_factory=list)


class InterviewPrepResponse(BaseModel):
    """Response for interview prep."""
    job_title: str
    questions: list[InterviewQuestionDTO]


class CoachingTipsRequest(BaseModel):
    """Request for coaching tips."""
    resume_text: str = Field(..., min_length=100)
    job_postings: list[JobPostingInput] = Field(..., min_length=1)
    match_results: list[dict] = Field(default_factory=list)


class CoachingTipsResponse(BaseModel):
    """Response for coaching tips."""
    tips: list[CoachingTipDTO]
