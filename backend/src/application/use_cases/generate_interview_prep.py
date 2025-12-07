"""Generate Interview Prep Use Case."""

from typing import Any

from src.domain.entities.analysis_result import InterviewQuestion
from src.infrastructure.llm import OpenAIGateway


class GenerateInterviewPrepUseCase:
    """Use case for generating interview preparation questions."""

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(
        self,
        resume_summary: str,
        job_summary: str,
        skill_gaps: list[str],
    ) -> list[InterviewQuestion]:
        """
        Generate interview preparation questions.

        Args:
            resume_summary: Summary of candidate's resume
            job_summary: Summary of job requirements
            skill_gaps: List of skills the candidate is missing

        Returns:
            List of InterviewQuestion entities
        """
        # Generate questions using LLM
        questions_data = await self.llm_gateway.generate_interview_questions(
            resume_summary=resume_summary,
            job_summary=job_summary,
            skill_gaps=skill_gaps,
        )

        # Convert to domain entities
        return self._parse_questions(questions_data)

    def _parse_questions(self, questions_data: list[dict[str, Any]]) -> list[InterviewQuestion]:
        """Parse questions from LLM response."""
        questions = []
        for q in questions_data:
            if not isinstance(q, dict):
                continue

            question_text = q.get("question", "")
            if not question_text:
                continue

            questions.append(InterviewQuestion(
                question=question_text,
                category=q.get("category", "general"),
                why_asked=q.get("why_asked", ""),
                what_to_say=q.get("what_to_say", []),
                what_to_avoid=q.get("what_to_avoid", []),
            ))

        return questions
