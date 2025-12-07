"""Interview question generation prompt."""

INTERVIEW_GENERATION_SYSTEM = """You are a JSON-only response generator for interview preparation.
You MUST return ONLY a valid JSON array. No explanations, no markdown, no additional text.
Your response must start with '[' and end with ']'.
Do not include any text before or after the JSON array."""

INTERVIEW_GENERATION_PROMPT = """Generate interview questions for this candidate and role.

CANDIDATE PROFILE:
{resume_summary}

JOB REQUIREMENTS:
{job_requirements}

SKILL GAPS:
{skill_gaps}

Generate 6-8 interview questions with these categories: behavioral, technical, gap-focused.

JSON array structure (return ONLY this, no other text):
[
    {{
        "question": "The interview question",
        "category": "behavioral|technical|gap-focused",
        "why_asked": "Why interviewer asks this",
        "what_to_say": ["Key point 1", "Key point 2"],
        "what_to_avoid": ["Mistake 1", "Mistake 2"]
    }}
]

IMPORTANT: Return ONLY the JSON array. No explanations before or after. Start with '[' and end with ']'."""
