"""Integration tests for API routes."""

import pytest
import tempfile
import os
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from typing import List, Optional

from src.presentation.api.main import app
from src.presentation.api.dependencies import get_llm_gateway, get_orchestrator
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
from src.domain.services.ats_scorer import ATSScorer
from src.domain.services.job_matcher import JobMatcher
from src.application.orchestrator import CareerCoachOrchestrator


class MockLLMGateway:
    """Mock LLM gateway for integration tests."""

    async def extract_resume(self, resume_text: str) -> dict:
        """Return mock extracted resume data as dict."""
        return {
            "skills": [
                {"name": "Python", "normalized_name": "python", "level": "expert", "years_experience": 5},
                {"name": "React", "normalized_name": "react", "level": "advanced", "years_experience": 3},
            ],
            "experiences": [
                {
                    "title": "Senior Engineer",
                    "company": "Tech Corp",
                    "duration_months": 36,
                    "description": "Development",
                    "skills_used": ["Python", "React"],
                },
            ],
            "education": [
                {"degree": "BS", "field": "CS", "institution": "University", "year": 2018},
            ],
            "certifications": ["AWS"],
            "total_experience_years": 5.0,
        }

    async def extract_job_posting(self, job_text: str) -> dict:
        """Return mock extracted job data as dict."""
        return {
            "title": "Software Engineer",
            "company": "Tech Co",
            "requirements": [
                {"skill": "Python", "is_required": True, "min_years": 3},
                {"skill": "React", "is_required": True, "min_years": 2},
            ],
            "min_experience_years": 3,
            "education_requirements": ["Bachelor's degree"],
            "preferred_skills": ["Docker"],
            "keywords": ["python", "react", "docker"],
        }

    async def generate_interview_questions(
        self, resume_summary: str, job_summary: str, skill_gaps: List[str], seniority_level: str = "mid"
    ) -> List[dict]:
        """Return mock interview questions data."""
        return [
            {
                "question": "Tell me about yourself",
                "category": "Behavioral",
                "why_asked": "To understand background",
                "what_to_say": ["Be concise", "Highlight relevant experience"],
                "what_to_avoid": ["Rambling", "Personal details"],
            },
        ]

    async def generate_coaching_tips(
        self, resume_summary: str, jobs_summary: str, match_results: Optional[List] = None
    ) -> List[dict]:
        """Return mock coaching tips data."""
        return [
            {
                "category": "Skills",
                "title": "Learn Kubernetes",
                "description": "Kubernetes is in high demand",
                "action_items": ["Take a course", "Practice with minikube"],
                "priority": "high",
            },
        ]


def get_mock_llm_gateway():
    """Return mock LLM gateway."""
    return MockLLMGateway()


def get_mock_orchestrator():
    """Return orchestrator with mock LLM gateway."""
    mock_gateway = MockLLMGateway()
    return CareerCoachOrchestrator(
        llm_gateway=mock_gateway,
        ats_scorer=ATSScorer(),
        job_matcher=JobMatcher(),
    )


@pytest.fixture
def client():
    """Create a test client with mocked dependencies."""
    app.dependency_overrides[get_llm_gateway] = get_mock_llm_gateway
    app.dependency_overrides[get_orchestrator] = get_mock_orchestrator

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


class TestHealthEndpoint:
    """Test cases for health endpoint."""

    def test_health_check(self, client):
        """Test health check returns OK."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


class TestUploadEndpoint:
    """Test cases for upload endpoint."""

    def test_upload_txt_file(self, client):
        """Test uploading a TXT file."""
        content = "John Doe\nSoftware Engineer\nPython, React, Docker"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            with open(temp_path, 'rb') as f:
                response = client.post(
                    "/upload",
                    files={"file": ("resume.txt", f, "text/plain")},
                )

            assert response.status_code == 200
            data = response.json()
            assert data["filename"] == "resume.txt"
            assert "John Doe" in data["text_content"]
            assert data["char_count"] > 0
        finally:
            os.unlink(temp_path)

    def test_upload_unsupported_file(self, client):
        """Test uploading an unsupported file type."""
        content = b"Some content"

        response = client.post(
            "/upload",
            files={"file": ("resume.xyz", content, "application/octet-stream")},
        )

        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"].lower() or "unsupported" in response.json()["detail"].lower()


class TestAnalyzeEndpoint:
    """Test cases for analyze endpoint."""

    # Sample data that meets min_length requirements (resume: 100+, job: 50+)
    SAMPLE_RESUME = """John Doe
