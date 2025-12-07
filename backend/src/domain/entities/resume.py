"""Resume entity and related value objects."""

import re
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# Email validation pattern
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# LinkedIn URL pattern
LINKEDIN_PATTERN = re.compile(
    r'^(https?://)?(www\.)?linkedin\.com/in/[\w-]+/?$',
    re.IGNORECASE
)


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
    start_year: Optional[int] = Field(default=None, description="Start year (e.g., 2021)")
    end_year: Optional[int] = Field(default=None, description="End year (None = current job)")

    @field_validator('start_year', 'end_year', mode='before')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """Validate year is reasonable (1950-2030)."""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                return None
        if 1950 <= v <= 2030:
            return v
        return None

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

    # Contact information (P1.1)
    name: Optional[str] = Field(default=None, description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    linkedin_url: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    location: Optional[str] = Field(default=None, description="City, State/Country")

    # Extracted data
    skills: list[Skill] = Field(default_factory=list, description="Extracted skills")
    experiences: list[Experience] = Field(default_factory=list, description="Work experience entries")
    education: list[Education] = Field(default_factory=list, description="Education entries")
    certifications: list[str] = Field(default_factory=list, description="Certifications held")
    total_experience_years: float = Field(default=0.0, ge=0, description="Total years of experience")

    # Metadata
    filename: Optional[str] = Field(default=None, description="Original filename")

    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean email address."""
        if v is None or v == "":
            return None
        v = v.strip().lower()
        if EMAIL_PATTERN.match(v):
            return v
        # Try to extract email from text (fallback)
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', v)
        if match:
            return match.group(0).lower()
        return None  # Invalid email, set to None instead of raising

    @field_validator('linkedin_url', mode='before')
    @classmethod
    def validate_linkedin(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize LinkedIn URL."""
        if v is None or v == "":
            return None
        v = v.strip()
        # Normalize URL
        if not v.startswith(('http://', 'https://')):
            if 'linkedin.com' in v.lower():
                v = 'https://' + v.lstrip('/')
        if LINKEDIN_PATTERN.match(v):
            return v
        # Try to extract LinkedIn from text
        match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+', v, re.IGNORECASE)
        if match:
            url = match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            return url
        return None  # Invalid LinkedIn, set to None instead of raising

    @field_validator('phone', mode='before')
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone number format."""
        if v is None or v == "":
            return None
        # Remove common separators and normalize
        v = re.sub(r'[\s\-\.\(\)]', '', v.strip())
        # Basic validation: should contain mostly digits
        digits = re.sub(r'\D', '', v)
        if len(digits) >= 8:  # Minimum phone length
            return v
        return None

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
