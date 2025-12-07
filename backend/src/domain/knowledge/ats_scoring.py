"""ATS Scoring Knowledge Base - Scoring weights, patterns, and rules."""

import re
from typing import Any, Optional

# ATS Scoring Weights (total = 100 points)
ATS_WEIGHTS: dict[str, dict[str, Any]] = {
    "skills": {
        "max_points": 40,
        "weight": 0.40,
        "description": "Technical and soft skills match",
        "subcategories": {
            "required_skills": 0.70,  # 70% of skill points
            "preferred_skills": 0.30,  # 30% of skill points
        },
    },
    "experience": {
        "max_points": 30,
        "weight": 0.30,
        "description": "Years of experience match",
        "thresholds": {
            "exceeds": 1.0,  # Full points if exceeds
            "meets": 0.9,  # 90% if meets exactly
            "close": 0.7,  # 70% if within 1 year
            "partial": 0.5,  # 50% if within 2 years
            "insufficient": 0.2,  # 20% if >2 years short
        },
    },
    "education": {
        "max_points": 15,
        "weight": 0.15,
        "description": "Education requirements match",
        "levels": {
            "phd": 1.0,
            "masters": 0.9,
            "bachelors": 0.8,
            "associate": 0.6,
            "bootcamp": 0.5,
            "self_taught": 0.4,
        },
    },
    "certifications": {
        "max_points": 10,
        "weight": 0.10,
        "description": "Relevant certifications",
        "bonus_per_cert": 2.5,  # Points per relevant cert (max 10)
    },
    "keywords": {
        "max_points": 5,
        "weight": 0.05,
        "description": "Keyword density and placement",
    },
}

# Role-specific weight adjustments
ROLE_WEIGHT_ADJUSTMENTS: dict[str, dict[str, float]] = {
    "technical": {
        "skills": 0.45,
        "experience": 0.25,
        "education": 0.15,
        "certifications": 0.10,
        "keywords": 0.05,
    },
    "management": {
        "skills": 0.30,
        "experience": 0.35,
        "education": 0.15,
        "certifications": 0.10,
        "keywords": 0.10,
    },
    "entry_level": {
        "skills": 0.35,
        "experience": 0.15,
        "education": 0.30,
        "certifications": 0.15,
        "keywords": 0.05,
    },
    "senior": {
        "skills": 0.40,
        "experience": 0.35,
        "education": 0.10,
        "certifications": 0.10,
        "keywords": 0.05,
    },
}

# Contact information regex patterns
CONTACT_PATTERNS: dict[str, str] = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone_us": r"(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "phone_br": r"(\+55[-.\s]?)?\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}",
    "linkedin": r"linkedin\.com/in/[\w-]+",
    "github": r"github\.com/[\w-]+",
    "portfolio": r"https?://[\w.-]+\.[a-z]{2,}(?:/[\w.-]*)*",
}

# Keyword categories for ATS matching
KEYWORD_CATEGORIES: dict[str, dict[str, Any]] = {
    "programming_languages": {
        "weight": "critical",
        "examples": [
            "python",
            "javascript",
            "typescript",
            "java",
            "c++",
            "c#",
            "go",
            "rust",
            "ruby",
            "php",
            "swift",
            "kotlin",
        ],
    },
    "frameworks": {
        "weight": "high",
        "examples": [
            "react",
            "angular",
            "vue",
            "django",
            "flask",
            "fastapi",
            "spring",
            "express",
            "next.js",
            "rails",
        ],
    },
    "cloud_platforms": {
        "weight": "critical",
        "examples": [
            "aws",
            "azure",
            "gcp",
            "google cloud",
            "heroku",
            "digitalocean",
            "vercel",
        ],
    },
    "databases": {
        "weight": "high",
        "examples": [
            "postgresql",
            "mysql",
            "mongodb",
            "redis",
            "elasticsearch",
            "dynamodb",
            "cassandra",
        ],
    },
    "devops_tools": {
        "weight": "high",
        "examples": [
            "docker",
            "kubernetes",
            "terraform",
            "ansible",
            "jenkins",
            "github actions",
            "gitlab ci",
        ],
    },
    "ai_ml": {
        "weight": "critical",
        "examples": [
            "machine learning",
            "deep learning",
            "nlp",
            "llm",
            "tensorflow",
            "pytorch",
            "langchain",
            "rag",
        ],
    },
    "soft_skills": {
        "weight": "medium",
        "examples": [
            "leadership",
            "communication",
            "problem solving",
            "teamwork",
            "agile",
            "scrum",
            "mentoring",
        ],
    },
    "methodologies": {
        "weight": "medium",
        "examples": [
            "agile",
            "scrum",
            "kanban",
            "ci/cd",
            "tdd",
            "bdd",
            "devops",
            "microservices",
        ],
    },
}

