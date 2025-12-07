"""Knowledge bases for deterministic career analysis."""

from .job_titles import (
    SENIORITY_KEYWORDS,
    ROLE_CATEGORIES,
    LEVEL_NAMES,
    detect_seniority_from_title,
    detect_category,
)
from .seniority_detection import (
    SENIORITY_THRESHOLDS,
    ACTION_VERBS_BY_LEVEL,
    SKILL_INDICATORS,
    IMPACT_SCOPE,
    detect_seniority_level,
)
from .career_stability import (
    STABILITY_FLAGS,
    PJ_CLT_ADJUSTMENTS,
    TECH_LAYOFF_COMPANIES,
    calculate_stability_score,
)
from .ats_scoring import (
    ATS_WEIGHTS,
    CONTACT_PATTERNS,
    KEYWORD_CATEGORIES,
    calculate_ats_component_scores,
)

__all__ = [
    # job_titles
    "SENIORITY_KEYWORDS",
    "ROLE_CATEGORIES",
    "LEVEL_NAMES",
    "detect_seniority_from_title",
    "detect_category",
    # seniority_detection
    "SENIORITY_THRESHOLDS",
    "ACTION_VERBS_BY_LEVEL",
    "SKILL_INDICATORS",
    "IMPACT_SCOPE",
    "detect_seniority_level",
    # career_stability
    "STABILITY_FLAGS",
    "PJ_CLT_ADJUSTMENTS",
    "TECH_LAYOFF_COMPANIES",
    "calculate_stability_score",
    # ats_scoring
    "ATS_WEIGHTS",
    "CONTACT_PATTERNS",
    "KEYWORD_CATEGORIES",
    "calculate_ats_component_scores",
]
