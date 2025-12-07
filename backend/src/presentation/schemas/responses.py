"""API response schemas."""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str = "AI Career Coach Backend"


# ============= ATS Enhanced Schemas =============

class KeywordWeight(str, Enum):
    """Keyword weight levels for ATS analysis."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class KeywordAnalysisResponse(BaseModel):
    """Detailed keyword analysis for ATS scoring."""
    keyword: str = Field(..., description="The keyword being analyzed")
    found_in_resume: bool = Field(..., description="Whether keyword was found")
    weight: KeywordWeight = Field(..., description="Importance weight of this keyword")
    observation: str = Field(..., description="Analysis observation for this keyword")


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
    # Enhanced fields
    keyword_analysis: list[KeywordAnalysisResponse] = Field(
        default_factory=list,
        description="Detailed keyword-by-keyword analysis with weights"
    )
    score_calculation: str = Field(
        default="",
        description="Human-readable score calculation breakdown"
    )
    methodology: str = Field(
        default="",
        description="Explanation of ATS scoring methodology"
    )


class SkillGapResponse(BaseModel):
    """Skill gap response."""
    skill: str
    is_required: bool
    suggestion: str
    learning_resources: list[str] = Field(default_factory=list)


# ============= Job Match Enhanced Schemas =============

class RequirementMatchResponse(BaseModel):
    """Requirement-by-requirement match analysis."""
    requirement: str = Field(..., description="The job requirement")
    candidate_experience: str = Field(..., description="Candidate's relevant experience")
    match_percentage: int = Field(..., ge=0, le=100, description="Match percentage for this requirement")
    logic: str = Field(..., description="Explanation of match logic")


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
    # Enhanced fields
    requirement_matrix: list[RequirementMatchResponse] = Field(
        default_factory=list,
        description="Requirement-by-requirement match analysis"
    )
    weighted_calculation: str = Field(
        default="",
        description="Human-readable match calculation formula"
    )
    transferable_skills: list[str] = Field(
        default_factory=list,
        description="Skills that transfer well to the target role"
    )


class BestFitResponse(BaseModel):
    """Best fit recommendation response."""
    job_id: str
    job_title: str
    match_percentage: float
    recommendation: str


# ============= Seniority Enhanced Schemas =============

class SeniorityScoresResponse(BaseModel):
    """Seniority score breakdown."""
    experience: float = Field(..., ge=0, le=1)
    complexity: float = Field(..., ge=0, le=1)
    autonomy: float = Field(..., ge=0, le=1)
    skills: float = Field(..., ge=0, le=1)
    leadership: float = Field(..., ge=0, le=1)
    impact: float = Field(..., ge=0, le=1)


class SeniorityAxisResponse(BaseModel):
    """Axis-by-axis seniority comparison."""
    axis: str = Field(..., description="The seniority axis (e.g., experience, complexity)")
    candidate_level: str = Field(..., description="Candidate's level on this axis")
    evidence: str = Field(..., description="Evidence supporting this assessment")
    job_expected_level: str = Field(..., description="Job's expected level for this axis")


class SeniorityResponse(BaseModel):
    """Detected seniority level response."""
    level: str = Field(..., description="Seniority level: junior, mid, or senior")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    years_experience: float = Field(..., ge=0, description="Total years of experience")
    scores: SeniorityScoresResponse = Field(..., description="Breakdown of scoring criteria")
    indicators: list[str] = Field(default_factory=list, description="Reasons for classification")
    # Enhanced fields
    axis_comparison: list[SeniorityAxisResponse] = Field(
        default_factory=list,
        description="Axis-by-axis comparison of candidate vs job requirements"
    )
    job_fit_assessment: str = Field(
        default="",
        description="Overall assessment of candidate-job seniority fit"
    )
    gap_analysis: str = Field(
        default="",
        description="Analysis of seniority gaps to address"
    )
    seniority_match: str = Field(
        default="",
        description="Match status: under-qualified, match, or over-qualified"
    )


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


# ============= Interview Prep Enhanced Schemas =============

class StarMethodResponse(BaseModel):
    """STAR method guidance for behavioral questions."""
    situation: str = Field(..., description="How to describe the situation")
    task: str = Field(..., description="How to describe your task/responsibility")
    action: str = Field(..., description="How to describe your actions")
    result: str = Field(..., description="How to describe the outcome")


class InterviewQuestionResponse(BaseModel):
    """Interview question response."""
    question: str
    category: str
    why_asked: str
    what_to_say: list[str] = Field(default_factory=list)
    what_to_avoid: list[str] = Field(default_factory=list)
    # Enhanced fields
    your_angle: str = Field(
        default="",
        description="How to approach this question based on your background"
    )
    star_guidance: Optional[StarMethodResponse] = Field(
        default=None,
        description="STAR method guidance for behavioral questions"
    )


class InterviewPrepResponse(BaseModel):
    """Interview prep response."""
    job_title: str
    questions: list[InterviewQuestionResponse]
    # Enhanced fields
    questions_by_category: dict[str, list[InterviewQuestionResponse]] = Field(
        default_factory=dict,
        description="Questions organized by category (screening, technical, behavioral, curveball)"
    )
    preparation_tips: list[str] = Field(
        default_factory=list,
        description="General preparation tips for the interview"
    )
    questions_to_ask_interviewer: list[str] = Field(
        default_factory=list,
        description="Questions the candidate should ask the interviewer"
    )


# ============= Coaching Enhanced Schemas =============

class CoachingTipResponse(BaseModel):
    """Coaching tip response."""
    category: str
    title: str
    description: str
    action_items: list[str] = Field(default_factory=list)
    priority: str = "medium"


class GapImpact(str, Enum):
    """Gap impact levels."""
    ELIMINATORY = "eliminatory"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GapAnalysisResponse(BaseModel):
    """Gap analysis with action mapping."""
    gap: str = Field(..., description="The identified gap")
    impact: GapImpact = Field(..., description="Impact level of this gap")
    action: str = Field(..., description="Recommended action to address the gap")
    priority: int = Field(..., ge=1, description="Priority order (1 = highest)")


class CoachingTipsResponse(BaseModel):
    """Coaching tips response."""
    tips: list[CoachingTipResponse]
    # Enhanced fields
    gap_analysis: list[GapAnalysisResponse] = Field(
        default_factory=list,
        description="Prioritized gap analysis with action mapping"
    )
    success_probability: str = Field(
        default="",
        description="Estimated success probability range (e.g., '30-50%')"
    )
    honest_recommendation: str = Field(
        default="",
        description="Honest assessment and recommendation"
    )
    alternative_paths: list[str] = Field(
        default_factory=list,
        description="Alternative career paths if current match is low"
    )


# ============= Main Analysis Response =============

class SimpleInterviewPrepResponse(BaseModel):
    """Simplified interview prep for main analysis response."""
    job_title: Optional[str] = None
    questions: list[InterviewQuestionResponse] = Field(default_factory=list)


class SimpleCoachingTipsResponse(BaseModel):
    """Simplified coaching tips for main analysis response."""
    tips: list[CoachingTipResponse] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    """Full analysis response."""
    ats_result: ATSResultResponse
    job_matches: list[JobMatchResponse]
    best_fit: Optional[BestFitResponse] = None
    seniority: Optional[SeniorityResponse] = None
    stability: Optional[StabilityResponse] = None
    interview_prep: Optional[SimpleInterviewPrepResponse] = None
    coaching_tips: Optional[SimpleCoachingTipsResponse] = None


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    error_type: Optional[str] = None
