"""Resume-related DTOs."""

from typing import Optional
from pydantic import BaseModel, Field


class ResumeInput(BaseModel):
    """Input for resume processing."""
    text: str = Field(..., min_length=50, description="Resume text content")
    filename: Optional[str] = Field(default=None, description="Original filename")


class SkillDTO(BaseModel):
    """Skill data transfer object."""
    name: str
    normalized_name: str
    level: str
    years_experience: Optional[float] = None


class ExperienceDTO(BaseModel):
    """Experience data transfer object."""
    title: str
    company: str
    duration_months: int
    description: str = ""
    skills_used: list[str] = Field(default_factory=list)


class EducationDTO(BaseModel):
    """Education data transfer object."""
    degree: str
    field: str
    institution: str
    year: Optional[int] = None


class ParsedResumeDTO(BaseModel):
    """Parsed resume data transfer object."""
    id: str
    raw_content: str
    skills: list[SkillDTO] = Field(default_factory=list)
    experiences: list[ExperienceDTO] = Field(default_factory=list)
    education: list[EducationDTO] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    total_experience_years: float = 0.0
    filename: Optional[str] = None

    def get_summary(self) -> str:
        """Get a text summary of the resume."""
        parts = []

        if self.total_experience_years > 0:
            parts.append(f"{self.total_experience_years:.0f} years of experience")

        if self.skills:
            skill_names = [s.normalized_name for s in self.skills[:5]]
            parts.append(f"Skills: {', '.join(skill_names)}")

        if self.experiences:
            exp = self.experiences[0]
            parts.append(f"Most recent: {exp.title} at {exp.company}")

        if self.education:
            edu = self.education[0]
            parts.append(f"Education: {edu.degree} in {edu.field}")

        if self.certifications:
            parts.append(f"Certifications: {', '.join(self.certifications[:3])}")

        return "; ".join(parts) if parts else "No structured data extracted"
