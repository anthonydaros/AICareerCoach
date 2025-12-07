"""Data Transfer Objects for application layer."""

from .resume_dto import ResumeInput, ParsedResumeDTO
from .job_dto import JobPostingInput, ParsedJobDTO
from .analysis_dto import AnalyzeRequest, AnalyzeResponse, BestFitDTO

__all__ = [
    "ResumeInput",
    "ParsedResumeDTO",
    "JobPostingInput",
    "ParsedJobDTO",
    "AnalyzeRequest",
    "AnalyzeResponse",
    "BestFitDTO",
]
