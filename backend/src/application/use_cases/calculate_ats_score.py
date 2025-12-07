"""Calculate ATS Score Use Case."""

from typing import Optional

from src.domain.entities.resume import Resume
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.analysis_result import ATSResult
from src.domain.services.ats_scorer import ATSScorer


class CalculateATSScoreUseCase:
    """Use case for calculating ATS compatibility score."""

    def __init__(self, ats_scorer: Optional[ATSScorer] = None):
        self.ats_scorer = ats_scorer or ATSScorer()

    def execute(self, resume: Resume, job: JobPosting) -> ATSResult:
        """
        Calculate ATS score for resume against job.

        Args:
            resume: Parsed Resume entity
            job: Parsed JobPosting entity

        Returns:
            ATSResult with score breakdown
        """
        return self.ats_scorer.calculate(resume, job)