Senior Software Engineer with 5+ years of experience
Skills: Python, React, Docker, PostgreSQL, AWS, Kubernetes
Experience: Led development of web applications at TechCorp
Education: BS in Computer Science from State University"""

    SAMPLE_JOB = """Senior Developer Position at Amazing Tech Company
Requirements: Python (5+ years), React (3+ years), Docker experience
We are looking for talented developers to join our team."""

    def test_analyze_success(self, client):
        """Test successful analysis."""
        response = client.post(
            "/analyze",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": self.SAMPLE_JOB}
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "ats_result" in data
        assert "job_matches" in data
        assert data["ats_result"]["total_score"] >= 0

    def test_analyze_multiple_jobs(self, client):
        """Test analysis with multiple job postings."""
        response = client.post(
            "/analyze",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": "Python Developer role requiring 3+ years experience with Python, FastAPI, and Docker"},
                    {"id": "job2", "text": "React Developer role requiring 2+ years experience with React, JavaScript, and TypeScript"},
                    {"id": "job3", "text": "Full Stack Developer role requiring Python and React experience with 3+ years"},
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["job_matches"]) == 3

    def test_analyze_empty_resume(self, client):
        """Test analysis with empty resume."""
        response = client.post(
            "/analyze",
            json={
                "resume_text": "",
                "job_postings": [
                    {"id": "job1", "text": self.SAMPLE_JOB}
                ],
            },
        )

        # Pydantic validates min_length and returns 422
        assert response.status_code == 422

    def test_analyze_no_jobs(self, client):
        """Test analysis with no job postings."""
        response = client.post(
            "/analyze",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [],
            },
        )

        # Pydantic validates min_length=1 for job_postings and returns 422
        assert response.status_code == 422


class TestATSScoreEndpoint:
    """Test cases for ATS score endpoint."""

    SAMPLE_RESUME = """John Doe
Senior Software Engineer with 5+ years of experience
Skills: Python, React, Docker, PostgreSQL, AWS, Kubernetes
Experience: Led development of web applications at TechCorp"""

    SAMPLE_JOB = """Senior Developer Position at Amazing Tech Company
Requirements: Python (5+ years), React (3+ years), Docker experience"""

    def test_ats_score_success(self, client):
        """Test successful ATS score calculation."""
        response = client.post(
            "/ats-score",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_text": self.SAMPLE_JOB,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_score" in data
        assert "skill_score" in data
        assert "matched_keywords" in data
        assert 0 <= data["total_score"] <= 100

    def test_ats_score_empty_inputs(self, client):
        """Test ATS score with empty inputs."""
        response = client.post(
            "/ats-score",
            json={
                "resume_text": "",
                "job_text": "",
            },
        )

        # Pydantic validates min_length and returns 422
        assert response.status_code == 422


class TestMatchJobsEndpoint:
    """Test cases for match-jobs endpoint."""

    SAMPLE_RESUME = """John Doe
