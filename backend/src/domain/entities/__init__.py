"""Domain entities - Business objects and value objects."""

from .resume import Resume, Skill, Experience, Education, SkillLevel
from .job_posting import JobPosting, JobRequirement
from .analysis_result import (
    ATSResult,
    JobMatch,
    SkillGap,
    InterviewQuestion,
    CoachingTip,
    MatchLevel,
)

__all__ = [
    "Resume",
    "Skill",
    "Experience",
    "Education",
    "SkillLevel",
    "JobPosting",
    "JobRequirement",
    "ATSResult",
    "JobMatch",
    "SkillGap",
    "InterviewQuestion",
    "CoachingTip",
    "MatchLevel",
]
