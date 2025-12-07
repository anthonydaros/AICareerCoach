"""Parse Resume Use Case."""

import re
import uuid
import logging
from typing import Any, Optional, List

from src.domain.entities.resume import Resume, Skill, Experience, Education, SkillLevel
from src.infrastructure.llm import OpenAIGateway
from src.domain.knowledge.ats_scoring import KEYWORD_CATEGORIES

logger = logging.getLogger(__name__)

# Known skills for regex fallback extraction
KNOWN_SKILLS = set()
for category_data in KEYWORD_CATEGORIES.values():
    KNOWN_SKILLS.update(skill.lower() for skill in category_data.get("examples", []))


class ParseResumeUseCase:
    """Use case for parsing resume text into structured data."""

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(self, text: str, filename: Optional[str] = None) -> Resume:
        """
        Parse resume text into structured Resume entity.

        Args:
            text: Raw resume text
            filename: Optional original filename

        Returns:
            Parsed Resume entity
        """
        # Extract structured data using LLM
        extracted = await self.llm_gateway.extract_resume(text)

        # Convert to domain entities (use 'or []' to handle None values from LLM)
        skills = self._parse_skills(extracted.get("skills") or [])
        experiences = self._parse_experiences(extracted.get("experiences") or [])
        education = self._parse_education(extracted.get("education") or [])
        certifications = extracted.get("certifications") or []
        total_years = extracted.get("total_experience_years") or 0.0

        # P4.1: Fallback to regex extraction if LLM failed to extract skills
        if not skills:
            logger.warning("LLM failed to extract skills, using regex fallback")
            skills = self._extract_skills_regex(text)

        # Fallback for experience calculation if LLM returned 0
        if total_years == 0 and text:
            total_years = self._extract_experience_years_regex(text)

        # P4.2: Extract contact info via regex if LLM failed
        email = extracted.get("email")
        phone = extracted.get("phone")
        linkedin_url = extracted.get("linkedin_url")
        name = extracted.get("name")
        location = extracted.get("location")

        if not email or not phone:
            contact_info = self._extract_contact_regex(text)
            if not email:
                email = contact_info.get("email")
            if not phone:
                phone = contact_info.get("phone")
            if not linkedin_url:
                linkedin_url = contact_info.get("linkedin_url")
            if not name:
                name = contact_info.get("name")

        return Resume(
            id=str(uuid.uuid4()),
            raw_content=text,
            name=name,
            email=email,
            phone=phone,
            linkedin_url=linkedin_url,
            location=location,
            skills=skills,
            experiences=experiences,
            education=education,
            certifications=certifications,
            total_experience_years=float(total_years),
            filename=filename,
        )

    def _extract_skills_regex(self, text: str) -> list[Skill]:
        """
        P4.1: Fallback regex extraction for skills when LLM fails.
        Uses knowledge base of known skills to find matches in resume text.
        """
        text_lower = text.lower()
        found_skills = []

        for skill in KNOWN_SKILLS:
            # Use word boundary matching to avoid partial matches
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                found_skills.append(Skill(
                    name=skill.title() if len(skill) > 3 else skill.upper(),
                    normalized_name=skill.lower(),
                    level=SkillLevel.INTERMEDIATE,
                    years_experience=None,
                ))

        logger.info(f"Regex fallback extracted {len(found_skills)} skills")
        return found_skills

    def _extract_experience_years_regex(self, text: str) -> float:
        """
        P4.1: Fallback regex extraction for total experience years.
        """
        # Pattern 1: "X+ years" or "X years"
        years_pattern = r'(\d+)\+?\s*(?:years?|anos?)\s+(?:of\s+)?(?:experience|experiência)'
        matches = re.findall(years_pattern, text, re.IGNORECASE)
        if matches:
            return float(max(int(m) for m in matches))

        # Pattern 2: Count job entries with dates (2021 - Present, 2019 - 2021, etc.)
        date_ranges = re.findall(
            r'(\d{4})\s*[-–]\s*(?:Present|Presente|Atual|(\d{4}))',
            text,
            re.IGNORECASE
        )
        if date_ranges:
            # Calculate years from date ranges
            total_months = 0
            for start, end in date_ranges:
                start_year = int(start)
                end_year = 2024 if not end else int(end)  # Present = current year
                total_months += (end_year - start_year) * 12
            return round(total_months / 12, 1)

        return 0.0

    def _parse_skills(self, skills_data: list[dict[str, Any]]) -> list[Skill]:
        """Parse skills from extracted data."""
        skills = []
        for s in skills_data:
            if not isinstance(s, dict):
                continue

            name = s.get("name") or ""
            if not name:
                continue

            # Handle None values from LLM - use 'or' pattern
            level_str = (s.get("level") or "intermediate").lower()
            try:
                level = SkillLevel(level_str)
            except ValueError:
                level = SkillLevel.INTERMEDIATE

            skills.append(Skill(
                name=name,
                normalized_name=s.get("normalized_name") or name,
                level=level,
                years_experience=s.get("years_experience"),
            ))

        return skills

    def _parse_experiences(self, exp_data: list[dict[str, Any]]) -> list[Experience]:
        """Parse experiences from extracted data."""
        experiences = []
        for e in exp_data:
            if not isinstance(e, dict):
                continue

            # Handle None values from LLM - use 'or' pattern
            title = e.get("title") or ""
            company = e.get("company") or ""
            if not title or not company:
                continue

            experiences.append(Experience(
                title=title,
                company=company,
                duration_months=int(e.get("duration_months") or 0),
                description=e.get("description") or "",
                skills_used=e.get("skills_used") or [],
            ))

        return experiences

    def _parse_education(self, edu_data: list[dict[str, Any]]) -> list[Education]:
        """Parse education from extracted data."""
        education = []
        for ed in edu_data:
            if not isinstance(ed, dict):
                continue

            # Handle None values from LLM - use 'or' pattern
            degree = ed.get("degree") or ""
            field = ed.get("field") or ""
            institution = ed.get("institution") or ""
            if not degree or not institution:
                continue

            education.append(Education(
                degree=degree,
                field=field or "General",
                institution=institution,
                year=ed.get("year"),
            ))

        return education

    def _extract_contact_regex(self, text: str) -> dict[str, Optional[str]]:
        """
        P4.2: Fallback regex extraction for contact information when LLM fails.
        """
        contact: dict[str, Optional[str]] = {
            "email": None,
            "phone": None,
            "linkedin_url": None,
            "name": None,
        }

        # Extract email
        email_match = re.search(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            text
        )
        if email_match:
            contact["email"] = email_match.group(0).lower()

        # Extract phone (BR and international formats)
        phone_patterns = [
            r'\+?55\s*\(?0?\d{2}\)?\s*\d{4,5}[-.\s]?\d{4}',  # BR: +55 (11) 99999-8888
            r'\(?0?\d{2}\)?\s*\d{4,5}[-.\s]?\d{4}',  # BR without country code
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact["phone"] = phone_match.group(0)
                break

        # Extract LinkedIn URL
        linkedin_match = re.search(
            r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+',
            text,
            re.IGNORECASE
        )
        if linkedin_match:
            url = linkedin_match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            contact["linkedin_url"] = url

        # Extract name (first line that looks like a name - capitalized words)
        name_match = re.search(
            r'^([A-Z][a-záéíóúàèìòùâêîôûãõç]+(?:\s+[A-Z][a-záéíóúàèìòùâêîôûãõç]+)+)',
            text,
            re.MULTILINE
        )
        if name_match:
            contact["name"] = name_match.group(1)

        if contact["email"] or contact["phone"]:
            logger.info(f"Regex extracted contact: email={contact['email']}, phone={contact['phone']}")

        return contact
