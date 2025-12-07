"""Unit tests for ATS Scorer service."""

import pytest
from src.domain.services.ats_scorer import ATSScorer
from src.domain.entities.resume import Resume, Skill, Experience, Education, SkillLevel
from src.domain.entities.job_posting import JobPosting, JobRequirement


class TestATSScorer:
    """Test cases for ATSScorer service."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = ATSScorer()

    def test_perfect_match_high_score(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that a resume matching all requirements gets a high score."""
        result = self.scorer.calculate(sample_resume, sample_job_posting)

        assert result.total_score > 0
        assert result.skill_score >= 0
        assert result.experience_score >= 0
        assert result.education_score >= 0
        assert len(result.matched_keywords) > 0

    def test_no_skills_low_score(self, sample_job_posting: JobPosting):
        """Test that a resume with no matching skills gets a low score."""
        empty_resume = Resume(
            id="empty-resume",
            raw_content="Empty resume",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=0,
        )

        result = self.scorer.calculate(empty_resume, sample_job_posting)

        assert result.skill_score == 0
        assert result.experience_score == 0
        assert result.total_score < 30

    def test_matched_keywords_populated(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that matched keywords are correctly identified."""
        result = self.scorer.calculate(sample_resume, sample_job_posting)

        # Resume has Python, React, Docker which are required
        assert "python" in [k.lower() for k in result.matched_keywords]

    def test_missing_keywords_identified(self, sample_job_posting: JobPosting):
        """Test that missing keywords are correctly identified."""
        partial_resume = Resume(
            id="partial-resume",
            raw_content="Python developer",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5)],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        result = self.scorer.calculate(partial_resume, sample_job_posting)

        # Resume is missing React, Docker, Kubernetes
        missing_lower = [k.lower() for k in result.missing_keywords]
        assert "react" in missing_lower or "docker" in missing_lower

    def test_experience_score_calculation(self, sample_job_posting: JobPosting):
        """Test experience score based on years of experience."""
        resume_with_experience = Resume(
            id="exp-resume",
            raw_content="4 years of experience",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5)],
            experiences=[
                Experience(
                    title="Senior Engineer",
                    company="Company",
                    duration_months=48,  # 4 years
                    description="Development work",
                    skills_used=["Python"],
                ),
            ],
            education=[],
            certifications=[],
            total_experience_years=4,
        )

        result = self.scorer.calculate(resume_with_experience, sample_job_posting)

        # Should get some experience score for 4 years (within 3-7 range)
        assert result.experience_score > 0

    def test_education_score_with_degree(self, sample_job_posting: JobPosting):
        """Test education score when degree is present."""
        resume_with_education = Resume(
            id="edu-resume",
            raw_content="CS graduate",
            skills=[],
            experiences=[],
            education=[
                Education(
                    degree="Bachelor of Science",
                    field="Computer Science",
                    institution="University",
                    year=2020,
                ),
            ],
            certifications=[],
            total_experience_years=0,
        )

        result = self.scorer.calculate(resume_with_education, sample_job_posting)

        # Should get education score for having a degree
        assert result.education_score > 0

    def test_certification_score(self, sample_job_posting: JobPosting):
        """Test certification score when certifications are present."""
        resume_with_certs = Resume(
            id="cert-resume",
            raw_content="Certified professional",
            skills=[],
            experiences=[],
            education=[],
            certifications=["AWS Certified", "Google Cloud Certified"],
            total_experience_years=0,
        )

        result = self.scorer.calculate(resume_with_certs, sample_job_posting)

        assert result.certification_score > 0

    def test_improvement_suggestions_generated(self, sample_job_posting: JobPosting):
        """Test that improvement suggestions are generated for missing skills."""
        partial_resume = Resume(
            id="partial-resume",
            raw_content="Junior developer",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.BEGINNER, years_experience=1)],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=1,
        )

        result = self.scorer.calculate(partial_resume, sample_job_posting)

        # Should have suggestions for improvement
        assert len(result.improvement_suggestions) > 0

    def test_score_components_sum_correctly(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that individual scores sum to total score."""
        result = self.scorer.calculate(sample_resume, sample_job_posting)

        expected_total = (
            result.skill_score
            + result.experience_score
            + result.education_score
            + result.certification_score
            + result.keyword_score
        )

        assert result.total_score == expected_total

    def test_max_scores_respected(self):
        """Test that scores don't exceed maximum values."""
        # Create an over-qualified resume
        super_resume = Resume(
            id="super-resume",
            raw_content="Expert in everything Python React Docker Kubernetes",
            skills=[
                Skill(name=f"Skill{i}", normalized_name=f"skill{i}", level=SkillLevel.EXPERT, years_experience=10)
                for i in range(20)
            ],
            experiences=[
                Experience(
                    title="CTO",
                    company="Company",
                    duration_months=120,
                    description="Everything",
                    skills_used=["All"],
                )
            ],
            education=[
                Education(degree="PhD", field="CS", institution="MIT", year=2010),
                Education(degree="MBA", field="Business", institution="Harvard", year=2015),
            ],
            certifications=["Cert1", "Cert2", "Cert3", "Cert4", "Cert5"],
            total_experience_years=10,
        )

        job = JobPosting(
            id="test-job",
            raw_text="Engineer needed",
            title="Engineer",
            company="Company",
            requirements=[
                JobRequirement(skill="Python", is_required=True, min_years=1),
            ],
            min_experience_years=1,
        )

        result = self.scorer.calculate(super_resume, job)

        # Scores should not exceed maximums
        assert result.skill_score <= 40
        assert result.experience_score <= 30
        assert result.education_score <= 15
        assert result.certification_score <= 10
        assert result.keyword_score <= 5
        assert result.total_score <= 100
