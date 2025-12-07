"""Resume extraction prompt - Optimized for accuracy and token efficiency."""

RESUME_EXTRACTION_SYSTEM = """Expert resume parser. Extract structured data as JSON.

Extract ALL skills (languages, frameworks, tools, soft skills, methodologies).
Normalize names: "JS"→"JavaScript", "K8s"→"Kubernetes", "ML"→"Machine Learning".
Skill levels: beginner (limited), intermediate (1-3yr), advanced (3-5yr), expert (5+yr/leadership).

IMPORTANT: Extract contact info (name, email, phone, linkedin, location) from the header."""

RESUME_EXTRACTION_PROMPT = """Extract structured data from this resume. Return ONLY valid JSON.

Resume:
{resume_text}

JSON Schema:
{{
    "name": "full name or null",
    "email": "email@domain.com or null",
    "phone": "phone number or null",
    "linkedin_url": "linkedin.com/in/... or null",
    "location": "City, State/Country or null",
    "skills": [
        {{
            "name": "original name",
            "normalized_name": "standardized name",
            "level": "beginner|intermediate|advanced|expert",
            "years_experience": number or null
        }}
    ],
    "experiences": [
        {{
            "title": "job title",
            "company": "company name",
            "duration_months": integer,
            "description": "brief description",
            "skills_used": ["skill1", "skill2"],
            "start_year": integer,
            "end_year": integer or null (if current)
        }}
    ],
    "education": [
        {{
            "degree": "degree type",
            "field": "field of study",
            "institution": "school name",
            "year": integer or null
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "total_experience_years": number
}}

Rules:
- Extract contact info from header (name, email, phone, linkedin, location)
- Extract ALL skills (technical + soft)
- "Present"/"Current"/"Atual" → end_year: null
- Date ranges: "2021-2024" → start_year: 2021, end_year: 2024"""
