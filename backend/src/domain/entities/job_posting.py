"""Job posting entity and related value objects."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class JobRequirement(BaseModel):
    """A single job requirement."""

    skill: str = Field(..., description="Required skill name")
    min_years: Optional[int] = Field(default=None, ge=0, description="Minimum years of experience")
    is_required: bool = Field(default=True, description="True if required, False if nice-to-have")

    class Config:
        frozen = True


class SeniorityLevel(str, Enum):
    """Job seniority level."""
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    STAFF = "staff"
    PRINCIPAL = "principal"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


class RemotePolicy(str, Enum):
    """Remote work policy."""
    ONSITE = "onsite"
    HYBRID = "hybrid"
    REMOTE = "remote"
    UNKNOWN = "unknown"


class JobPosting(BaseModel):
    """Job posting entity parsed from text."""

    id: str = Field(..., description="Unique identifier for the job posting")
    raw_text: str = Field(..., description="Original job posting text")

    # Parsed data
    title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    requirements: list[JobRequirement] = Field(default_factory=list, description="Job requirements")
    preferred_skills: list[str] = Field(default_factory=list, description="Nice-to-have skills")
    keywords: list[str] = Field(default_factory=list, description="Keywords found in posting")
    min_experience_years: int = Field(default=0, ge=0, description="Minimum years of experience")
    education_requirements: list[str] = Field(default_factory=list, description="Required education")

    # Enhanced fields (P1.3)
    seniority_level: Optional[SeniorityLevel] = Field(default=None, description="Detected seniority level")
    remote_policy: RemotePolicy = Field(default=RemotePolicy.UNKNOWN, description="Remote work policy")
    salary_min: Optional[int] = Field(default=None, description="Minimum salary (annual)")
    salary_max: Optional[int] = Field(default=None, description="Maximum salary (annual)")
    salary_currency: str = Field(default="USD", description="Salary currency code")
    location: Optional[str] = Field(default=None, description="Job location")

    def get_required_skills(self) -> set[str]:
        """Get required skill names as a set (lowercase)."""
        return {r.skill.lower() for r in self.requirements if r.is_required}

    def get_all_skills(self) -> set[str]:
        """Get all skill names (required + preferred) as a set (lowercase)."""
        required = {r.skill.lower() for r in self.requirements}
        preferred = {s.lower() for s in self.preferred_skills}
        return required | preferred

    def get_nice_to_have_skills(self) -> set[str]:
        """Get nice-to-have skill names as a set (lowercase)."""
        from_requirements = {r.skill.lower() for r in self.requirements if not r.is_required}
        from_preferred = {s.lower() for s in self.preferred_skills}
        return from_requirements | from_preferred

    def get_display_title(self) -> str:
        """Get a display-friendly job title."""
        if self.title and self.company:
            return f"{self.title} @ {self.company}"
        elif self.title:
            return self.title
        else:
            return "Unknown Position"
