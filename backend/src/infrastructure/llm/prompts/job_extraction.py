"""Job posting extraction prompt - Optimized for accuracy and token efficiency."""

JOB_EXTRACTION_SYSTEM = """Expert job posting analyzer. Extract structured data as JSON.

Distinguish: Required ("Must have", "Essential") vs Preferred ("Nice to have", "Bonus", "Plus").
Detect seniority: intern, junior, mid, senior, lead, staff, principal, director, executive.
Detect remote policy: onsite, hybrid, remote."""

JOB_EXTRACTION_PROMPT = """Extract structured data from this job posting. Return ONLY valid JSON.

Job Posting:
{job_text}

JSON Schema:
{{
    "title": "exact job title",
    "company": "company name or null",
    "seniority_level": "intern|junior|mid|senior|lead|staff|principal|director|executive or null",
    "remote_policy": "onsite|hybrid|remote|unknown",
    "location": "job location or null",
    "salary_min": integer or null,
    "salary_max": integer or null,
    "salary_currency": "USD|BRL|EUR|etc",
    "requirements": [
        {{
            "skill": "normalized skill name",
            "min_years": integer or null,
            "is_required": true|false
        }}
    ],
    "preferred_skills": ["nice-to-have not in requirements"],
    "keywords": ["tech keywords"],
    "min_experience_years": integer (minimum from range, e.g., "3-5 years" → 3),
    "education_requirements": ["degree requirements"]
}}

Rules:
- Detect seniority from title/requirements (Senior Engineer → senior, Tech Lead → lead)
- Extract salary if mentioned (annual, convert if needed)
- "Remote", "Work from home" → remote; "Hybrid" → hybrid; office-only → onsite
- "Required"/"Must have" → is_required: true
- "Preferred"/"Nice to have"/"Plus" → is_required: false"""
