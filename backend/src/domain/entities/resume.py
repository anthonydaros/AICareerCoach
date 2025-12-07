"""Resume entity and related value objects."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SkillLevel(str, Enum):
    """Skill proficiency level."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(BaseModel):
    """Normalized skill extracted from resume."""

    name: str = Field(..., description="Original skill name as found in resume")
    normalized_name: str = Field(..., description="Normalized/standardized skill name")
    level: SkillLevel = Field(default=SkillLevel.INTERMEDIATE, description="Proficiency level")
    years_experience: Optional[float] = Field(default=None, description="Years of experience with this skill")

    class Config:
        frozen = True


class Experience(BaseModel):
    """Work experience entry."""

    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    duration_months: int = Field(..., ge=0, description="Duration in months")
    description: str = Field(default="", description="Role description")
    skills_used: list[str] = Field(default_factory=list, description="Skills used in this role")

    class Config:
        frozen = True


class Education(BaseModel):
    """Education entry."""

    degree: str = Field(..., description="Degree name (e.g., Bachelor's, Master's)")
    field: str = Field(..., description="Field of study")
    institution: str = Field(..., description="Educational institution name")
    year: Optional[int] = Field(default=None, description="Graduation year")

    class Config:
        frozen = True


class Resume(BaseModel):
    """Resume aggregate root - represents parsed resume data."""

    id: str = Field(..., description="Unique identifier for the resume")
    raw_content: str = Field(..., description="Original text content of the resume")

    # Extracted data
    skills: list[Skill] = Field(default_factory=list, description="Extracted skills")
    experiences: list[Experience] = Field(default_factory=list, description="Work experience entries")
    education: list[Education] = Field(default_factory=list, description="Education entries")
    certifications: list[str] = Field(default_factory=list, description="Certifications held")
    total_experience_years: float = Field(default=0.0, ge=0, description="Total years of experience")

    # Metadata
    filename: Optional[str] = Field(default=None, description="Original filename")

    def get_skill_names(self) -> set[str]:
        """Get normalized skill names as a set (lowercase)."""
        return {s.normalized_name.lower() for s in self.skills}

    def get_skill_names_original(self) -> set[str]:
        """Get original skill names as a set."""
        return {s.name for s in self.skills}

    def has_skill(self, skill_name: str) -> bool:
        """Check if resume contains a specific skill."""
        return skill_name.lower() in self.get_skill_names()

    def get_experience_summary(self) -> str:
        """Get a summary of work experience."""
        if not self.experiences:
            return "No work experience listed"

        summaries = []
        for exp in self.experiences[:3]:  # Top 3 experiences
            years = exp.duration_months / 12
            summaries.append(f"{exp.title} at {exp.company} ({years:.1f} years)")

        return "; ".join(summaries)
