"""Match Jobs Use Case."""

from typing import Optional, List

from src.domain.entities.resume import Resume
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.analysis_result import JobMatch
from src.domain.services.job_matcher import JobMatcher


class MatchJobsUseCase:
    """Use case for matching resume against multiple job postings."""

    def __init__(self, job_matcher: Optional[JobMatcher] = None):
        self.job_matcher = job_matcher or JobMatcher()

    def execute(self, resume: Resume, jobs: list[JobPosting]) -> list[JobMatch]:
        """
        Match resume against all jobs and rank them.

        Args:
            resume: Parsed Resume entity
            jobs: List of parsed JobPosting entities

        Returns:
            List of JobMatch results, sorted by match percentage
        """
        return self.job_matcher.match_all(resume, jobs)
