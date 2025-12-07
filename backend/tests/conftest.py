"""Pytest configuration and fixtures."""

import pytest
from typing import Optional, List

from src.domain.entities.resume import Resume, Skill, Experience, Education, SkillLevel
from src.domain.entities.job_posting import JobPosting, JobRequirement
from src.domain.entities.analysis_result import (
    ATSResult,
    JobMatch,
    SkillGap,
    InterviewQuestion,
    CoachingTip,
    MatchLevel,
)
from src.domain.interfaces.llm_gateway import ILLMGateway


# ============================================
# Mock LLM Gateway
# ============================================


class MockLLMGateway(ILLMGateway):
    """Mock LLM gateway for testing."""

    async def extract_resume(self, text: str) -> dict:
        """Return mock resume data."""
        return {
            "skills": [
                {"name": "Python", "normalized_name": "python", "level": "expert", "years_experience": 5},
                {"name": "JavaScript", "normalized_name": "javascript", "level": "advanced", "years_experience": 3},
                {"name": "React", "normalized_name": "react", "level": "intermediate", "years_experience": 2},
                {"name": "Docker", "normalized_name": "docker", "level": "intermediate", "years_experience": 2},
                {"name": "AWS", "normalized_name": "aws", "level": "beginner", "years_experience": 1},
            ],
            "experiences": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration_months": 36,
                    "description": "Led development of web applications",
                    "skills_used": ["Python", "React", "PostgreSQL"],
                },
                {
                    "title": "Software Engineer",
                    "company": "Startup Inc",
                    "duration_months": 24,
                    "description": "Full-stack development",
                    "skills_used": ["JavaScript", "Node.js", "MongoDB"],
                },
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "institution": "State University",
                    "year": 2018,
                },
            ],
            "certifications": ["AWS Certified Developer"],
            "total_experience_years": 5.0,
        }

    async def extract_job_posting(self, text: str) -> dict:
        """Return mock job posting data."""
        return {
            "title": "Senior Software Engineer",
            "company": "Amazing Tech Co",
            "requirements": [
                {"skill": "Python", "is_required": True, "min_years": 3},
                {"skill": "React", "is_required": True, "min_years": 2},
                {"skill": "Docker", "is_required": True, "min_years": 1},
                {"skill": "Kubernetes", "is_required": False, "min_years": 1},
                {"skill": "GraphQL", "is_required": False, "min_years": 1},
            ],
            "min_experience_years": 3,
            "education_requirements": ["Bachelor's degree in CS or related field"],
            "preferred_skills": ["Kubernetes", "GraphQL"],
            "keywords": ["python", "react", "docker", "scalable", "microservices"],
        }

    async def generate_interview_questions(
        self,
        resume_summary: str,
        job_summary: str,
        skill_gaps: List[str],
        seniority_level: str = "mid",
    ) -> List[dict]:
        """Return mock interview questions."""
        return [
            {
                "question": "Tell me about a time you led a complex technical project.",
                "category": "Behavioral",
                "why_asked": "Assesses leadership and project management skills",
                "what_to_say": [
                    "Describe specific project with measurable outcomes",
                    "Explain your role and decision-making process",
                    "Highlight collaboration with team members",
                ],
                "what_to_avoid": [
                    "Vague or general answers",
                    "Taking sole credit for team efforts",
                    "Focusing only on technical details",
                ],
            },
            {
                "question": "How would you design a scalable microservices architecture?",
                "category": "Technical",
                "why_asked": "Tests system design knowledge",
                "what_to_say": [
                    "Start with requirements clarification",
                    "Discuss service boundaries and communication",
                    "Address scaling, monitoring, and fault tolerance",
                ],
                "what_to_avoid": [
                    "Jumping to implementation without design",
                    "Ignoring non-functional requirements",
                    "Over-engineering the solution",
                ],
            },
        ]

    async def generate_coaching_tips(
        self,
        resume_summary: str,
        jobs_summary: str,
        match_results: List[dict],
    ) -> List[dict]:
        """Return mock coaching tips."""
        return [
            {
                "category": "Skills Development",
                "title": "Learn Kubernetes",
                "description": "Kubernetes is required for most senior roles. Consider getting certified.",
                "action_items": [
                    "Complete Kubernetes fundamentals course",
                    "Set up local minikube environment",
                    "Practice deploying applications",
                ],
                "priority": "high",
            },
            {
                "category": "Resume Optimization",
                "title": "Quantify Achievements",
                "description": "Add metrics to your experience descriptions for more impact.",
                "action_items": [
                    "Add performance improvements in percentages",
                    "Include team sizes and project scopes",
                    "Mention revenue or cost savings if applicable",
                ],
                "priority": "medium",
            },
        ]

    async def chat(self, messages: List[dict]) -> str:
        """Return mock chat response."""
        return "This is a mock response from the LLM."


