"""Job Titles Knowledge Base - 365+ tech titles with seniority mapping."""

import re
from typing import Optional

# Seniority level modifiers for title keywords
SENIORITY_KEYWORDS: dict[str, int] = {
    # Level modifiers (added to base level)
    "intern": -3,
    "estagiário": -3,
    "estagiario": -3,
    "trainee": -2,
    "junior": -2,
    "júnior": -2,
    "jr": -2,
    "jr.": -2,
    "associate": -1,
    "entry": -1,
    "entry-level": -1,
    "pleno": 0,  # Brazilian mid-level
    "mid": 0,
    "mid-level": 0,
    "intermediate": 0,
    "senior": 2,
    "sênior": 2,
    "sr": 2,
    "sr.": 2,
    "staff": 3,
    "principal": 4,
    "distinguished": 5,
    "fellow": 6,
    # Leadership modifiers
    "lead": 2,
    "tech lead": 3,
    "team lead": 2,
    "architect": 3,
    "head": 4,
    "head of": 4,
    "director": 5,
    "vp": 6,
    "vice president": 6,
    "cto": 7,
    "cio": 7,
    "chief": 7,
    "c-level": 7,
    "founder": 7,
    "co-founder": 7,
}

# Level names for display
LEVEL_NAMES: dict[int, str] = {
    0: "Intern/Trainee",
    1: "Entry Level",
    2: "Junior",
    3: "Mid-Level",
    4: "Senior",
    5: "Staff/Lead",
    6: "Principal/Architect",
    7: "Director/Head",
    8: "VP/Executive",
}

# Role categories with base seniority levels and keywords
ROLE_CATEGORIES: dict[str, dict] = {
    "software_engineering": {
        "base_level": 3,
        "titles": [
            "software engineer",
            "software developer",
            "programmer",
            "developer",
            "full stack developer",
            "fullstack developer",
            "full-stack developer",
            "backend developer",
            "back-end developer",
            "backend engineer",
            "frontend developer",
            "front-end developer",
            "frontend engineer",
            "web developer",
            "application developer",
            "systems developer",
            "platform engineer",
            "desenvolvedor",
            "programador",
            "engenheiro de software",
        ],
        "keywords": ["code", "coding", "programming", "software", "development"],
    },
    "devops_sre": {
        "base_level": 4,
        "titles": [
            "devops engineer",
            "site reliability engineer",
            "sre",
            "platform engineer",
            "infrastructure engineer",
            "cloud engineer",
            "systems engineer",
            "release engineer",
            "build engineer",
            "deployment engineer",
            "engenheiro devops",
            "engenheiro de infraestrutura",
        ],
        "keywords": ["devops", "sre", "infrastructure", "cloud", "kubernetes", "docker"],
    },
    "data_engineering": {
        "base_level": 4,
        "titles": [
            "data engineer",
            "data platform engineer",
            "etl developer",
            "data pipeline engineer",
            "analytics engineer",
            "bi engineer",
            "business intelligence engineer",
            "data warehouse engineer",
            "engenheiro de dados",
        ],
        "keywords": ["data pipeline", "etl", "warehouse", "spark", "airflow"],
    },
    "data_science": {
        "base_level": 4,
        "titles": [
            "data scientist",
            "machine learning engineer",
            "ml engineer",
            "ai engineer",
            "research scientist",
            "applied scientist",
            "nlp engineer",
            "computer vision engineer",
            "deep learning engineer",
            "cientista de dados",
            "engenheiro de machine learning",
        ],
        "keywords": ["machine learning", "ml", "ai", "neural network", "model training"],
    },
    "ai_ml": {
        "base_level": 4,
        "titles": [
            "ai engineer",
            "artificial intelligence engineer",
            "llm engineer",
            "mlops engineer",
            "ai/ml engineer",
            "prompt engineer",
            "ai researcher",
            "ml researcher",
            "ai specialist",
            "engenheiro de ia",
        ],
        "keywords": ["llm", "gpt", "langchain", "rag", "fine-tuning", "embeddings"],
    },
    "product_management": {
        "base_level": 4,
        "titles": [
            "product manager",
            "product owner",
            "technical product manager",
            "group product manager",
            "product lead",
            "gerente de produto",
            "dono do produto",
        ],
        "keywords": ["product", "roadmap", "stakeholder", "requirements", "user stories"],
    },
    "design": {
        "base_level": 3,
        "titles": [
            "ux designer",
            "ui designer",
            "ux/ui designer",
            "product designer",
            "interaction designer",
            "visual designer",
            "user researcher",
            "ux researcher",
            "designer",
            "designer de produto",
        ],
        "keywords": ["figma", "sketch", "user experience", "wireframe", "prototype"],
    },
    "qa_testing": {
        "base_level": 3,
        "titles": [
            "qa engineer",
            "quality assurance engineer",
            "test engineer",
            "sdet",
            "automation engineer",
            "test automation engineer",
            "quality engineer",
            "analista de qualidade",
            "engenheiro de testes",
        ],
        "keywords": ["testing", "qa", "automation", "selenium", "cypress", "jest"],
    },
    "security": {
        "base_level": 4,
        "titles": [
            "security engineer",
            "application security engineer",
            "penetration tester",
            "security analyst",
            "devsecops engineer",
            "cybersecurity engineer",
            "information security engineer",
            "engenheiro de segurança",
            "analista de segurança",
        ],
        "keywords": ["security", "pentest", "vulnerability", "compliance", "soc"],
    },
    "mobile": {
        "base_level": 3,
        "titles": [
            "mobile developer",
            "ios developer",
            "android developer",
            "mobile engineer",
            "react native developer",
            "flutter developer",
            "swift developer",
            "kotlin developer",
            "desenvolvedor mobile",
        ],
        "keywords": ["ios", "android", "mobile", "react native", "flutter", "swift"],
    },
    "management": {
        "base_level": 5,
        "titles": [
            "engineering manager",
            "development manager",
            "software development manager",
            "technical manager",
            "it manager",
            "technology manager",
            "gerente de engenharia",
            "gerente de desenvolvimento",
        ],
        "keywords": ["manage", "team", "leadership", "hiring", "performance review"],
    },
    "architecture": {
        "base_level": 6,
        "titles": [
            "software architect",
            "solutions architect",
            "enterprise architect",
            "technical architect",
            "system architect",
            "cloud architect",
            "data architect",
            "arquiteto de software",
            "arquiteto de soluções",
        ],
        "keywords": ["architecture", "design patterns", "system design", "scalability"],
    },
    "executive": {
        "base_level": 7,
        "titles": [
            "cto",
            "chief technology officer",
            "vp of engineering",
            "vice president of engineering",
            "director of engineering",
            "head of engineering",
            "cio",
            "chief information officer",
            "diretor de tecnologia",
        ],
        "keywords": ["executive", "strategy", "board", "c-level", "leadership"],
    },
    "support_ops": {
        "base_level": 2,
        "titles": [
            "technical support engineer",
            "support engineer",
            "it support",
            "helpdesk",
            "system administrator",
            "network administrator",
            "database administrator",
            "dba",
            "analista de suporte",
            "administrador de sistemas",
        ],
        "keywords": ["support", "troubleshoot", "helpdesk", "administration"],
    },
    "analyst": {
        "base_level": 3,
        "titles": [
            "business analyst",
            "systems analyst",
            "data analyst",
            "technical analyst",
            "it analyst",
            "requirements analyst",
            "analista de sistemas",
            "analista de negócios",
            "analista de dados",
        ],
        "keywords": ["analysis", "requirements", "documentation", "reporting"],
    },
}