# Format issues that affect ATS parsing
FORMAT_ISSUES: dict[str, dict[str, Any]] = {
    "special_characters": {
        "pattern": r"[^\x00-\x7F]+",
        "description": "Special characters detected - use standard bullets and symbols",
        "impact": -2,
    },
    "tables": {
        "indicators": ["table", "grid", "columns"],
        "description": "Tables may not parse correctly in ATS",
        "impact": -3,
    },
    "images": {
        "indicators": ["image", "logo", "photo", "picture"],
        "description": "Images are not readable by ATS",
        "impact": -2,
    },
    "headers_footers": {
        "description": "Important info in headers/footers may be missed",
        "impact": -1,
    },
    "fancy_fonts": {
        "description": "Non-standard fonts may cause parsing issues",
        "impact": -1,
    },
}

# Education level mapping
EDUCATION_LEVELS: dict[str, int] = {
    # Highest to lowest
    "phd": 6,
    "doctorate": 6,
    "doutorado": 6,
    "masters": 5,
    "master's": 5,
    "mba": 5,
    "mestrado": 5,
    "bachelors": 4,
    "bachelor's": 4,
    "bacharelado": 4,
    "graduacao": 4,
    "graduação": 4,
    "associate": 3,
    "tecnologo": 3,
    "tecnólogo": 3,
    "bootcamp": 2,
    "certification": 2,
    "certificacao": 2,
    "high school": 1,
    "ensino medio": 1,
    "ensino médio": 1,
}


def calculate_ats_component_scores(
    resume_data: dict[str, Any],
    job_data: dict[str, Any],
    role_type: str = "technical",
) -> dict[str, Any]:
    """
    Calculate ATS score components.

    Args:
        resume_data: Parsed resume with skills, experience, education
        job_data: Job requirements with required/preferred skills
        role_type: Type of role for weight adjustment

    Returns:
        Dict with component scores and total
    """
    # Get role-specific weights
    weights = ROLE_WEIGHT_ADJUSTMENTS.get(role_type, ROLE_WEIGHT_ADJUSTMENTS["technical"])

    scores = {}

    # Skills score
    skills_score = _calculate_skills_score(
        resume_data.get("skills", []),
        job_data.get("requirements", []),
        job_data.get("preferred_skills", []),
    )
    scores["skills"] = {
        "score": skills_score,
        "max": ATS_WEIGHTS["skills"]["max_points"],
        "weighted": skills_score * weights["skills"] / ATS_WEIGHTS["skills"]["weight"],
    }

    # Experience score
    exp_score = _calculate_experience_score(
        resume_data.get("total_experience_years", 0),
        job_data.get("min_experience_years", 0),
    )
    scores["experience"] = {
        "score": exp_score,
        "max": ATS_WEIGHTS["experience"]["max_points"],
        "weighted": exp_score * weights["experience"] / ATS_WEIGHTS["experience"]["weight"],
    }

    # Education score
    edu_score = _calculate_education_score(
        resume_data.get("education", []),
        job_data.get("education_requirements", []),
    )
    scores["education"] = {
        "score": edu_score,
        "max": ATS_WEIGHTS["education"]["max_points"],
        "weighted": edu_score * weights["education"] / ATS_WEIGHTS["education"]["weight"],
    }

    # Certifications score
    cert_score = _calculate_certifications_score(
        resume_data.get("certifications", []),
        job_data.get("requirements", []) + job_data.get("preferred_skills", []),
    )
    scores["certifications"] = {
        "score": cert_score,
        "max": ATS_WEIGHTS["certifications"]["max_points"],
        "weighted": cert_score * weights["certifications"] / ATS_WEIGHTS["certifications"]["weight"],
    }

    # Keywords score
    keywords_score = _calculate_keywords_score(
        resume_data,
        job_data.get("keywords", []),
    )
    scores["keywords"] = {
        "score": keywords_score,
        "max": ATS_WEIGHTS["keywords"]["max_points"],
        "weighted": keywords_score * weights["keywords"] / ATS_WEIGHTS["keywords"]["weight"],
    }

    # Calculate total
    total = sum(s["weighted"] for s in scores.values())

    return {
        "total_score": round(total, 1),
        "component_scores": scores,
        "weights_used": weights,
        "role_type": role_type,
    }


