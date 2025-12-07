"""Generate Coaching Tips Use Case."""

from typing import Any

from src.domain.entities.analysis_result import CoachingTip
from src.infrastructure.llm import OpenAIGateway


class GenerateCoachingTipsUseCase:
    """Use case for generating career coaching tips."""

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(
        self,
        resume_summary: str,
        jobs_summary: str,
        match_results: list[dict[str, Any]],
    ) -> list[CoachingTip]:
        """
        Generate career coaching tips.

        Args:
            resume_summary: Summary of candidate's resume
            jobs_summary: Summary of all job postings
            match_results: List of job match results

        Returns:
            List of CoachingTip entities
        """
        # Generate tips using LLM
        tips_data = await self.llm_gateway.generate_coaching_tips(
            resume_summary=resume_summary,
            jobs_summary=jobs_summary,
            match_results=match_results,
        )

        # Convert to domain entities
        return self._parse_tips(tips_data)

    def _parse_tips(self, tips_data: list[dict[str, Any]]) -> list[CoachingTip]:
        """Parse tips from LLM response."""
        tips = []
        for t in tips_data:
            if not isinstance(t, dict):
                continue

            title = t.get("title", "")
            if not title:
                continue

            tips.append(CoachingTip(
                category=t.get("category", "general"),
                title=title,
                description=t.get("description", ""),
                action_items=t.get("action_items", []),
                priority=t.get("priority", "medium"),
            ))

        return tips
