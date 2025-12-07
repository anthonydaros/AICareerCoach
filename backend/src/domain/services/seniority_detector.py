"""Seniority Detection Service - Detects candidate seniority level from resume."""

import re
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from src.domain.entities.resume import Resume


class SeniorityLevel(str, Enum):
    """Candidate seniority level."""
    JUNIOR = "junior"
    MID = "mid"  # Pleno
    SENIOR = "senior"


@dataclass
class SeniorityResult:
    """Result of seniority detection."""
    level: SeniorityLevel
    confidence: float  # 0-100
    years_experience: float
    scores: Dict[str, float] = field(default_factory=dict)
    indicators: List[str] = field(default_factory=list)


# Seniority indicator patterns (Portuguese + English)
SENIOR_VERBS = [
    # Leadership
    r"\b(liderei|liderado|led|leading|lead)\b",
    r"\b(coordenei|coordinated|coordinating)\b",
    r"\b(gerenciei|managed|managing|manager)\b",
    r"\b(mentored|mentoring|mentor|mentorei)\b",
    r"\b(coached|coaching|coach)\b",
    # Architecture
    r"\b(projetei|designed|architected|architect)\b",
    r"\b(arquitetura|architecture)\b",
    r"\b(escalei|scaled|scaling)\b",
    r"\b(migra[çc][ãa]o|migrated|migration)\b",
    # Ownership
    r"\b(responsável\s+por|responsible\s+for|ownership)\b",
    r"\b(principal|main|primary)\s+(developer|engineer|dev)\b",
    # Strategic
    r"\b(defini|defined|defining)\s+(estrat[ée]gia|strategy)\b",
    r"\b(tomada\s+de\s+decis[ãa]o|decision\s+making)\b",
    r"\b(stakeholder|stakeholders)\b",
]

MID_VERBS = [
    # Implementation
    r"\b(implementei|implemented|implementing)\b",
    r"\b(desenvolvi|developed|developing)\b",
    r"\b(integrei|integrated|integrating)\b",
    r"\b(otimizei|optimized|optimizing)\b",
    r"\b(automatizei|automated|automating)\b",
    r"\b(refatorei|refactored|refactoring)\b",
    # Independence
    r"\b(independently|independente)\b",
    r"\b(autônom[ao]|autonomous)\b",
]

JUNIOR_VERBS = [
    # Support/Assistance
    r"\b(auxiliei|assisted|assisting|helped|helping)\b",
    r"\b(apoiei|supported|supporting)\b",
    r"\b(participei|participated|participating)\b",
    r"\b(contribuí|contributed|contributing)\b",
    r"\b(aprendi|learned|learning)\b",
    r"\b(mantive|maintained|maintaining)\b",
    r"\b(estagi[áa]rio|intern|trainee)\b",
]

# Skills that indicate seniority level
SENIOR_SKILLS = {
    # Architecture patterns
    "ddd", "domain driven design", "event-driven", "hexagonal",
    "cqrs", "microservices architecture", "system design", "clean architecture",
    "event sourcing", "saga pattern",
    # Observability
    "observability", "distributed tracing", "distributed logging",
    "prometheus", "grafana", "datadog", "new relic", "jaeger", "opentelemetry",
    # Advanced Cloud/Infra
    "terraform", "pulumi", "iam", "vpc", "eks", "gke", "aks",
    "infrastructure as code", "cloud architecture", "multi-cloud",
    # Leadership indicators
    "tech lead", "technical leadership", "architecture review",
    "technical strategy", "engineering excellence",
    # Advanced practices
    "performance optimization", "scalability", "high availability",
    "disaster recovery", "security architecture",
}

