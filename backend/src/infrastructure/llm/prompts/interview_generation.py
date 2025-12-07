"""Interview question generation prompt - Optimized with seniority context."""

INTERVIEW_GENERATION_SYSTEM = """JSON-only response generator for interview prep.
Return ONLY valid JSON array. Start with '[', end with ']'.
No explanations, no markdown, no extra text."""

INTERVIEW_GENERATION_PROMPT = """Generate interview questions for this candidate and role.

CANDIDATE PROFILE:
{resume_summary}

JOB REQUIREMENTS:
{job_requirements}

SKILL GAPS:
{skill_gaps}

SENIORITY LEVEL: {seniority_level}
DIFFICULTY ADJUSTMENT: {difficulty_context}

Generate 6-8 questions with this distribution based on seniority:
- Junior/Entry: 3 behavioral, 3 technical (fundamental), 2 gap-focused
- Mid-level: 2 behavioral, 4 technical (hands-on), 2 gap-focused
- Senior/Lead: 2 behavioral (leadership), 3 technical (architecture), 2 gap-focused, 1 system design
- Staff+: 1 behavioral, 2 technical (deep), 2 system design, 2 leadership, 1 gap-focused

JSON array structure (return ONLY this):
[
    {{
        "question": "The interview question",
        "category": "behavioral|technical|gap-focused|system-design|leadership",
        "difficulty": "entry|mid|senior|staff",
        "why_asked": "What interviewer evaluates",
        "what_to_say": ["Key point 1", "Key point 2"],
        "what_to_avoid": ["Mistake 1", "Mistake 2"]
    }}
]

Return ONLY the JSON array. Start with '[', end with ']'."""


# Default context templates for different seniority levels
SENIORITY_CONTEXT = {
    "entry": "Focus on fundamentals, learning ability, and potential. Assess basic problem-solving.",
    "junior": "Test foundational skills, coding basics, and eagerness to learn. Include simple scenarios.",
    "mid": "Evaluate hands-on experience, independent problem-solving, and collaboration skills.",
    "senior": "Assess technical leadership, mentoring ability, architectural thinking, and complex problem-solving.",
    "lead": "Focus on team leadership, technical vision, cross-team collaboration, and strategic thinking.",
    "staff": "Evaluate broad technical impact, organizational influence, and ability to solve ambiguous problems.",
    "principal": "Assess company-wide technical strategy, innovation leadership, and industry expertise.",
    "director": "Focus on organizational leadership, strategy execution, and business impact.",
    "executive": "Evaluate vision setting, business strategy, and organizational transformation.",
}
