"""Unit tests for Job Matcher service."""

import pytest
from src.domain.services.job_matcher import JobMatcher
from src.domain.entities.resume import Resume, Skill, Experience, Education, SkillLevel
from src.domain.entities.job_posting import JobPosting, JobRequirement
from src.domain.entities.analysis_result import MatchLevel


class TestJobMatcher:
    """Test cases for JobMatcher service."""

    def setup_method(self):
        """Set up test fixtures."""
        self.matcher = JobMatcher()

    def test_match_single_job(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test matching against a single job."""
        results = self.matcher.match_all(sample_resume, [sample_job_posting])

        assert len(results) == 1
        result = results[0]
        assert result.job_id == sample_job_posting.id
        assert result.job_title == sample_job_posting.title
        assert result.company == sample_job_posting.company
        assert 0 <= result.match_percentage <= 100
        assert result.match_level in [MatchLevel.EXCELLENT, MatchLevel.GOOD, MatchLevel.FAIR, MatchLevel.POOR]

    def test_match_multiple_jobs_ranking(self, sample_resume: Resume):
        """Test that multiple jobs are ranked by match percentage."""
        good_job = JobPosting(
            id="good-job",
            raw_text="Python Developer",
            title="Python Developer",
            company="Company A",
            requirements=[
                JobRequirement(skill="Python", is_required=True, min_years=3),
                JobRequirement(skill="JavaScript", is_required=True, min_years=2),
            ],
            min_experience_years=3,
        )

        bad_job = JobPosting(
            id="bad-job",
            raw_text="Java Developer",
            title="Java Developer",
            company="Company B",
            requirements=[
                JobRequirement(skill="Java", is_required=True, min_years=5),
                JobRequirement(skill="Spring", is_required=True, min_years=3),
                JobRequirement(skill="Microservices", is_required=True, min_years=3),
            ],
            min_experience_years=5,
        )

        results = self.matcher.match_all(sample_resume, [good_job, bad_job])

        # Results should be sorted by match percentage (highest first)
        assert len(results) == 2
        assert results[0].match_percentage >= results[1].match_percentage

    def test_best_fit_identification(self, sample_resume: Resume):
        """Test that the best fit job is correctly identified."""
        job1 = JobPosting(
            id="job1",
            raw_text="Python Developer",
            title="Python Developer",
            company="Company A",
            requirements=[
                JobRequirement(skill="Python", is_required=True, min_years=3),
            ],
            min_experience_years=2,
        )

        job2 = JobPosting(
            id="job2",
            raw_text="Full Stack Developer",
            title="Full Stack Developer",
            company="Company B",
            requirements=[
                JobRequirement(skill="Python", is_required=True, min_years=3),
                JobRequirement(skill="React", is_required=True, min_years=2),
            ],
            min_experience_years=3,
        )

        results = self.matcher.match_all(sample_resume, [job1, job2])

        # Exactly one job should be marked as best fit
        best_fit_count = sum(1 for r in results if r.is_best_fit)
        assert best_fit_count == 1

        # The best fit should be the one with highest match percentage
        best_fit = next(r for r in results if r.is_best_fit)
        assert best_fit.match_percentage == max(r.match_percentage for r in results)

    def test_matched_skills_populated(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that matched skills are correctly identified."""
        results = self.matcher.match_all(sample_resume, [sample_job_posting])
        result = results[0]

        # Resume has Python, React, Docker which are in job requirements
        matched_lower = [s.lower() for s in result.matched_skills]
        assert "python" in matched_lower

    def test_missing_skills_populated(self, sample_job_posting: JobPosting):
        """Test that missing skills are correctly identified."""
        partial_resume = Resume(
            id="partial",
            raw_content="Python developer",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5)],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        results = self.matcher.match_all(partial_resume, [sample_job_posting])
        result = results[0]

        # Resume is missing React, Docker, Kubernetes
        missing_lower = [s.lower() for s in result.missing_skills]
        assert len(missing_lower) > 0
        assert "react" in missing_lower or "docker" in missing_lower

    def test_skill_gaps_generated(self, sample_job_posting: JobPosting):
        """Test that skill gaps include learning resources."""
        partial_resume = Resume(
            id="partial",
            raw_content="Python developer",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5)],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        results = self.matcher.match_all(partial_resume, [sample_job_posting])
        result = results[0]

        # Should have skill gaps with suggestions
        assert len(result.skill_gaps) > 0
        for gap in result.skill_gaps:
            assert gap.skill
            assert gap.suggestion
            assert isinstance(gap.is_required, bool)

    def test_strengths_identified(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that candidate strengths are identified."""
        results = self.matcher.match_all(sample_resume, [sample_job_posting])
        result = results[0]

        # Should identify some strengths
        assert len(result.strengths) > 0

    def test_match_level_excellent(self):
        """Test excellent match level for high score."""
        perfect_resume = Resume(
            id="perfect",
            raw_content="Expert Python developer",
            skills=[
                Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5),
                Skill(name="React", normalized_name="react", level=SkillLevel.EXPERT, years_experience=4),
            ],
            experiences=[
                Experience(
                    title="Senior Engineer",
                    company="Company",
                    duration_months=60,
                    description="Development",
                    skills_used=["Python", "React"],
                ),
            ],
            education=[
                Education(degree="BS", field="CS", institution="MIT", year=2015),
            ],
            certifications=["AWS"],
            total_experience_years=5,
        )

        easy_job = JobPosting(
            id="easy",
            raw_text="Developer needed",
            title="Developer",
            company="Company",
            requirements=[
                JobRequirement(skill="Python", is_required=True, min_years=2),
            ],
            min_experience_years=2,
        )

        results = self.matcher.match_all(perfect_resume, [easy_job])
        result = results[0]

        # Should be excellent or good match
        assert result.match_level in [MatchLevel.EXCELLENT, MatchLevel.GOOD]
        assert result.match_percentage >= 60

    def test_match_level_poor(self):
        """Test poor match level for low score."""
        empty_resume = Resume(
            id="empty",
            raw_content="Empty",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=0,
        )

        demanding_job = JobPosting(
            id="demanding",
            raw_text="Senior Architect",
            title="Senior Architect",
            company="Company",
            requirements=[
                JobRequirement(skill="Kubernetes", is_required=True, min_years=5),
                JobRequirement(skill="Terraform", is_required=True, min_years=3),
                JobRequirement(skill="Go", is_required=True, min_years=4),
            ],
            min_experience_years=10,
        )

        results = self.matcher.match_all(empty_resume, [demanding_job])
        result = results[0]

        assert result.match_level == MatchLevel.POOR
        assert result.match_percentage < 40

    def test_concerns_for_gaps(self, sample_job_posting: JobPosting):
        """Test that concerns are raised for significant gaps."""
        junior_resume = Resume(
            id="junior",
            raw_content="Recent graduate",
            skills=[Skill(name="Python", normalized_name="python", level=SkillLevel.BEGINNER, years_experience=1)],
            experiences=[
                Experience(
                    title="Intern",
                    company="Startup",
                    duration_months=6,
                    description="Internship",
                    skills_used=["Python"],
                ),
            ],
            education=[],
            certifications=[],
            total_experience_years=0.5,
        )

        results = self.matcher.match_all(junior_resume, [sample_job_posting])
        result = results[0]

        # Should identify concerns for experience gap
        assert len(result.concerns) > 0

    def test_empty_jobs_list(self, sample_resume: Resume):
        """Test matching against empty job list."""
        results = self.matcher.match_all(sample_resume, [])

        assert len(results) == 0

    def test_single_job_best_fit(self, sample_resume: Resume, sample_job_posting: JobPosting):
        """Test that single job is marked as best fit."""
        results = self.matcher.match_all(sample_resume, [sample_job_posting])

        assert len(results) == 1
        assert results[0].is_best_fit is True