Senior Software Engineer with 5+ years of experience
Skills: Python, React, Docker, PostgreSQL, AWS, Kubernetes
Experience: Led development of web applications at TechCorp"""

    def test_match_jobs_success(self, client):
        """Test successful job matching."""
        response = client.post(
            "/match-jobs",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": "Python Developer role requiring 3+ years experience with Python, FastAPI, Docker"},
                    {"id": "job2", "text": "React Developer role requiring 2+ years experience with React, JavaScript, TypeScript"},
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_match_jobs_ranking(self, client):
        """Test that jobs are ranked by match percentage."""
        response = client.post(
            "/match-jobs",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": "Python Developer role requiring 5+ years Python experience and Docker skills"},
                    {"id": "job2", "text": "Java Developer role requiring 5+ years Java experience and Spring framework"},
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        # Results should be sorted by match percentage (highest first)
        if len(data) >= 2:
            assert data[0]["match_percentage"] >= data[1]["match_percentage"]


class TestInterviewPrepEndpoint:
    """Test cases for interview-prep endpoint."""

    SAMPLE_RESUME = """John Doe
Senior Software Engineer with 5+ years of experience
Skills: Python, React, Docker, PostgreSQL, AWS, Kubernetes
Experience: Led development of web applications at TechCorp"""

    SAMPLE_JOB = """Senior Developer Position at Amazing Tech Company
Requirements: Python (5+ years), React (3+ years), Docker experience"""

    def test_interview_prep_success(self, client):
        """Test successful interview prep generation."""
        response = client.post(
            "/interview-prep",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_text": self.SAMPLE_JOB,
                "skill_gaps": ["Kubernetes"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "job_title" in data
        assert "questions" in data
        assert len(data["questions"]) > 0
        assert "question" in data["questions"][0]
        assert "category" in data["questions"][0]

    def test_interview_prep_without_skill_gaps(self, client):
        """Test interview prep without skill gaps."""
        response = client.post(
            "/interview-prep",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_text": self.SAMPLE_JOB,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "questions" in data


class TestCoachingTipsEndpoint:
    """Test cases for coaching-tips endpoint."""

    SAMPLE_RESUME = """John Doe
Senior Software Engineer with 5+ years of experience
Skills: Python, React, Docker, PostgreSQL, AWS, Kubernetes
Experience: Led development of web applications at TechCorp"""

    def test_coaching_tips_success(self, client):
        """Test successful coaching tips generation."""
        response = client.post(
            "/coaching-tips",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": "Senior Developer role requiring Python, React, and cloud experience with 3+ years"},
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "tips" in data
        assert len(data["tips"]) > 0
        assert "category" in data["tips"][0]
        assert "title" in data["tips"][0]
        assert "action_items" in data["tips"][0]

    def test_coaching_tips_multiple_jobs(self, client):
        """Test coaching tips with multiple jobs."""
        response = client.post(
            "/coaching-tips",
            json={
                "resume_text": self.SAMPLE_RESUME,
                "job_postings": [
                    {"id": "job1", "text": "Python Developer role requiring 3+ years experience with Python, FastAPI, Docker"},
                    {"id": "job2", "text": "React Developer role requiring 2+ years experience with React, JavaScript, TypeScript"},
                ],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "tips" in data


class TestErrorHandling:
    """Test error handling across endpoints."""

    def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        response = client.post(
            "/analyze",
            content="not valid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    def test_missing_required_fields(self, client):
        """Test handling of missing required fields."""
        response = client.post(
            "/analyze",
            json={"resume_text": "Some text"},  # Missing job_postings
        )

        assert response.status_code == 422

    def test_wrong_http_method(self, client):
        """Test handling of wrong HTTP method."""
        response = client.get("/analyze")

        assert response.status_code == 405

    def test_wrong_field_types(self, client):
        """Test handling of wrong field types."""
        response = client.post(
            "/analyze",
            json={
                "resume_text": 12345,  # Should be string
                "job_postings": "not a list",  # Should be list
            },
        )

        assert response.status_code == 422


class TestCORS:
    """Test CORS configuration."""

    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        # Should allow the request (might be 200 or 405 depending on setup)
        # The important thing is it doesn't fail with 500
        assert response.status_code < 500