MID_SKILLS = {
    # Testing
    "test automation", "unit testing", "integration testing", "e2e testing",
    "tdd", "bdd",
    # APIs
    "rest api", "graphql", "api design", "api gateway",
    # Databases
    "database design", "sql optimization", "query optimization",
    "data modeling", "nosql",
    # CI/CD
    "ci/cd", "jenkins", "github actions", "gitlab ci",
    "continuous integration", "continuous deployment",
    # Cloud basics
    "aws", "gcp", "azure", "docker", "kubernetes",
    # Code quality
    "code review", "pull request", "clean code",
}

JUNIOR_SKILLS = {
    # Basic only
    "html", "css", "basic javascript", "git basics", "sql basics",
    "junior developer", "trainee",
}

# Title patterns that indicate seniority
SENIOR_TITLES = [
    r"\b(senior|sr\.?|sênior|pleno\s*iii|lead|principal|staff|architect)\b",
    r"\b(tech\s*lead|technical\s*lead|team\s*lead)\b",
    r"\b(head\s+of|diretor|director|gerente|manager)\b",
    r"\b(specialist|especialista)\b",
]

MID_TITLES = [
    r"\b(pleno|mid|middle|intermediate|ii)\b",
    r"\b(developer|engineer|analyst)\s+(ii|2|pleno)\b",
]

JUNIOR_TITLES = [
    r"\b(junior|jr\.?|júnior|trainee|estagi[áa]rio|intern)\b",
    r"\b(entry\s*level|entry-level)\b",
    r"\b(developer|engineer|analyst)\s+(i|1|junior)\b",
]


