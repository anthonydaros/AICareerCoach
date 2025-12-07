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


class ATSResult(BaseModel):
    """ATS score breakdown."""

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

    class Config:
        frozen = True


class InterviewQuestion(BaseModel):
    """Interview prep question."""

    question: str = Field(..., description="The interview question")
    category: str = Field(..., description="Category: behavioral, technical, or gap-focused")
    why_asked: str = Field(..., description="Why the interviewer might ask this")
    what_to_say: list[str] = Field(default_factory=list, description="Key points to mention")
    what_to_avoid: list[str] = Field(default_factory=list, description="Things to avoid saying")

    class Config:
        frozen = True


class CoachingTip(BaseModel):
    """Career coaching tip."""

    category: str = Field(..., description="Category: quick_win, skill_gap, or strategy")
    title: str = Field(..., description="Tip title")
    description: str = Field(..., description="Detailed description")
    action_items: list[str] = Field(default_factory=list, description="Actionable steps")
    priority: str = Field(default="medium", description="Priority: high, medium, or low")

    class Config:
        frozen = True
