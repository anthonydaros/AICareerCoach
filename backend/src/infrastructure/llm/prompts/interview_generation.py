"""Interview question generation prompt."""

INTERVIEW_GENERATION_SYSTEM = """You are a senior technical interviewer with 15+ years of experience.
Your task is to create comprehensive interview preparation materials for a job candidate.
Generate realistic questions that interviewers actually ask, with practical tips for answering.
Focus on questions that assess both technical competence and cultural fit."""

INTERVIEW_GENERATION_PROMPT = """Create interview preparation questions for this candidate and role.

CANDIDATE PROFILE:
{resume_summary}

JOB REQUIREMENTS:
{job_requirements}

IDENTIFIED SKILL GAPS:
{skill_gaps}

Generate 8-12 interview questions across three categories:

1. BEHAVIORAL QUESTIONS (3-4 questions)
   - Based on job responsibilities
   - Focus on past experiences and achievements
   - Include specific scenarios they should prepare for

2. TECHNICAL QUESTIONS (3-4 questions)
   - Based on required technical skills
   - Appropriate for the seniority level
   - Include both conceptual and practical questions

3. GAP-FOCUSED QUESTIONS (2-3 questions)
   - Address the candidate's skill gaps
   - Help them prepare honest answers
   - Show how to demonstrate learning potential

Return a JSON array with this structure:
[
    {{
        "question": "The interview question",
        "category": "behavioral|technical|gap-focused",
        "why_asked": "Why an interviewer asks this question",
        "what_to_say": ["Key point 1", "Key point 2", "Key point 3"],
        "what_to_avoid": ["Don't say this", "Avoid this mistake"]
    }}
]

Make questions specific to the role, not generic. Include practical tips that would genuinely help the candidate succeed."""