# ============================================
# Fixtures
# ============================================


@pytest.fixture
def mock_llm_gateway() -> MockLLMGateway:
    """Provide a mock LLM gateway."""
    return MockLLMGateway()


@pytest.fixture
def sample_resume() -> Resume:
    """Provide a sample resume for testing."""
    return Resume(
        id="test-resume-1",
        raw_content="John Doe - Software Engineer with 5 years experience in Python, React, Docker.",
        skills=[
            Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5),
            Skill(name="JavaScript", normalized_name="javascript", level=SkillLevel.ADVANCED, years_experience=3),
            Skill(name="React", normalized_name="react", level=SkillLevel.INTERMEDIATE, years_experience=2),
            Skill(name="Docker", normalized_name="docker", level=SkillLevel.INTERMEDIATE, years_experience=2),
        ],
        experiences=[
            Experience(
                title="Senior Software Engineer",
                company="Tech Corp",
                duration_months=36,
                description="Led development of web applications",
                skills_used=["Python", "React"],
            ),
        ],
        education=[
            Education(
                degree="Bachelor of Science",
                field="Computer Science",
                institution="State University",
                year=2018,
            ),
        ],
        certifications=["AWS Certified Developer"],
        total_experience_years=5.0,
    )


@pytest.fixture
def sample_job_posting() -> JobPosting:
    """Provide a sample job posting for testing."""
    return JobPosting(
        id="test-job-1",
        raw_text="Senior Software Engineer position requiring Python, React, Docker. 3-7 years experience.",
        title="Senior Software Engineer",
        company="Amazing Tech Co",
        requirements=[
            JobRequirement(skill="Python", is_required=True, min_years=3),
            JobRequirement(skill="React", is_required=True, min_years=2),
            JobRequirement(skill="Docker", is_required=True, min_years=1),
            JobRequirement(skill="Kubernetes", is_required=False, min_years=1),
        ],
        min_experience_years=3,
        education_requirements=["Bachelor's degree"],
        preferred_skills=["Kubernetes"],
        keywords=["python", "react", "docker"],
    )


@pytest.fixture
def sample_resume_text() -> str:
    """Provide sample resume text for testing."""
    return """
    John Doe
    Senior Software Engineer
    john.doe@email.com

    SUMMARY
    Experienced software engineer with 5+ years of experience in web development.
    Proficient in Python, JavaScript, React, and Docker.

    EXPERIENCE
    Senior Software Engineer at Tech Corp (2020 - Present)
    - Led development of customer-facing web applications
    - Implemented CI/CD pipelines using Docker and Jenkins
    - Mentored junior developers

    Software Engineer at Startup Inc (2018 - 2020)
    - Full-stack development using React and Node.js
    - Built RESTful APIs and microservices

    EDUCATION
    Bachelor of Science in Computer Science
    State University, 2018

    SKILLS
    Python, JavaScript, TypeScript, React, Node.js, Docker, PostgreSQL, MongoDB

    CERTIFICATIONS
    AWS Certified Developer - Associate
    """


@pytest.fixture
def sample_job_text() -> str:
    """Provide sample job posting text for testing."""
    return """
    Senior Software Engineer
    Amazing Tech Co - Remote

    About the Role:
    We're looking for a Senior Software Engineer to join our growing team.
    You will design and implement scalable systems using modern technologies.

    Requirements:
    - 3-5 years of experience in software development
    - Strong proficiency in Python and React
    - Experience with Docker and containerization
    - Kubernetes experience is a plus
    - Bachelor's degree in Computer Science or equivalent

    Responsibilities:
    - Design and implement scalable backend services
    - Lead technical decisions and code reviews
    - Mentor junior developers
    - Collaborate with product and design teams

    Benefits:
    - Competitive salary ($120,000 - $160,000)
    - Health, dental, and vision insurance
    - Remote work flexibility
    - 401(k) matching
    """
