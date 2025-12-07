"""API request schemas."""

from pydantic import BaseModel, Field


class JobPostingInput(BaseModel):
    """Job posting input for analysis."""
    id: str = Field(..., description="Unique identifier for the job posting")
    text: str = Field(..., min_length=50, description="Job posting text content")


class AnalyzeRequest(BaseModel):
    """Request for full career analysis."""
    resume_text: str = Field(
        ...,
        min_length=100,
        description="Resume text content"
    )
    job_postings: list[JobPostingInput] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="List of job postings to analyze against"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "John Doe\nSenior Python Developer\n5 years of experience with Python, FastAPI, AWS...",
                "job_postings": [
                    {
                        "id": "job1",
                        "text": "Senior Python Developer at TechCorp\nRequirements: 5+ years Python, FastAPI, AWS..."
                    }
                ]
            }
        }


class ATSScoreRequest(BaseModel):
    """Request for ATS score calculation only."""
    resume_text: str = Field(..., min_length=100, description="Resume text content")
    job_text: str = Field(..., min_length=50, description="Job posting text content")


class MatchJobsRequest(BaseModel):
    """Request for job matching."""
    resume_text: str = Field(..., min_length=100, description="Resume text content")
    job_postings: list[JobPostingInput] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="List of job postings to match against"
    )


class InterviewPrepRequest(BaseModel):
    """Request for interview prep generation."""
    resume_text: str = Field(..., min_length=100, description="Resume text content")
    job_text: str = Field(..., min_length=50, description="Job posting text content")
    skill_gaps: list[str] = Field(
        default_factory=list,
        description="Known skill gaps to focus on"
    )


class CoachingTipsRequest(BaseModel):
    """Request for career coaching tips."""
    resume_text: str = Field(..., min_length=100, description="Resume text content")
    job_postings: list[JobPostingInput] = Field(
        ...,
        min_length=1,
        description="List of target job postings"
    )
    match_results: list[dict] = Field(
        default_factory=list,
        description="Optional pre-computed match results"
    )
