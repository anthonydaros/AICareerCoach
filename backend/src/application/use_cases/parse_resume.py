"""Parse Resume Use Case."""

import uuid
from typing import Any, Optional, List

from src.domain.entities.resume import Resume, Skill, Experience, Education, SkillLevel
from src.infrastructure.llm import OpenAIGateway


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

        return Resume(
            id=str(uuid.uuid4()),
            raw_content=text,
            skills=skills,
            experiences=experiences,
            education=education,
            certifications=certifications,
            total_experience_years=float(total_years),
            filename=filename,
        )

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
