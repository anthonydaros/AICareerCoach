"""OpenAI SDK Gateway - Compatible with OpenRouter, Ollama, or OpenAI."""

import json
import logging
from typing import Any, Optional, Union

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
from src.infrastructure.llm.prompts.interview_generation import SENIORITY_CONTEXT

logger = logging.getLogger(__name__)


class OpenAIGateway:
    """
    LLM Gateway using OpenAI SDK.

    This implementation uses the OpenAI Python SDK configured to
    communicate with OpenRouter, Ollama, or OpenAI directly.
    """

    def __init__(self):
        settings = get_settings()

        # Build default headers for OpenRouter (optional but recommended)
        default_headers = {}
        if settings.openrouter_app_url:
            default_headers["HTTP-Referer"] = settings.openrouter_app_url
        if settings.openrouter_app_name:
            default_headers["X-Title"] = settings.openrouter_app_name

        self.client = AsyncOpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout,
            default_headers=default_headers if default_headers else None,
        )
        self.model = settings.openai_model
        self.fallback_model = settings.openai_fallback_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

        # Google Gemini fallback (direct API, bypasses OpenRouter rate limits)
        self.gemini_api_key = settings.gemini_api_key
        self.gemini_model = settings.gemini_model

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

    async def _try_gemini_json_response(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> Union[dict[str, Any], list[Any], None]:
        """
        Fallback using Google Gemini API directly (bypasses OpenRouter rate limits).

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Temperature for generation
            max_tokens: Max output tokens

        Returns:
            Parsed JSON response, or None if failed
        """
        if not self.gemini_api_key:
            logger.warning("Gemini API key not configured, skipping Gemini fallback")
            return None

        try:
            import google.generativeai as genai
            import re

            genai.configure(api_key=self.gemini_api_key)

            # Convert OpenAI messages to Gemini format
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
            user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")

            # Create model with system instruction for better context
            model = genai.GenerativeModel(
                self.gemini_model,
                system_instruction=system_msg,
            )

            logger.info(f"[Gemini] Calling {self.gemini_model} directly")

            response = await model.generate_content_async(
                user_msg,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json",
                ),
            )

            content = response.text or ""

            if not content.strip():
                logger.warning("[Gemini] Returned empty response")
                return None

            logger.debug(f"[Gemini] Raw response (first 500 chars): {content[:500]}")

            # Extract JSON content
            json_content = self._extract_json(content)

            # Fix common JSON issues from LLMs
            # Remove trailing commas before ] or }
            json_content = re.sub(r',(\s*[\]}])', r'\1', json_content)
            # Fix newlines inside string values (replace with \n)
            json_content = re.sub(r'(?<!\\)\n(?=[^"]*"[^"]*(?:"[^"]*"[^"]*)*$)', r'\\n', json_content)
            # Replace single quotes with double quotes for keys (careful approach)
            json_content = re.sub(r"(?<=[{,\s])'([^']+)'(?=\s*:)", r'"\1"', json_content)

            try:
                result = json.loads(json_content)
            except json.JSONDecodeError as e:
                # Try one more fix: remove any control characters
                try:
                    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_content)
                    result = json.loads(cleaned)
                    logger.info("[Gemini] Successfully parsed JSON after cleanup")
                except json.JSONDecodeError:
                    logger.warning(f"[Gemini] JSON parse error: {e}")
                    logger.debug(f"[Gemini] Raw content that failed: {content[:2000]}")
                    return None

            if result and (isinstance(result, list) or any(result.values())):
                logger.info("[Gemini] Successfully parsed JSON response")
                return result
            else:
                logger.warning("[Gemini] Returned empty JSON structure")
                return None

        except ImportError:
            logger.error("[Gemini] google-generativeai package not installed")
            return None
        except Exception as e:
            logger.error(f"[Gemini] API call failed: {e}")
            return None

    async def _try_chat_json_with_model(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> Union[dict[str, Any], list[Any], None]:
        """
        Try to get JSON response from a specific model.

        Returns:
            Parsed JSON, or None if failed/empty
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content or ""

            # Debug log the raw response
            logger.debug(f"[{model}] Raw response (first 500 chars): {content[:500]}")

            # Empty response check
            if not content.strip():
                logger.warning(f"[{model}] Returned empty response")
                return None

            # Try multiple JSON extraction strategies
            json_content = self._extract_json(content)

            try:
                result = json.loads(json_content)
                # Check if result is meaningfully non-empty
                if result and (isinstance(result, list) or any(result.values())):
                    logger.info(f"[{model}] Successfully parsed JSON response")
                    return result
                else:
                    logger.warning(f"[{model}] Returned empty JSON structure")
                    return None
            except json.JSONDecodeError as e:
                logger.error(f"[{model}] Failed to parse JSON: {e}")
                logger.warning(f"[{model}] Raw response that failed: {content[:500]}")
                return None

        except Exception as e:
            logger.error(f"[{model}] API call failed: {e}")
            return None

    async def _chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> Union[dict[str, Any], list[Any]]:
        """
        Send a chat request expecting JSON response with automatic fallback.

        Args:
            system_prompt: System message for context
            user_prompt: User message with the request
            temperature: Temperature for this request (default 0.0 for deterministic JSON)
            max_tokens: Max tokens for this request (defaults to instance setting)

        Returns:
            Parsed JSON response as dictionary or list
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        tokens = max_tokens or self.max_tokens

        # Try primary model first
        result = await self._try_chat_json_with_model(
            self.model, messages, temperature, tokens
        )

        # If primary failed/empty and fallback is configured, try fallback
        if result is None and self.fallback_model and self.fallback_model != self.model:
            logger.warning(f"Primary model ({self.model}) failed, trying fallback ({self.fallback_model})")
            result = await self._try_chat_json_with_model(
                self.fallback_model, messages, temperature, tokens
            )

        # If OpenRouter fallback also failed, try Google Gemini directly (bypasses rate limits)
        if result is None and self.gemini_api_key:
            logger.warning("OpenRouter fallback failed, trying Google Gemini API directly")
            result = await self._try_gemini_json_response(messages, temperature, tokens)

        # Return result or empty structure
        return result if result is not None else {}

    def _extract_json(self, content: str) -> str:
        """
        Extract JSON from LLM response using multiple strategies.

        Args:
            content: Raw LLM response

        Returns:
            Extracted JSON string
        """
        content = content.strip()

        # Strategy 1: Already valid JSON (starts with [ or {)
        if content.startswith("[") or content.startswith("{"):
            # Find the matching closing bracket
            if content.startswith("["):
                end_idx = content.rfind("]")
                if end_idx != -1:
                    return content[:end_idx + 1]
            else:
                end_idx = content.rfind("}")
                if end_idx != -1:
                    return content[:end_idx + 1]

        # Strategy 2: Markdown code block with json tag
        if "```json" in content:
            parts = content.split("```json")
            if len(parts) > 1:
                json_part = parts[1].split("```")[0]
                return json_part.strip()

        # Strategy 3: Generic markdown code block
        if "```" in content:
            parts = content.split("```")
            if len(parts) >= 2:
                return parts[1].strip()

        # Strategy 4: Find first [ or { and extract from there
        for i, char in enumerate(content):
            if char in "[{":
                bracket = char
                close_bracket = "]" if bracket == "[" else "}"
                end_idx = content.rfind(close_bracket)
                if end_idx > i:
                    return content[i:end_idx + 1]

        # Strategy 5: Return as-is and let JSON parser handle the error
        return content

    async def extract_resume(self, text: str) -> dict[str, Any]:
        """
        Extract structured data from resume text.

        Args:
            text: Raw resume text content

        Returns:
            Dictionary with extracted resume data
        """
        prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=text)
        # Use temperature=0.0 for deterministic JSON extraction
        result = await self._chat_json(RESUME_EXTRACTION_SYSTEM, prompt, temperature=0.0, max_tokens=2000)

        # Ensure required fields exist with defaults (use 'or' to handle None values)
        return {
            # Contact information (P1.1)
            "name": result.get("name"),
            "email": result.get("email"),
            "phone": result.get("phone"),
            "linkedin_url": result.get("linkedin_url"),
            "location": result.get("location"),
            # Extracted data
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
        # Use temperature=0.0 for deterministic JSON extraction
        result = await self._chat_json(JOB_EXTRACTION_SYSTEM, prompt, temperature=0.0, max_tokens=1500)

        # Ensure required fields exist with defaults (use 'or' to handle None values)
        return {
            "title": result.get("title"),
            "company": result.get("company"),
            "requirements": result.get("requirements") or [],
            "preferred_skills": result.get("preferred_skills") or [],
            "keywords": result.get("keywords") or [],
            "min_experience_years": result.get("min_experience_years") or 0,
            "education_requirements": result.get("education_requirements") or [],
            # Enhanced fields (P1.3)
            "seniority_level": result.get("seniority_level"),
            "remote_policy": result.get("remote_policy") or "unknown",
            "salary_min": result.get("salary_min"),
            "salary_max": result.get("salary_max"),
            "salary_currency": result.get("salary_currency") or "USD",
            "location": result.get("location"),
        }

    async def generate_interview_questions(
        self,
        resume_summary: str,
        job_summary: str,
        skill_gaps: list[str],
        seniority_level: str = "mid",
    ) -> list[dict[str, Any]]:
        """
        Generate interview preparation questions personalized by seniority.

        Args:
            resume_summary: Summary of candidate's resume
            job_summary: Summary of job requirements
            skill_gaps: List of skills the candidate is missing
            seniority_level: Candidate's detected seniority level (P2.3)

        Returns:
            List of question objects
        """
        gaps_text = ", ".join(skill_gaps) if skill_gaps else "None identified"

        # Get seniority context for difficulty adjustment
        difficulty_context = SENIORITY_CONTEXT.get(
            seniority_level.lower(),
            SENIORITY_CONTEXT.get("mid", "")
        )

        prompt = INTERVIEW_GENERATION_PROMPT.format(
            resume_summary=resume_summary,
            job_requirements=job_summary,
            skill_gaps=gaps_text,
            seniority_level=seniority_level,
            difficulty_context=difficulty_context,
        )

        # Use slightly higher temperature for creative question generation
        result = await self._chat_json(INTERVIEW_GENERATION_SYSTEM, prompt, temperature=0.3, max_tokens=2500)

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
