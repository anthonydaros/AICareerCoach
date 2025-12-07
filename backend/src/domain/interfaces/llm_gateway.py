"""LLM Gateway interface - Port for LLM interactions."""

from typing import Protocol, Any


class ILLMGateway(Protocol):
    """Protocol for LLM gateway implementations."""

    async def extract_resume(self, text: str) -> dict[str, Any]:
        """
        Extract structured data from resume text.

        Args:
            text: Raw resume text content

        Returns:
            Dictionary containing:
                - skills: list of skill objects
                - experiences: list of experience objects
                - education: list of education objects
                - certifications: list of strings
                - total_experience_years: float
        """
        ...

    async def extract_job_posting(self, text: str) -> dict[str, Any]:
        """
        Extract structured data from job posting text.

        Args:
            text: Raw job posting text

        Returns:
            Dictionary containing:
                - title: job title
                - company: company name
                - requirements: list of requirement objects
                - preferred_skills: list of strings
                - keywords: list of strings
                - min_experience_years: int
                - education_requirements: list of strings
        """
        ...

    async def generate_interview_questions(
        self,
        resume_summary: str,
        job_summary: str,
        skill_gaps: list[str],
    ) -> list[dict[str, Any]]:
        """
        Generate interview preparation questions.

        Args:
            resume_summary: Summary of candidate's resume
            job_summary: Summary of job requirements
            skill_gaps: List of skills the candidate is missing

        Returns:
            List of question objects containing:
                - question: the question text
                - category: behavioral, technical, or gap-focused
                - why_asked: why interviewer might ask this
                - what_to_say: key points to mention
                - what_to_avoid: things to avoid saying
        """
        ...

    async def generate_coaching_tips(
        self,
        resume_summary: str,
        jobs_summary: str,
        match_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Generate career coaching tips.

        Args:
            resume_summary: Summary of candidate's resume
            jobs_summary: Summary of all job postings
            match_results: List of job match results

        Returns:
            List of coaching tip objects containing:
                - category: quick_win, skill_gap, or strategy
                - title: tip title
                - description: detailed description
                - action_items: list of actionable steps
                - priority: high, medium, or low
        """
        ...

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """
        Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            The assistant's response text
        """
        ...
