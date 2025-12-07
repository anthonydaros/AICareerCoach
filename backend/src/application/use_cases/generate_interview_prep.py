"""Generate Interview Prep Use Case."""

from typing import Any, Optional
from collections import defaultdict

from src.domain.entities.analysis_result import InterviewQuestion, InterviewPrep, StarMethod
from src.infrastructure.llm import OpenAIGateway


class GenerateInterviewPrepUseCase:
    """Use case for generating comprehensive interview preparation."""

    # Standard preparation tips
    PREPARATION_TIPS = [
        "Research the company's recent news, products, and culture before the interview",
        "Prepare 2-3 specific examples for each type of behavioral question using the STAR method",
        "Practice explaining your most complex projects in simple, non-technical terms",
        "Prepare thoughtful questions that show genuine interest in the role and company",
        "Review the job description and map your experiences to each requirement",
        "Practice whiteboard/coding problems if technical interviews are expected",
        "Get a good night's sleep and arrive 10-15 minutes early",
        "Bring copies of your resume and a notebook for taking notes",
    ]

    # Seniority-specific preparation tips (P2.3)
    SENIORITY_TIPS = {
        "intern": [
            "Focus on demonstrating eagerness to learn and adaptability",
            "Prepare questions about mentorship and learning opportunities",
            "Have examples of academic projects or personal learning initiatives",
        ],
        "entry": [
            "Prepare to discuss relevant coursework and side projects",
            "Show enthusiasm for growth and willingness to learn quickly",
            "Research the tech stack and prepare basic understanding questions",
        ],
        "junior": [
            "Prepare examples showing rapid learning and problem-solving",
            "Be ready to discuss how you handle feedback and iterate",
            "Show awareness of best practices even if still learning them",
        ],
        "mid": [
            "Prepare concrete examples of independent problem-solving",
            "Be ready to discuss trade-offs in your technical decisions",
            "Show how you've mentored others or improved team processes",
        ],
        "senior": [
            "Prepare examples of technical leadership and architectural decisions",
            "Be ready to discuss how you've influenced team direction",
            "Show system-level thinking and cross-team collaboration examples",
        ],
        "lead": [
            "Prepare examples of team building and talent development",
            "Discuss how you balance hands-on work with leadership duties",
            "Show how you've handled technical disagreements and built consensus",
        ],
        "staff": [
            "Prepare examples of organization-wide technical impact",
            "Discuss your approach to solving ambiguous, cross-cutting problems",
            "Show how you've influenced technical strategy beyond your team",
        ],
        "principal": [
            "Prepare to discuss your technical vision and industry perspective",
            "Show examples of company-wide initiatives you've driven",
            "Discuss how you balance innovation with practical constraints",
        ],
        "director": [
            "Prepare examples of building and scaling engineering organizations",
            "Discuss your approach to aligning technical and business strategy",
            "Show how you've developed leaders and created succession plans",
        ],
        "executive": [
            "Prepare to discuss organizational transformation examples",
            "Show how you've built culture and defined engineering values",
            "Discuss board-level communication and stakeholder management",
        ],
    }

    # Questions to ask interviewer by category
    QUESTIONS_TO_ASK = {
        "role": [
            "What does success look like in this role in the first 90 days?",
            "What are the biggest challenges facing the team right now?",
            "How does this role contribute to the company's overall goals?",
        ],
        "team": [
            "Can you tell me about the team I'd be working with?",
            "How does the team approach collaboration and code reviews?",
            "What's the on-call rotation like for this team?",
        ],
        "growth": [
            "What growth opportunities are available for someone in this role?",
            "How does the company support professional development?",
            "What's the typical career path for this position?",
        ],
        "company": [
            "What do you enjoy most about working here?",
            "How would you describe the company culture?",
            "What's the company's approach to work-life balance?",
        ],
    }

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(
        self,
        resume_summary: str,
        job_summary: str,
        skill_gaps: list[str],
        matched_skills: Optional[list[str]] = None,
        job_title: Optional[str] = None,
        seniority_level: Optional[str] = None,
    ) -> InterviewPrep:
        """
        Generate comprehensive interview preparation.

        Args:
            resume_summary: Summary of candidate's resume
            job_summary: Summary of job requirements
            skill_gaps: List of skills the candidate is missing
            matched_skills: Optional list of matched skills
            job_title: Optional job title for context
            seniority_level: Optional seniority level for difficulty adjustment (P2.3)

        Returns:
            InterviewPrep with questions, STAR guidance, and tips
        """
        # Detect seniority from job title if not provided
        detected_seniority = seniority_level or self._detect_seniority(job_title)

        # Generate questions using LLM with seniority context
        questions_data = await self.llm_gateway.generate_interview_questions(
            resume_summary=resume_summary,
            job_summary=job_summary,
            skill_gaps=skill_gaps,
            seniority_level=detected_seniority,
        )

        # Parse and enhance questions
        questions = self._parse_questions(questions_data, resume_summary, skill_gaps)

        # Organize questions by category
        questions_by_category = self._organize_by_category(questions)

        # Select preparation tips with seniority context
        preparation_tips = self._get_preparation_tips(skill_gaps, job_title, detected_seniority)

        # Select questions to ask interviewer
        questions_to_ask = self._get_questions_to_ask(job_title, detected_seniority)

        return InterviewPrep(
            questions=questions,
            questions_by_category=questions_by_category,
            preparation_tips=preparation_tips,
            questions_to_ask_interviewer=questions_to_ask,
        )

    def _parse_questions(
        self,
        questions_data: list[dict[str, Any]],
        resume_summary: str,
        skill_gaps: list[str],
    ) -> list[InterviewQuestion]:
        """Parse questions from LLM response with STAR guidance."""
        questions = []
        for q in questions_data:
            if not isinstance(q, dict):
                continue

            question_text = q.get("question", "")
            if not question_text:
                continue

            category = q.get("category", "general").lower()

            # Generate your_angle based on the question and resume
            your_angle = self._generate_your_angle(question_text, category, resume_summary)

            # Generate STAR guidance for behavioral questions
            star_guidance = None
            if category == "behavioral":
                star_guidance = self._generate_star_guidance(question_text)

            questions.append(InterviewQuestion(
                question=question_text,
                category=category,
                why_asked=q.get("why_asked", ""),
                what_to_say=q.get("what_to_say", []),
                what_to_avoid=q.get("what_to_avoid", []),
                your_angle=your_angle,
                star_guidance=star_guidance,
            ))

        return questions

    def _generate_your_angle(
        self,
        question: str,
        category: str,
        resume_summary: str,
    ) -> str:
        """Generate approach angle for the question based on candidate's background."""
        question_lower = question.lower()

        if category == "behavioral":
            return (
                "Use the STAR method to structure your answer. Choose a specific example "
                "from your experience that demonstrates the skill being asked about. "
                "Focus on YOUR actions and quantify the results if possible."
            )
        elif category == "technical":
            return (
                "Start with the fundamentals and build up to complexity. If you're unsure, "
                "think out loud and show your problem-solving process. It's okay to ask "
                "clarifying questions before diving into the solution."
            )
        elif "weakness" in question_lower or "improve" in question_lower:
            return (
                "Choose a real weakness but one you're actively working to improve. "
                "Focus on the steps you've taken to address it and show self-awareness. "
                "Avoid cliche answers like 'I'm a perfectionist'."
            )
        elif "why" in question_lower and ("company" in question_lower or "role" in question_lower):
            return (
                "Show you've done your research. Reference specific aspects of the company, "
                "product, or role that genuinely interest you. Connect your career goals "
                "to what this opportunity offers."
            )
        elif "tell me about yourself" in question_lower:
            return (
                "Keep it to 2-3 minutes. Structure as: current role, key achievements, "
                "why you're interested in this opportunity. Make it a story, not a resume recitation."
            )
        else:
            return (
                "Be specific and use concrete examples. Structure your answer clearly "
                "and stay focused on what's most relevant to the question."
            )

    def _generate_star_guidance(self, question: str) -> StarMethod:
        """Generate STAR method guidance for behavioral questions."""
        question_lower = question.lower()

        # Default STAR guidance - can be customized based on question type
        if "conflict" in question_lower or "disagree" in question_lower:
            return StarMethod(
                situation="Describe a specific professional disagreement or conflict (keep it professional, not personal)",
                task="Explain your role and what needed to be resolved",
                action="Detail how YOU approached the situation - focus on communication, compromise, and professionalism",
                result="Share the outcome, what you learned, and how you'd handle it differently if needed",
            )
        elif "failure" in question_lower or "mistake" in question_lower:
            return StarMethod(
                situation="Choose a real failure but not something catastrophic",
                task="Explain what you were trying to accomplish",
                action="Describe what went wrong and take ownership without blaming others",
                result="Focus on what you learned and how you've applied that lesson since",
            )
        elif "lead" in question_lower or "team" in question_lower:
            return StarMethod(
                situation="Set the context - team size, project type, and timeline",
                task="Explain your leadership responsibilities and goals",
                action="Describe specific leadership actions: delegation, motivation, conflict resolution",
                result="Quantify the outcome: project success, team growth, metrics improved",
            )
        elif "challenge" in question_lower or "difficult" in question_lower:
            return StarMethod(
                situation="Describe a genuinely challenging situation (technical or interpersonal)",
                task="Explain why it was challenging and what was at stake",
                action="Detail your problem-solving approach step by step",
                result="Share the outcome and what made your approach effective",
            )
        else:
            return StarMethod(
                situation="Set the scene briefly - when, where, who was involved",
                task="Explain your specific responsibility or goal",
                action="Describe what YOU did (use 'I' not 'we') with specific details",
                result="Quantify the outcome if possible - numbers, percentages, time saved",
            )

    def _organize_by_category(
        self,
        questions: list[InterviewQuestion],
    ) -> dict[str, list[InterviewQuestion]]:
        """Organize questions by category."""
        by_category = defaultdict(list)

        for q in questions:
            category = q.category.lower()
            # Normalize category names
            if category in ["screen", "screening"]:
                category = "screening"
            elif category in ["tech", "technical", "coding"]:
                category = "technical"
            elif category in ["behavior", "behavioral", "soft"]:
                category = "behavioral"
            elif category in ["curve", "curveball", "tricky"]:
                category = "curveball"
            else:
                category = "general"

            by_category[category].append(q)

        return dict(by_category)

    def _detect_seniority(self, job_title: Optional[str]) -> str:
        """Detect seniority level from job title."""
        if not job_title:
            return "mid"

        title_lower = job_title.lower()

        # Executive level
        if any(word in title_lower for word in ["cto", "ceo", "cio", "vp ", "vice president", "chief"]):
            return "executive"
        # Director level
        if "director" in title_lower:
            return "director"
        # Principal level
        if "principal" in title_lower or "distinguished" in title_lower:
            return "principal"
        # Staff level
        if "staff" in title_lower:
            return "staff"
        # Lead level
        if "lead" in title_lower or "tech lead" in title_lower or "team lead" in title_lower:
            return "lead"
        # Senior level
        if "senior" in title_lower or "sr." in title_lower or "sr " in title_lower:
            return "senior"
        # Junior level
        if "junior" in title_lower or "jr." in title_lower or "jr " in title_lower:
            return "junior"
        # Entry level
        if "entry" in title_lower or "associate" in title_lower or "trainee" in title_lower:
            return "entry"
        # Intern
        if "intern" in title_lower or "estágio" in title_lower or "estagiário" in title_lower:
            return "intern"

        return "mid"

    def _get_preparation_tips(
        self,
        skill_gaps: list[str],
        job_title: Optional[str] = None,
        seniority_level: str = "mid",
    ) -> list[str]:
        """Get relevant preparation tips with seniority context."""
        tips = list(self.PREPARATION_TIPS)

        # Add seniority-specific tips (P2.3)
        seniority_tips = self.SENIORITY_TIPS.get(seniority_level.lower(), [])
        tips.extend(seniority_tips)

        # Add tips based on skill gaps
        if skill_gaps:
            tips.append(
                f"Be prepared to discuss how you'd learn: {', '.join(skill_gaps[:3])}. "
                "Show enthusiasm and a plan for filling these gaps."
            )

        # Add role-specific tips
        if job_title:
            title_lower = job_title.lower()
            if "manager" in title_lower:
                tips.append(
                    "Prepare examples of team building, performance management, and conflict resolution"
                )
            if "architect" in title_lower:
                tips.append(
                    "Prepare to discuss system design decisions, trade-offs, and scalability considerations"
                )

        return tips[:12]  # Return top 12 tips (expanded for seniority context)

    def _get_questions_to_ask(
        self,
        job_title: Optional[str] = None,
        seniority_level: str = "mid",
    ) -> list[str]:
        """Get questions candidate should ask the interviewer with seniority context."""
        questions = []

        # Add one from each category
        for category, q_list in self.QUESTIONS_TO_ASK.items():
            questions.append(q_list[0])

        # Add seniority-specific questions (P2.3)
        seniority_lower = seniority_level.lower()
        if seniority_lower in ["intern", "entry", "junior"]:
            questions.extend([
                "What does the onboarding process look like for new team members?",
                "How does the team support professional development for early-career engineers?",
            ])
        elif seniority_lower in ["senior", "lead"]:
            questions.extend([
                "What's the balance between hands-on coding and technical leadership in this role?",
                "What are the biggest technical challenges the team is facing right now?",
            ])
        elif seniority_lower in ["staff", "principal"]:
            questions.extend([
                "How does engineering influence product and business strategy here?",
                "What's the process for driving technical initiatives across teams?",
            ])
        elif seniority_lower in ["director", "executive"]:
            questions.extend([
                "How do you measure engineering team health and productivity?",
                "What's the company's approach to technical investment vs. feature delivery?",
            ])

        # Add role-specific questions
        if job_title:
            title_lower = job_title.lower()
            if "remote" in title_lower:
                questions.append(
                    "How does the team maintain collaboration and communication remotely?"
                )
            if "architect" in title_lower:
                questions.append(
                    "How are architectural decisions made and documented?"
                )

        return questions[:8]  # Return top 8 questions (expanded for seniority)
