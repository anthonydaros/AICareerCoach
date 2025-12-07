"""Seniority Detection Knowledge Base - Thresholds, action verbs, and indicators."""

from typing import Any

# Regional thresholds for seniority levels (years of experience)
SENIORITY_THRESHOLDS: dict[str, dict[str, tuple[float, float]]] = {
    # US Market thresholds
    "us": {
        "intern": (0, 0),
        "entry": (0, 1),
        "junior": (0, 2),
        "mid": (2, 5),
        "senior": (5, 8),
        "staff": (8, 12),
        "principal": (12, 15),
        "director": (15, 20),
        "executive": (20, 99),
    },
    # Brazilian Market thresholds (includes "Pleno")
    "br": {
        "estagiario": (0, 0),
        "trainee": (0, 1),
        "junior": (0, 2),
        "pleno": (2, 4),  # Brazilian mid-level
        "senior": (4, 7),
        "especialista": (7, 10),
        "coordenador": (10, 15),
        "gerente": (15, 20),
        "diretor": (20, 99),
    },
}

# Action verbs that indicate seniority level
ACTION_VERBS_BY_LEVEL: dict[str, list[str]] = {
    "junior": [
        "assisted",
        "helped",
        "supported",
        "contributed",
        "participated",
        "learned",
        "observed",
        "shadowed",
        "completed",
        "executed",
        # Portuguese
        "auxiliou",
        "ajudou",
        "apoiou",
        "contribuiu",
        "participou",
        "aprendeu",
    ],
    "mid": [
        "developed",
        "implemented",
        "built",
        "created",
        "designed",
        "maintained",
        "managed",
        "collaborated",
        "resolved",
        "improved",
        "optimized",
        # Portuguese
        "desenvolveu",
        "implementou",
        "construiu",
        "criou",
        "projetou",
        "manteve",
        "gerenciou",
    ],
    "senior": [
        "led",
        "architected",
        "mentored",
        "drove",
        "spearheaded",
        "established",
        "defined",
        "influenced",
        "transformed",
        "scaled",
        "strategized",
        "pioneered",
        "championed",
        "orchestrated",
        "directed",
        # Portuguese
        "liderou",
        "arquitetou",
        "mentorou",
        "conduziu",
        "estabeleceu",
        "definiu",
        "influenciou",
        "transformou",
        "escalou",
    ],
    "leadership": [
        "owned",
        "delivered",
        "launched",
        "evangelized",
        "founded",
        "negotiated",
        "partnered",
        "secured",
        "closed",
        "acquired",
        # Portuguese
        "fundou",
        "negociou",
        "parceirou",
    ],
}

# Skill indicators by seniority level
SKILL_INDICATORS: dict[str, dict[str, list[str]]] = {
    "junior": {
        "tools": ["git basics", "ide", "debugging", "unit tests"],
        "concepts": ["data structures", "algorithms basics", "oop basics"],
        "soft": ["communication", "teamwork", "willingness to learn"],
    },
    "mid": {
        "tools": ["ci/cd", "docker", "monitoring", "testing frameworks"],
        "concepts": ["design patterns", "api design", "database design", "security basics"],
        "soft": ["code review", "documentation", "estimation", "cross-team collaboration"],
    },
    "senior": {
        "tools": ["kubernetes", "terraform", "observability", "performance profiling"],
        "concepts": [
            "system design",
            "distributed systems",
            "scalability",
            "high availability",
            "architecture patterns",
        ],
        "soft": [
            "mentoring",
            "technical leadership",
            "stakeholder management",
            "project planning",
            "influence without authority",
        ],
    },
    "staff": {
        "tools": ["infrastructure as code", "platform engineering", "mlops"],
        "concepts": [
            "enterprise architecture",
            "cross-org alignment",
            "technical strategy",
            "build vs buy decisions",
        ],
        "soft": [
            "org-wide influence",
            "executive communication",
            "roadmap ownership",
            "hiring/team building",
        ],
    },
}

# Impact scope indicators
IMPACT_SCOPE: dict[str, dict[str, Any]] = {
    "individual": {
        "level": "junior",
        "indicators": ["own tasks", "individual contributions", "learning focused"],
        "score_weight": 0.3,
    },
    "team": {
        "level": "mid",
        "indicators": [
            "team deliverables",
            "collaboration",
            "code reviews",
            "feature ownership",
        ],
        "score_weight": 0.5,
    },
    "multi_team": {
        "level": "senior",
        "indicators": [
            "cross-team projects",
            "technical decisions affecting multiple teams",
            "mentoring across teams",
        ],
        "score_weight": 0.7,
    },
    "org_wide": {
        "level": "staff",
        "indicators": [
            "organization-wide initiatives",
            "company standards",
            "platform/infrastructure work",
        ],
        "score_weight": 0.85,
    },
    "company": {
        "level": "principal",
        "indicators": [
            "company strategy",
            "external representation",
            "industry influence",
        ],
        "score_weight": 1.0,
    },
}

# Team size indicators
TEAM_SIZE_THRESHOLDS: dict[str, tuple[int, int]] = {
    "individual_contributor": (0, 0),
    "tech_lead": (2, 5),
    "manager": (5, 10),
    "senior_manager": (10, 25),
    "director": (25, 100),
    "vp": (100, 500),
    "c_level": (500, 99999),
}

