"""Job posting-related DTOs."""

from typing import Optional
from pydantic import BaseModel, Field


class JobPostingInput(BaseModel):
    """Input for job posting processing."""
    id: str = Field(..., description="Unique identifier for the job")
    text: str = Field(..., min_length=50, description="Job posting text content")


class JobRequirementDTO(BaseModel):
    """Job requirement data transfer object."""
    skill: str
    min_years: Optional[int] = None
    is_required: bool = True


class ParsedJobDTO(BaseModel):
    """Parsed job posting data transfer object."""
    id: str
    raw_text: str
    title: Optional[str] = None
    company: Optional[str] = None
    requirements: list[JobRequirementDTO] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    min_experience_years: int = 0
    education_requirements: list[str] = Field(default_factory=list)

    def get_summary(self) -> str:
        """Get a text summary of the job posting."""
        parts = []

        if self.title:
            title_part = self.title
            if self.company:
                title_part += f" at {self.company}"
            parts.append(title_part)

        required_skills = [r.skill for r in self.requirements if r.is_required]
        if required_skills:
            parts.append(f"Required: {', '.join(required_skills[:5])}")

        if self.preferred_skills:
            parts.append(f"Preferred: {', '.join(self.preferred_skills[:3])}")

        if self.min_experience_years > 0:
            parts.append(f"Min experience: {self.min_experience_years} years")

        return "; ".join(parts) if parts else "No structured data extracted"

    def get_display_title(self) -> str:
        """Get a display-friendly job title."""
        if self.title and self.company:
            return f"{self.title} @ {self.company}"
        elif self.title:
            return self.title
        else:
            return "Unknown Position"
