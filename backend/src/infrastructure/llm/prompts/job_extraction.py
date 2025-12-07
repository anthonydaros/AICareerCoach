"""Job posting extraction prompt."""

JOB_EXTRACTION_SYSTEM = """You are an expert job posting analyzer. Your task is to extract structured requirements from job posting text.
You must return a valid JSON object with the exact schema specified.
Carefully distinguish between:
- Required skills (must-have)
- Preferred/nice-to-have skills
- Keywords that appear throughout the posting

Pay attention to phrases like:
- "Required", "Must have", "Essential" -> is_required: true
- "Preferred", "Nice to have", "Bonus", "Plus" -> is_required: false"""

JOB_EXTRACTION_PROMPT = """Extract structured information from this job posting and return as JSON.

Job Posting:
{job_text}

Return a JSON object with this exact structure:
{{
    "title": "job title",
    "company": "company name or null if not mentioned",
    "requirements": [
        {{
            "skill": "skill name (normalized)",
            "min_years": null or minimum years required,
            "is_required": true for required, false for nice-to-have
        }}
    ],
    "preferred_skills": ["nice-to-have skills not in requirements"],
    "keywords": ["important keywords from the posting"],
    "min_experience_years": minimum total experience required (integer),
    "education_requirements": ["CS degree", "Bachelor's", etc.]
}}

Important:
- Extract the exact job title as written
- Distinguish required vs preferred skills carefully
- Include technology-specific keywords (Python, AWS, Docker, etc.)
- Extract education requirements even if flexible
- min_experience_years should be the minimum mentioned (e.g., "3-5 years" -> 3)"""
