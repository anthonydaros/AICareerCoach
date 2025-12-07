"""Analysis result value objects."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MatchLevel(str, Enum):
    """Job match quality level."""
    EXCELLENT = "excellent"  # 80-100%
    GOOD = "good"           # 60-79%
    FAIR = "fair"           # 40-59%
    POOR = "poor"           # 0-39%


class KeywordWeight(str, Enum):
    """Keyword importance weight levels."""
    CRITICAL = "critical"   # Must-have skills
    HIGH = "high"           # Strongly preferred
    MEDIUM = "medium"       # Nice to have
    LOW = "low"             # Minor boost


class KeywordAnalysis(BaseModel):
    """Detailed keyword analysis with weight and observation."""

    keyword: str = Field(..., description="The keyword being analyzed")
    found_in_resume: bool = Field(..., description="Whether keyword was found in resume")
    weight: KeywordWeight = Field(..., description="Importance weight of keyword")
    observation: str = Field(..., description="Analysis observation for this keyword")

    class Config:
        frozen = True


class ATSResult(BaseModel):
    """ATS score breakdown with detailed analysis."""

    total_score: float = Field(..., ge=0, le=100, description="Total ATS score (0-100)")
    skill_score: float = Field(..., ge=0, description="Score for skill match (max 40)")
    experience_score: float = Field(..., ge=0, description="Score for experience (max 30)")
    education_score: float = Field(..., ge=0, description="Score for education (max 15)")
    certification_score: float = Field(..., ge=0, description="Score for certifications (max 10)")
    keyword_score: float = Field(..., ge=0, description="Score for keyword optimization (max 5)")
    matched_keywords: list[str] = Field(default_factory=list, description="Keywords found in resume")
    missing_keywords: list[str] = Field(default_factory=list, description="Keywords missing from resume")
    format_issues: list[str] = Field(default_factory=list, description="Format problems detected")
    improvement_suggestions: list[str] = Field(default_factory=list, description="Actionable improvements")

    # Enhanced fields for detailed report
    keyword_analysis: list[KeywordAnalysis] = Field(
        default_factory=list,
        description="Detailed analysis of each keyword with weights"
    )
    score_calculation: str = Field(
        default="",
        description="Formula explanation of how score was calculated"
    )
    methodology: str = Field(
        default="",
        description="Explanation of ATS scoring methodology"
    )

    class Config:
        frozen = True

    def get_level(self) -> str:
        """Get score level as a string."""
        if self.total_score >= 80:
            return "Excellent"
        elif self.total_score >= 60:
            return "Good"
        elif self.total_score >= 40:
            return "Fair"
        else:
            return "Poor"


class SkillGap(BaseModel):
    """A skill gap between resume and job."""

    skill: str = Field(..., description="Missing skill name")
    is_required: bool = Field(default=True, description="Whether the skill is required or nice-to-have")
    suggestion: str = Field(..., description="Actionable suggestion to address the gap")
    learning_resources: list[str] = Field(default_factory=list, description="Resources to learn this skill")

    class Config:
        frozen = True


class RequirementMatch(BaseModel):
    """Individual requirement match analysis."""

    requirement: str = Field(..., description="The job requirement being evaluated")
    candidate_experience: str = Field(..., description="Candidate's relevant experience")
    match_percentage: int = Field(..., ge=0, le=100, description="Match percentage for this requirement")
    logic: str = Field(..., description="Explanation of the match logic")

    class Config:
        frozen = True


class JobMatch(BaseModel):
    """Match result between resume and a job."""

    job_id: str = Field(..., description="Job posting ID")
    job_title: str = Field(..., description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    match_percentage: float = Field(..., ge=0, le=100, description="Match percentage (0-100)")
    match_level: MatchLevel = Field(..., description="Match quality level")
    matched_skills: list[str] = Field(default_factory=list, description="Skills that matched")
    missing_skills: list[str] = Field(default_factory=list, description="Skills that are missing")
    skill_gaps: list[SkillGap] = Field(default_factory=list, description="Detailed skill gaps")
    strengths: list[str] = Field(default_factory=list, description="Candidate strengths for this job")
    concerns: list[str] = Field(default_factory=list, description="Concerns or weaknesses")
    is_best_fit: bool = Field(default=False, description="Whether this is the best matching job")

    # Enhanced fields for detailed report
    requirement_matrix: list[RequirementMatch] = Field(
        default_factory=list,
        description="Detailed requirement-by-requirement match analysis"
    )
    weighted_calculation: str = Field(
        default="",
        description="Formula explanation of how match was calculated"
    )
    transferable_skills: list[str] = Field(
        default_factory=list,
        description="Skills that transfer well to this role"
    )

    class Config:
        frozen = True


class StarMethod(BaseModel):
    """STAR method guidance for behavioral questions."""

    situation: str = Field(..., description="How to frame the situation")
    task: str = Field(..., description="How to describe your task/responsibility")
    action: str = Field(..., description="How to explain your actions")
    result: str = Field(..., description="How to present the results")

    class Config:
        frozen = True


class InterviewQuestion(BaseModel):
    """Interview prep question with enhanced guidance."""

    question: str = Field(..., description="The interview question")
    category: str = Field(..., description="Category: screening, technical, behavioral, or curveball")
    why_asked: str = Field(..., description="What the interviewer is seeking to evaluate")
    what_to_say: list[str] = Field(default_factory=list, description="Key points to mention")
    what_to_avoid: list[str] = Field(default_factory=list, description="Things to avoid saying")

    # Enhanced fields
    your_angle: str = Field(
        default="",
        description="How to approach this question given your background"
    )
    star_guidance: Optional[StarMethod] = Field(
        default=None,
        description="STAR method guidance for behavioral questions"
    )

    class Config:
        frozen = True


class GapImpact(str, Enum):
    """Gap impact severity levels."""
    ELIMINATORY = "eliminatory"  # Disqualifying gap
    HIGH = "high"                # Significant concern
    MEDIUM = "medium"            # Moderate concern
    LOW = "low"                  # Minor concern


class GapAnalysis(BaseModel):
    """Detailed gap analysis with action recommendations."""

    gap: str = Field(..., description="The identified gap")
    impact: GapImpact = Field(..., description="Impact level of this gap")
    action: str = Field(..., description="Recommended action to address gap")
    priority: int = Field(..., ge=1, le=5, description="Priority rank (1=highest)")

    class Config:
        frozen = True


class CoachingTip(BaseModel):
    """Career coaching tip with enhanced analysis."""

    category: str = Field(..., description="Category: quick_win, skill_gap, or strategy")
    title: str = Field(..., description="Tip title")
    description: str = Field(..., description="Detailed description")
    action_items: list[str] = Field(default_factory=list, description="Actionable steps")
    priority: str = Field(default="medium", description="Priority: high, medium, or low")

    class Config:
        frozen = True


class CoachingResult(BaseModel):
    """Enhanced coaching result with gap analysis."""

    tips: list[CoachingTip] = Field(default_factory=list, description="Coaching tips")
    gap_analysis: list[GapAnalysis] = Field(
        default_factory=list,
        description="Detailed gap analysis with prioritized actions"
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
        description="Alternative career paths or roles to consider"
    )

    class Config:
        frozen = True


class InterviewPrep(BaseModel):
    """Enhanced interview preparation result."""

    questions: list[InterviewQuestion] = Field(default_factory=list, description="Interview questions")
    questions_by_category: dict[str, list[InterviewQuestion]] = Field(
        default_factory=dict,
        description="Questions organized by category"
    )
    preparation_tips: list[str] = Field(
        default_factory=list,
        description="General preparation tips"
    )
    questions_to_ask_interviewer: list[str] = Field(
        default_factory=list,
        description="Smart questions candidate should ask"
    )

    class Config:
        frozen = True