# Complexity indicators by level
COMPLEXITY_PATTERNS: dict[str, list[str]] = {
    "junior": [
        "bug fixes",
        "minor features",
        "documentation",
        "testing",
        "maintenance tasks",
    ],
    "mid": [
        "full features",
        "component design",
        "integration work",
        "performance improvements",
        "code refactoring",
    ],
    "senior": [
        "system design",
        "architecture decisions",
        "complex integrations",
        "cross-service work",
        "technical strategy",
        "platform development",
    ],
    "staff": [
        "company-wide systems",
        "technical vision",
        "foundational infrastructure",
        "standards and best practices",
        "build vs buy decisions",
    ],
}


def detect_seniority_level(
    years_experience: float,
    action_verbs: list[str],
    skills: list[str],
    team_size: int = 0,
    region: str = "us",
) -> dict[str, Any]:
    """
    Detect seniority level based on multiple factors.

    Args:
        years_experience: Total years of professional experience
        action_verbs: List of action verbs from resume
        skills: List of skills from resume
        team_size: Size of team led/managed (0 if IC)
        region: Market region ('us' or 'br')

    Returns:
        Dict with level, confidence, and supporting evidence
    """
    scores = {
        "experience": _score_experience(years_experience, region),
        "verbs": _score_action_verbs(action_verbs),
        "skills": _score_skills(skills),
        "leadership": _score_leadership(team_size),
    }

    # Weighted average
    weights = {"experience": 0.35, "verbs": 0.25, "skills": 0.25, "leadership": 0.15}

    total_score = sum(scores[k] * weights[k] for k in scores)

    # Map score to level
    level = _score_to_level(total_score)

    # Calculate confidence
    variance = sum((s - total_score) ** 2 for s in scores.values()) / len(scores)
    confidence = max(0.5, 1.0 - (variance * 0.1))

    return {
        "level": level,
        "score": round(total_score * 100, 1),
        "confidence": round(confidence * 100, 1),
        "scores": {k: round(v * 100, 1) for k, v in scores.items()},
        "indicators": _get_indicators(level),
    }


def _score_experience(years: float, region: str) -> float:
    """Score based on years of experience."""
    thresholds = SENIORITY_THRESHOLDS.get(region, SENIORITY_THRESHOLDS["us"])

    if years >= 15:
        return 1.0
    elif years >= 10:
        return 0.85
    elif years >= 7:
        return 0.7
    elif years >= 5:
        return 0.6
    elif years >= 3:
        return 0.45
    elif years >= 1:
        return 0.3
    else:
        return 0.15


def _score_action_verbs(verbs: list[str]) -> float:
    """Score based on action verbs used."""
    if not verbs:
        return 0.3

    verbs_lower = [v.lower() for v in verbs]
    scores = []

    for verb in verbs_lower:
        if verb in ACTION_VERBS_BY_LEVEL["leadership"]:
            scores.append(1.0)
        elif verb in ACTION_VERBS_BY_LEVEL["senior"]:
            scores.append(0.8)
        elif verb in ACTION_VERBS_BY_LEVEL["mid"]:
            scores.append(0.5)
        elif verb in ACTION_VERBS_BY_LEVEL["junior"]:
            scores.append(0.3)

    return sum(scores) / len(scores) if scores else 0.3


def _score_skills(skills: list[str]) -> float:
    """Score based on skill sophistication."""
    if not skills:
        return 0.3

    skills_lower = [s.lower() for s in skills]
    senior_count = 0
    total_matched = 0

    for level, indicators in SKILL_INDICATORS.items():
        for category, skill_list in indicators.items():
            for skill in skill_list:
                if any(skill.lower() in s for s in skills_lower):
                    total_matched += 1
                    if level in ["senior", "staff"]:
                        senior_count += 1

    if total_matched == 0:
        return 0.3

    senior_ratio = senior_count / total_matched
    return min(1.0, 0.3 + (senior_ratio * 0.7))


def _score_leadership(team_size: int) -> float:
    """Score based on team leadership."""
    if team_size >= 100:
        return 1.0
    elif team_size >= 25:
        return 0.85
    elif team_size >= 10:
        return 0.7
    elif team_size >= 5:
        return 0.5
    elif team_size >= 2:
        return 0.35
    else:
        return 0.2


def _score_to_level(score: float) -> str:
    """Convert numeric score to level name."""
    if score >= 0.9:
        return "executive"
    elif score >= 0.8:
        return "director"
    elif score >= 0.7:
        return "staff"
    elif score >= 0.6:
        return "senior"
    elif score >= 0.45:
        return "mid"
    elif score >= 0.25:
        return "junior"
    else:
        return "entry"


def _get_indicators(level: str) -> list[str]:
    """Get expected indicators for a seniority level."""
    indicators = []

    if level in SKILL_INDICATORS:
        for category, skills in SKILL_INDICATORS[level].items():
            indicators.extend(skills[:3])

    if level in COMPLEXITY_PATTERNS:
        indicators.extend(COMPLEXITY_PATTERNS[level][:3])

    return indicators[:10]


def get_expected_skills_for_level(level: str) -> dict[str, list[str]]:
    """Get expected skills for a given seniority level."""
    return SKILL_INDICATORS.get(level, SKILL_INDICATORS["mid"])


def get_action_verbs_for_level(level: str) -> list[str]:
    """Get recommended action verbs for a given seniority level."""
    return ACTION_VERBS_BY_LEVEL.get(level, ACTION_VERBS_BY_LEVEL["mid"])