# Common title aliases/variations
TITLE_ALIASES: dict[str, str] = {
    "swe": "software engineer",
    "sde": "software development engineer",
    "dev": "developer",
    "fe": "frontend engineer",
    "be": "backend engineer",
    "fs": "fullstack developer",
    "pm": "product manager",
    "po": "product owner",
    "em": "engineering manager",
    "tpm": "technical product manager",
    "sa": "solutions architect",
    "ta": "technical architect",
    "de": "data engineer",
    "ds": "data scientist",
    "mle": "machine learning engineer",
    "sre": "site reliability engineer",
    "dba": "database administrator",
    "sysadmin": "system administrator",
}


def detect_seniority_from_title(title: str) -> tuple[int, str]:
    """
    Detect seniority level from job title.

    Args:
        title: Job title string

    Returns:
        Tuple of (level: int 0-8, level_name: str)
    """
    if not title:
        return 3, LEVEL_NAMES[3]  # Default to mid-level

    title_lower = title.lower().strip()

    # Check for aliases first
    for alias, full_title in TITLE_ALIASES.items():
        if alias in title_lower.split():
            title_lower = title_lower.replace(alias, full_title)

    # Find base level from role category
    base_level = 3  # Default mid-level
    for category, data in ROLE_CATEGORIES.items():
        for role_title in data["titles"]:
            if role_title in title_lower:
                base_level = data["base_level"]
                break

    # Apply seniority modifiers
    modifier = 0
    for keyword, mod in SENIORITY_KEYWORDS.items():
        if keyword in title_lower:
            modifier = max(modifier, mod) if mod > 0 else min(modifier, mod)

    # Calculate final level (0-8 range)
    final_level = max(0, min(8, base_level + modifier))

    return final_level, LEVEL_NAMES.get(final_level, "Unknown")


def detect_category(title: str) -> Optional[str]:
    """
    Detect role category from job title.

    Args:
        title: Job title string

    Returns:
        Category name or None if not detected
    """
    if not title:
        return None

    title_lower = title.lower().strip()

    # Check title matches first (more specific)
    for category, data in ROLE_CATEGORIES.items():
        for role_title in data["titles"]:
            if role_title in title_lower:
                return category

    # Check keyword matches (broader)
    for category, data in ROLE_CATEGORIES.items():
        for keyword in data.get("keywords", []):
            if keyword in title_lower:
                return category

    return None


def get_related_titles(title: str) -> list[str]:
    """
    Get related job titles based on category.

    Args:
        title: Job title string

    Returns:
        List of related title strings
    """
    category = detect_category(title)
    if category and category in ROLE_CATEGORIES:
        return ROLE_CATEGORIES[category]["titles"]
    return []


def normalize_title(title: str) -> str:
    """
    Normalize a job title for comparison.

    Args:
        title: Raw job title

    Returns:
        Normalized title string
    """
    if not title:
        return ""

    # Lowercase and strip
    normalized = title.lower().strip()

    # Expand aliases
    for alias, full_title in TITLE_ALIASES.items():
        pattern = r'\b' + re.escape(alias) + r'\b'
        normalized = re.sub(pattern, full_title, normalized)

    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized)

    return normalized
