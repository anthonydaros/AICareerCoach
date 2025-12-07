"""Parse Job Posting Use Case."""

from typing import Any

from src.domain.entities.job_posting import JobPosting, JobRequirement
from src.infrastructure.llm import OpenAIGateway


class ParseJobPostingUseCase:
    """Use case for parsing job posting text into structured data."""

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(self, job_id: str, text: str) -> JobPosting:
        """
        Parse job posting text into structured JobPosting entity.

        Args:
            job_id: Unique identifier for the job
            text: Raw job posting text

        Returns:
            Parsed JobPosting entity
        """
        # Extract structured data using LLM
        extracted = await self.llm_gateway.extract_job_posting(text)

        # Convert to domain entities (use 'or []' to handle None values from LLM)
        requirements = self._parse_requirements(extracted.get("requirements") or [])
        preferred_skills = extracted.get("preferred_skills") or []
        keywords = extracted.get("keywords") or []

        return JobPosting(
            id=job_id,
            raw_text=text,
            title=extracted.get("title"),
            company=extracted.get("company"),
            requirements=requirements,
            preferred_skills=preferred_skills,
            keywords=keywords,
            min_experience_years=int(extracted.get("min_experience_years") or 0),
            education_requirements=extracted.get("education_requirements") or [],
        )

    def _parse_requirements(self, req_data: list[dict[str, Any]]) -> list[JobRequirement]:
        """Parse requirements from extracted data."""
        requirements = []
        for r in req_data:
            if not isinstance(r, dict):
                continue

            skill = r.get("skill", "")
            if not skill:
                continue

            requirements.append(JobRequirement(
                skill=skill,
                min_years=r.get("min_years"),
                is_required=r.get("is_required", True),
            ))

        return requirements
