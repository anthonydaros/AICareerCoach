"""OpenAI SDK Gateway - Implementation pointing to Ollama."""

import json
import logging
from typing import Any

from openai import AsyncOpenAI

from src.config import get_settings
from src.infrastructure.llm.prompts import (
    RESUME_EXTRACTION_PROMPT,
    RESUME_EXTRACTION_SYSTEM,
    JOB_EXTRACTION_PROMPT,
    JOB_EXTRACTION_SYSTEM,
    INTERVIEW_GENERATION_PROMPT,
    INTERVIEW_GENERATION_SYSTEM,
    COACHING_GENERATION_PROMPT,
    COACHING_GENERATION_SYSTEM,
)

logger = logging.getLogger(__name__)


class OpenAIGateway:
    """
    LLM Gateway using OpenAI SDK pointing to Ollama.

    This implementation uses the OpenAI Python SDK configured to
    communicate with an Ollama server via its OpenAI-compatible API.
    """

    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout,
        )
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """
        Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            The assistant's response text
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    async def _chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        """
        Send a chat request expecting JSON response.

        Args:
            system_prompt: System message for context
            user_prompt: User message with the request

        Returns:
            Parsed JSON response as dictionary
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        content = response.choices[0].message.content

        # Try to parse JSON from response
        try:
            # Handle potential markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            return json.loads(content.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Raw response: {content}")
            # Return empty structure on parse failure
            return {}

    async def extract_resume(self, text: str) -> dict[str, Any]:
        """
        Extract structured data from resume text.

        Args:
            text: Raw resume text content

        Returns:
            Dictionary with extracted resume data
        """
        prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=text)
        result = await self._chat_json(RESUME_EXTRACTION_SYSTEM, prompt)

        # Ensure required fields exist with defaults (use 'or' to handle None values)
        return {
            "skills": result.get("skills") or [],
            "experiences": result.get("experiences") or [],
            "education": result.get("education") or [],
            "certifications": result.get("certifications") or [],
            "total_experience_years": result.get("total_experience_years") or 0.0,
        }

    async def extract_job_posting(self, text: str) -> dict[str, Any]:
        """
        Extract structured data from job posting text.

        Args:
            text: Raw job posting text

        Returns:
            Dictionary with extracted job data
        """
        prompt = JOB_EXTRACTION_PROMPT.format(job_text=text)
        result = await self._chat_json(JOB_EXTRACTION_SYSTEM, prompt)

        # Ensure required fields exist with defaults (use 'or' to handle None values)
        return {
            "title": result.get("title"),
            "company": result.get("company"),
            "requirements": result.get("requirements") or [],
            "preferred_skills": result.get("preferred_skills") or [],
            "keywords": result.get("keywords") or [],
            "min_experience_years": result.get("min_experience_years") or 0,
            "education_requirements": result.get("education_requirements") or [],
        }

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
            List of question objects
        """
        gaps_text = ", ".join(skill_gaps) if skill_gaps else "None identified"

        prompt = INTERVIEW_GENERATION_PROMPT.format(
            resume_summary=resume_summary,
            job_requirements=job_summary,
            skill_gaps=gaps_text,
        )

        result = await self._chat_json(INTERVIEW_GENERATION_SYSTEM, prompt)

        # Handle both list response and dict with questions key
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and "questions" in result:
            return result["questions"]
        else:
            return []

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
            List of coaching tip objects
        """
        # Format match results for prompt
        match_text = "\n".join(
            f"- {m.get('job_title', 'Unknown')}: {m.get('match_percentage', 0):.0f}% match"
            for m in match_results
        )

        prompt = COACHING_GENERATION_PROMPT.format(
            resume_summary=resume_summary,
            jobs_summary=jobs_summary,
            match_results=match_text or "No match results available",
        )

        result = await self._chat_json(COACHING_GENERATION_SYSTEM, prompt)

        # Handle both list response and dict with tips key
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and "tips" in result:
            return result["tips"]
        else:
            return []