class SeniorityDetector:
    """
    Detects seniority level from resume content.

    Uses a weighted scoring system based on:
    - Years of experience (15%)
    - Complexity/responsibility patterns (20%)
    - Autonomy/ownership patterns (20%)
    - Advanced skills (20%)
    - Leadership indicators (15%)
    - Impact/results (10%)
    """

    WEIGHTS = {
        "experience": 0.15,
        "complexity": 0.20,
        "autonomy": 0.20,
        "skills": 0.20,
        "leadership": 0.15,
        "impact": 0.10,
    }

    def detect(self, resume: Resume) -> SeniorityResult:
        """
        Detect seniority level from resume.

        Args:
            resume: Parsed Resume entity

        Returns:
            SeniorityResult with level, confidence, and indicators
        """
        text = resume.raw_content.lower()
        indicators = []

        # Calculate individual scores
        scores = {
            "experience": self._score_experience(resume, indicators),
            "complexity": self._score_complexity(text, indicators),
            "autonomy": self._score_autonomy(text, indicators),
            "skills": self._score_skills(resume, indicators),
            "leadership": self._score_leadership(text, indicators),
            "impact": self._score_impact(text, indicators),
        }

        # Also check for explicit titles
        title_adjustment = self._check_titles(text, indicators)

        # Calculate weighted score (0-100)
        weighted_score = sum(
            scores[key] * self.WEIGHTS[key] * 100
            for key in scores
        )

        # Apply title adjustment (can shift score up to ±20)
        weighted_score += title_adjustment

        # Clamp to 0-100
        weighted_score = max(0, min(100, weighted_score))

        # Determine level based on score
        level, confidence = self._determine_level(weighted_score, scores)

        return SeniorityResult(
            level=level,
            confidence=confidence,
            years_experience=resume.total_experience_years,
            scores=scores,
            indicators=indicators,
        )

    def _score_experience(self, resume: Resume, indicators: List[str]) -> float:
        """Score based on years of experience (0-1)."""
        years = resume.total_experience_years

        if years >= 8:
            indicators.append(f"{years:.0f}+ years of experience (Senior level)")
            return 1.0
        elif years >= 5:
            indicators.append(f"{years:.0f} years of experience (Senior threshold)")
            return 0.85
        elif years >= 3:
            indicators.append(f"{years:.0f} years of experience (Mid level)")
            return 0.6
        elif years >= 2:
            indicators.append(f"{years:.0f} years of experience (Entry to Mid)")
            return 0.4
        elif years >= 1:
            indicators.append(f"{years:.0f} year(s) of experience (Junior)")
            return 0.25
        else:
            indicators.append("Less than 1 year of experience (Entry level)")
            return 0.1

    def _score_complexity(self, text: str, indicators: List[str]) -> float:
        """Score based on complexity of responsibilities (0-1)."""
        senior_matches = sum(
            1 for pattern in SENIOR_VERBS
            if re.search(pattern, text, re.IGNORECASE)
        )
        mid_matches = sum(
            1 for pattern in MID_VERBS
            if re.search(pattern, text, re.IGNORECASE)
        )
        junior_matches = sum(
            1 for pattern in JUNIOR_VERBS
            if re.search(pattern, text, re.IGNORECASE)
        )

        # Calculate weighted score
        total = senior_matches * 3 + mid_matches * 2 + junior_matches * 1
        if total == 0:
            return 0.5  # Neutral

        senior_ratio = (senior_matches * 3) / total

        if senior_matches >= 3:
            indicators.append(f"High-complexity responsibilities detected ({senior_matches} senior patterns)")
        elif mid_matches >= 3:
            indicators.append(f"Mid-complexity responsibilities ({mid_matches} patterns)")

        return min(1.0, 0.3 + senior_ratio * 0.7)

    def _score_autonomy(self, text: str, indicators: List[str]) -> float:
        """Score based on autonomy/ownership patterns (0-1)."""
        ownership_patterns = [
            r"\b(owner|ownership|dono|proprietário)\b",
            r"\b(responsável\s+por|responsible\s+for)\b",
            r"\b(end[\s-]to[\s-]end|e2e|full[\s-]cycle)\b",
            r"\b(independently|independente|autônom)\b",
            r"\b(single[\s-]handedly|sozinho)\b",
        ]

        matches = sum(
            1 for pattern in ownership_patterns
            if re.search(pattern, text, re.IGNORECASE)
        )

        if matches >= 3:
            indicators.append("High autonomy - owns features/products end-to-end")
            return 1.0
        elif matches >= 2:
            indicators.append("Shows independent work capability")
            return 0.7
        elif matches >= 1:
            return 0.5
        else:
            return 0.3

    def _score_skills(self, resume: Resume, indicators: List[str]) -> float:
        """Score based on skill sophistication (0-1)."""
        resume_skills = {s.normalized_name.lower() for s in resume.skills}
        resume_text_lower = resume.raw_content.lower()

        # Also check for skills mentioned in text but not extracted
        all_skills = resume_skills.copy()
        for skill in SENIOR_SKILLS | MID_SKILLS:
            if skill in resume_text_lower:
                all_skills.add(skill)

        senior_count = len(all_skills & SENIOR_SKILLS)
        mid_count = len(all_skills & MID_SKILLS)
        junior_count = len(all_skills & JUNIOR_SKILLS)

        if senior_count >= 5:
            indicators.append(f"Advanced skills: {', '.join(list(all_skills & SENIOR_SKILLS)[:5])}")
            return 1.0
        elif senior_count >= 3:
            indicators.append(f"Has {senior_count} senior-level skills")
            return 0.8
        elif senior_count >= 1 and mid_count >= 3:
            indicators.append(f"Mix of advanced ({senior_count}) and intermediate ({mid_count}) skills")
            return 0.6
        elif mid_count >= 3:
            indicators.append(f"Has {mid_count} mid-level skills")
            return 0.5
        else:
            return 0.3

    def _score_leadership(self, text: str, indicators: List[str]) -> float:
        """Score based on leadership indicators (0-1)."""
        leadership_patterns = [
            r"\b(liderei|led|leading)\s+\w*\s*(team|equipe|time|developer|engineer)",
            r"\b(mentor|mentored|mentoring)\b",
            r"\b(coach|coached|coaching)\b",
            r"\b(train|trained|training)\s+\w*\s*(developer|engineer|team)",
            r"\b(code\s*review|review\s*de\s*código)\b",
            r"\b(pair\s*programming)\b",
            r"\b(onboard|onboarding)\b",
            r"\b(tech\s*lead|technical\s*lead)\b",
            r"\b(team\s*of\s*\d+|equipe\s*de\s*\d+)\b",
        ]

        matches = sum(
            1 for pattern in leadership_patterns
            if re.search(pattern, text, re.IGNORECASE)
        )

        # Check for team size mentions
        team_match = re.search(r"(team|equipe|time)\s+(of|de)\s+(\d+)", text, re.IGNORECASE)
        if team_match:
            team_size = int(team_match.group(3))
            if team_size >= 3:
                indicators.append(f"Led/worked with team of {team_size}")
                matches += 2

        if matches >= 4:
            indicators.append("Strong leadership experience (mentoring, leading teams)")
            return 1.0
        elif matches >= 2:
            indicators.append("Some leadership indicators (code review, mentoring)")
            return 0.7
        elif matches >= 1:
            return 0.4
        else:
            return 0.2

    def _score_impact(self, text: str, indicators: List[str]) -> float:
        """Score based on quantifiable impact (0-1)."""
        impact_patterns = [
            # Performance improvements
            r"(reduc|diminui|improv|melhor|aument|increas)\w*\s*\w*\s*(\d+)\s*%",
            # Scale
            r"(\d+)\s*(mil|million|milh[ãõ])\s*(user|usuário|request|requisi)",
            r"(\d+)\s*(k|K)\s*(user|request|rps|qps)",
            # Revenue/Cost
            r"(R?\$|\$|USD|BRL)\s*\d+",
            r"(sav|econom|cost\s*reduc)\w*\s*\w*\s*\d+",
            # Time improvements
            r"(reduc|diminui)\w*\s*\w*\s*(\d+)\s*(hour|hora|day|dia|minute|minuto|second|segundo)",
        ]

        matches = sum(
            1 for pattern in impact_patterns
            if re.search(pattern, text, re.IGNORECASE)
        )

        if matches >= 3:
            indicators.append("Quantifiable impact demonstrated (metrics, improvements)")
            return 1.0
        elif matches >= 2:
            indicators.append("Some measurable results mentioned")
            return 0.7
        elif matches >= 1:
            return 0.5
        else:
            return 0.3

    def _check_titles(self, text: str, indicators: List[str]) -> float:
        """Check for explicit seniority in job titles. Returns adjustment (-20 to +20)."""
        senior_count = sum(
            1 for pattern in SENIOR_TITLES
            if re.search(pattern, text, re.IGNORECASE)
        )
        mid_count = sum(
            1 for pattern in MID_TITLES
            if re.search(pattern, text, re.IGNORECASE)
        )
        junior_count = sum(
            1 for pattern in JUNIOR_TITLES
            if re.search(pattern, text, re.IGNORECASE)
        )

        if senior_count > 0 and senior_count > junior_count:
            indicators.append("Senior-level job titles found")
            return 15
        elif mid_count > 0 and mid_count > junior_count:
            indicators.append("Mid-level job titles found")
            return 5
        elif junior_count > 0 and junior_count > senior_count:
            indicators.append("Junior/entry-level titles found")
            return -10

        return 0

    def _determine_level(
        self,
        score: float,
        scores: Dict[str, float],
    ) -> tuple[SeniorityLevel, float]:
        """Determine seniority level and confidence from score."""

        # Thresholds
        if score >= 70:
            level = SeniorityLevel.SENIOR
            # Confidence based on how far above threshold
            confidence = min(100, 70 + (score - 70))
        elif score >= 40:
            level = SeniorityLevel.MID
            # Confidence based on distance from boundaries
            distance_from_edges = min(score - 40, 70 - score)
            confidence = 50 + distance_from_edges
        else:
            level = SeniorityLevel.JUNIOR
            confidence = min(100, 90 - score)  # More confident if score is lower

        return level, round(confidence, 1)
