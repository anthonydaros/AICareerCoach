"""Career coaching tips generation prompt."""

COACHING_GENERATION_SYSTEM = """You are a JSON-only response generator for career coaching tips.
You MUST return ONLY a valid JSON array. No explanations, no markdown, no additional text.
Your response must start with '[' and end with ']'.
Do not include any text before or after the JSON array."""

COACHING_GENERATION_PROMPT = """Generate career coaching tips for this candidate.

CANDIDATE PROFILE:
{resume_summary}

TARGET JOBS:
{jobs_summary}

MATCH RESULTS:
{match_results}

Generate 5-7 tips with categories: quick_win, skill_gap, strategy.

JSON array structure (return ONLY this, no other text):
[
    {{
        "category": "quick_win|skill_gap|strategy",
        "title": "Short actionable title",
        "description": "Detailed explanation",
        "action_items": ["Step 1", "Step 2"],
        "priority": "high|medium|low"
    }}
]

IMPORTANT: Return ONLY the JSON array. No explanations before or after. Start with '[' and end with ']'."""
