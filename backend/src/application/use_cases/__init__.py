"""Application use cases."""

from .parse_resume import ParseResumeUseCase
from .parse_job_posting import ParseJobPostingUseCase
from .calculate_ats_score import CalculateATSScoreUseCase
from .match_jobs import MatchJobsUseCase
from .generate_interview_prep import GenerateInterviewPrepUseCase
from .generate_coaching_tips import GenerateCoachingTipsUseCase

__all__ = [
    "ParseResumeUseCase",
    "ParseJobPostingUseCase",
    "CalculateATSScoreUseCase",
    "MatchJobsUseCase",
    "GenerateInterviewPrepUseCase",
    "GenerateCoachingTipsUseCase",
]