def _calculate_skills_score(
    resume_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> float:
    """Calculate skills match score."""
    if not required_skills:
        return ATS_WEIGHTS["skills"]["max_points"] * 0.5  # Partial score if no requirements

    resume_skills_lower = {s.lower() for s in resume_skills}

    # Required skills (70% of skill points)
    required_matched = sum(
        1 for skill in required_skills
        if skill.lower() in resume_skills_lower or _fuzzy_skill_match(skill, resume_skills_lower)
    )
    required_ratio = required_matched / len(required_skills) if required_skills else 1.0

    # Preferred skills (30% of skill points)
    preferred_matched = sum(
        1 for skill in preferred_skills
        if skill.lower() in resume_skills_lower or _fuzzy_skill_match(skill, resume_skills_lower)
    )
    preferred_ratio = preferred_matched / len(preferred_skills) if preferred_skills else 1.0

    subcats = ATS_WEIGHTS["skills"]["subcategories"]
    score = (
        required_ratio * subcats["required_skills"] +
        preferred_ratio * subcats["preferred_skills"]
    ) * ATS_WEIGHTS["skills"]["max_points"]

    return round(score, 1)


def _fuzzy_skill_match(skill: str, resume_skills: set[str]) -> bool:
    """Check for fuzzy skill match (partial match or common variations)."""
    skill_lower = skill.lower()

    # Check for partial matches
    for resume_skill in resume_skills:
        if skill_lower in resume_skill or resume_skill in skill_lower:
            return True

        # Check common variations
        if skill_lower.replace("-", " ") in resume_skill:
            return True
        if skill_lower.replace(" ", "") in resume_skill.replace(" ", ""):
            return True

    return False


def _calculate_experience_score(candidate_years: float, required_years: int) -> float:
    """Calculate experience match score."""
    if required_years == 0:
        return ATS_WEIGHTS["experience"]["max_points"]  # Full score if no requirement

    thresholds = ATS_WEIGHTS["experience"]["thresholds"]

    if candidate_years >= required_years:
        multiplier = thresholds["exceeds"]
    elif candidate_years >= required_years - 0.5:
        multiplier = thresholds["meets"]
    elif candidate_years >= required_years - 1:
        multiplier = thresholds["close"]
    elif candidate_years >= required_years - 2:
        multiplier = thresholds["partial"]
    else:
        multiplier = thresholds["insufficient"]

    return round(ATS_WEIGHTS["experience"]["max_points"] * multiplier, 1)


def _calculate_education_score(
    resume_education: list[dict],
    required_education: list[str],
) -> float:
    """Calculate education match score."""
    if not required_education:
        return ATS_WEIGHTS["education"]["max_points"] * 0.8  # Default good score

    # Find highest education level in resume
    highest_level = 0
    for edu in resume_education:
        degree = (edu.get("degree") or "").lower()
        for level_name, level_value in EDUCATION_LEVELS.items():
            if level_name in degree:
                highest_level = max(highest_level, level_value)

    # Find required education level
    required_level = 0
    for req in required_education:
        req_lower = req.lower()
        for level_name, level_value in EDUCATION_LEVELS.items():
            if level_name in req_lower:
                required_level = max(required_level, level_value)

    if required_level == 0:
        return ATS_WEIGHTS["education"]["max_points"] * 0.8

    if highest_level >= required_level:
        multiplier = 1.0
    elif highest_level == required_level - 1:
        multiplier = 0.8
    elif highest_level == required_level - 2:
        multiplier = 0.6
    else:
        multiplier = 0.4

    return round(ATS_WEIGHTS["education"]["max_points"] * multiplier, 1)


def _calculate_certifications_score(
    resume_certs: list[dict],
    job_requirements: list[str],
) -> float:
    """Calculate certifications score."""
    if not resume_certs:
        return 0.0

    max_points = ATS_WEIGHTS["certifications"]["max_points"]
    bonus_per_cert = ATS_WEIGHTS["certifications"]["bonus_per_cert"]

    # Check for relevant certifications
    relevant_count = 0
    job_keywords = " ".join(job_requirements).lower()

    for cert in resume_certs:
        cert_name = (cert.get("name") or cert if isinstance(cert, str) else "").lower()
        # Check if cert is relevant to job
        if any(keyword in cert_name for keyword in job_keywords.split()):
            relevant_count += 1
        elif _is_valuable_certification(cert_name):
            relevant_count += 0.5  # Partial credit for valuable certs

    score = min(max_points, relevant_count * bonus_per_cert)
    return round(score, 1)


def _is_valuable_certification(cert_name: str) -> bool:
    """Check if certification is generally valuable."""
    valuable_certs = [
        "aws", "azure", "gcp", "google cloud",
        "kubernetes", "cka", "ckad",
        "terraform", "docker",
        "pmp", "scrum", "csm", "psm",
        "cissp", "cism", "security+",
        "ceh", "oscp",
        "comptia", "cisco", "ccna", "ccnp",
    ]
    return any(cert in cert_name for cert in valuable_certs)


def _calculate_keywords_score(resume_data: dict, job_keywords: list[str]) -> float:
    """Calculate keyword match score."""
    if not job_keywords:
        return ATS_WEIGHTS["keywords"]["max_points"] * 0.6  # Default moderate score

    # Build resume text for keyword search
    resume_text = " ".join([
        " ".join(resume_data.get("skills", [])),
        " ".join(exp.get("description", "") for exp in resume_data.get("experiences", [])),
        " ".join(exp.get("title", "") for exp in resume_data.get("experiences", [])),
    ]).lower()

    matched = sum(1 for kw in job_keywords if kw.lower() in resume_text)
    ratio = matched / len(job_keywords)

    return round(ATS_WEIGHTS["keywords"]["max_points"] * ratio, 1)


def detect_format_issues(resume_text: str) -> list[dict[str, Any]]:
    """Detect potential ATS format issues in resume text."""
    issues = []

    # Check for special characters
    if re.search(FORMAT_ISSUES["special_characters"]["pattern"], resume_text):
        issues.append({
            "issue": "special_characters",
            "description": FORMAT_ISSUES["special_characters"]["description"],
            "impact": FORMAT_ISSUES["special_characters"]["impact"],
        })

    return issues


def get_keyword_weight(keyword: str) -> str:
    """Get the weight/importance of a keyword."""
    keyword_lower = keyword.lower()

    for category, data in KEYWORD_CATEGORIES.items():
        if keyword_lower in [ex.lower() for ex in data["examples"]]:
            return data["weight"]

    return "medium"


def extract_contact_info(text: str) -> dict[str, Optional[str]]:
    """Extract contact information from resume text."""
    contact_info = {}

    for contact_type, pattern in CONTACT_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contact_info[contact_type] = match.group()
        else:
            contact_info[contact_type] = None

    return contact_info
