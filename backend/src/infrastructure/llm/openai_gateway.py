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
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

        # Google Gemini fallback (direct API, bypasses OpenRouter rate limits)
        # Support multiple API keys for rate limit rotation
        self.gemini_api_keys = [
            k for k in [settings.gemini_api_key, settings.gemini_api_key_fallback] if k
        ]
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

    async def _call_gemini_with_key(
        self,
        api_key: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> Union[dict[str, Any], list[Any], None]:
        """
        Call Gemini API with a specific API key.

        Args:
            api_key: The Gemini API key to use
            messages: List of message dicts with 'role' and 'content'
            temperature: Temperature for generation
            max_tokens: Max output tokens

        Returns:
            Parsed JSON response, or None if failed

        Raises:
            Exception: Re-raises 429 errors for rate limit handling
        """
        import google.generativeai as genai
        import re

        genai.configure(api_key=api_key)

        # Convert OpenAI messages to Gemini format
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")

        # Disable safety filters - our content (resumes/job postings) is safe
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }

        # Create model with system instruction and safety settings
        model = genai.GenerativeModel(
            self.gemini_model,
            system_instruction=system_msg,
            safety_settings=safety_settings,
        )

        response = await model.generate_content_async(
            user_msg,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json",
            ),
        )

        # Check if response was blocked before accessing .text
        if not response.candidates:
            logger.warning("[Gemini] No candidates in response (possibly blocked)")
            return None

        candidate = response.candidates[0]
        # finish_reason: 1=STOP (normal), 2=MAX_TOKENS, 3=SAFETY, 4=RECITATION, 5=OTHER
        if hasattr(candidate, 'finish_reason') and candidate.finish_reason not in (1, 'STOP', None):
            logger.warning(f"[Gemini] Response issue, finish_reason={candidate.finish_reason}")
            # Still try to get content if available
            if not candidate.content or not candidate.content.parts:
                return None

        # Safely extract content
        if not candidate.content or not candidate.content.parts:
            logger.warning("[Gemini] Response has no content parts")
            return None

        content = candidate.content.parts[0].text or ""

        if not content.strip():
            logger.warning("[Gemini] Returned empty response")
            return None

        logger.debug(f"[Gemini] Raw response (first 500 chars): {content[:500]}")

        # Extract JSON content
        json_content = self._extract_json(content)

        # Fix truncated JSON structures (from MAX_TOKENS cutoff)
        open_braces = json_content.count('{') - json_content.count('}')
        open_brackets = json_content.count('[') - json_content.count(']')
        if open_braces > 0 or open_brackets > 0:
            logger.warning(f"[Gemini] Attempting to fix truncated JSON (unclosed: {open_braces} braces, {open_brackets} brackets)")
            # Remove incomplete trailing content (cut at last complete element)
            # Find last complete value marker (comma, colon after value, or opening bracket)
            last_comma = json_content.rfind(',')
            if last_comma > 0:
                # Keep content up to and including the last comma, then close structures
                json_content = json_content[:last_comma]
            # Close arrays first (innermost), then objects
            json_content += ']' * open_brackets + '}' * open_braces

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

    async def _try_gemini_json_response(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
        retry_count: int = 0,
    ) -> Union[dict[str, Any], list[Any], None]:
        """
        Fallback using Google Gemini API with automatic key rotation on rate limit.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Temperature for generation
            max_tokens: Max output tokens
            retry_count: Number of retries attempted (for token limit increase)

        Returns:
            Parsed JSON response, or None if failed
        """
        if not self.gemini_api_keys:
            logger.warning("No Gemini API keys configured, skipping Gemini fallback")
            return None

        try:
            import google.generativeai as genai  # noqa: F401 - verify import
        except ImportError:
            logger.error("[Gemini] google-generativeai package not installed")
            return None

        # Try each API key in sequence
        for idx, api_key in enumerate(self.gemini_api_keys):
            key_label = "primary" if idx == 0 else f"fallback-{idx}"
            key_preview = f"{api_key[:10]}...{api_key[-4:]}"

            try:
                logger.info(f"[Gemini] Calling {self.gemini_model} with {key_label} key ({key_preview})")
                result = await self._call_gemini_with_key(api_key, messages, temperature, max_tokens)

                if result is not None:
                    logger.info(f"[Gemini] Success with {key_label} key")
                    return result

            except Exception as e:
                error_str = str(e)
                # Check for rate limit error (429)
                if "429" in error_str:
                    if idx < len(self.gemini_api_keys) - 1:
                        logger.warning(f"[Gemini] Rate limit (429) on {key_label} key, trying next key...")
                        continue
                    else:
                        logger.error(f"[Gemini] Rate limit (429) on all keys: {e}")
                else:
                    logger.error(f"[Gemini] {key_label} key failed: {e}")

        # If all keys failed and we haven't retried yet, try again with more tokens
        # This helps recover from MAX_TOKENS truncation (finish_reason=2)
        if retry_count < 1:
            increased_tokens = int(max_tokens * 1.5)
            logger.info(f"[Gemini] Retrying with increased tokens ({max_tokens} -> {increased_tokens})")
            return await self._try_gemini_json_response(
                messages, temperature, increased_tokens, retry_count + 1
            )

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

        # If primary failed/empty, try Google Gemini directly (more reliable than OpenRouter fallback)
        if result is None and self.gemini_api_keys:
            logger.warning(f"Primary model ({self.model}) failed, trying Google Gemini directly")
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
        result = await self._chat_json(RESUME_EXTRACTION_SYSTEM, prompt, temperature=0.0, max_tokens=3000)

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
        result = await self._chat_json(JOB_EXTRACTION_SYSTEM, prompt, temperature=0.0, max_tokens=2500)

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
        result = await self._chat_json(INTERVIEW_GENERATION_SYSTEM, prompt, temperature=0.3, max_tokens=3500)

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
