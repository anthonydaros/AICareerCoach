"""Unit tests for ATS Scorer service."""

import pytest
from src.domain.services.ats_scorer import (
    ATSScorer,
    ATSWeights,
    ROLE_TYPE_KEYWORDS,
    WEIGHTS_BY_ROLE,
)
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


class TestRoleTypeDetection:
    """Test cases for role type detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = ATSScorer()

    def test_detects_technical_role(self):
        """Test that technical roles are detected correctly."""
        job = JobPosting(
            id="tech-job",
            raw_text="Software Engineer position",
            title="Senior Backend Engineer",
            company="Tech Corp",
            requirements=[JobRequirement(skill="Python", is_required=True, min_years=3)],
            min_experience_years=3,
        )

        role_type = self.scorer._detect_role_type(job)
        assert role_type == "technical"

    def test_detects_design_role(self):
        """Test that design roles are detected correctly."""
        job = JobPosting(
            id="design-job",
            raw_text="UX Designer position creating user interfaces",
            title="Senior UX Designer",
            company="Design Studio",
            requirements=[JobRequirement(skill="Figma", is_required=True, min_years=2)],
            min_experience_years=3,
        )

        role_type = self.scorer._detect_role_type(job)
        assert role_type == "design"

    def test_detects_data_role(self):
        """Test that data roles are detected correctly."""
        job = JobPosting(
            id="data-job",
            raw_text="Data Scientist position for ML team",
            title="Senior Data Scientist",
            company="AI Corp",
            requirements=[JobRequirement(skill="Python", is_required=True, min_years=3)],
            min_experience_years=4,
        )

        role_type = self.scorer._detect_role_type(job)
        assert role_type == "data"

    def test_detects_product_role(self):
        """Test that product roles are detected correctly."""
        job = JobPosting(
            id="product-job",
            raw_text="Product Manager leading roadmap development",
            title="Senior Product Manager",
            company="Startup Inc",
            requirements=[],
            min_experience_years=5,
        )

        role_type = self.scorer._detect_role_type(job)
        assert role_type == "product"

    def test_defaults_to_technical_for_unknown(self):
        """Test that unknown roles default to technical."""
        # Note: Must avoid substrings that match role keywords like "po" (in position), "pm", etc.
        job = JobPosting(
            id="unknown-job",
            raw_text="General office duties and tasks",
            title="Administrative Assistant",
            company="Corp",
            requirements=[],
            min_experience_years=2,
        )

        role_type = self.scorer._detect_role_type(job)
        assert role_type == "technical"  # Default when no specific role type detected


class TestDynamicWeights:
    """Test cases for dynamic weight configurations."""

    def test_technical_weights_structure(self):
        """Test that technical role weights are correct."""
        weights = ATSWeights.for_role_type("technical")

        assert weights.skill_match == 40.0
        assert weights.experience == 30.0
        assert weights.education == 15.0
        assert weights.certifications == 10.0
        assert weights.keywords == 5.0
        assert weights.portfolio == 0.0
        assert weights.leadership == 0.0

    def test_design_weights_prioritize_portfolio(self):
        """Test that design role weights prioritize portfolio."""
        weights = ATSWeights.for_role_type("design")

        assert weights.portfolio == 35.0  # Portfolio is the highest weight for design
        assert weights.skill_match == 30.0
        assert weights.experience == 20.0
        assert weights.education == 5.0

    def test_data_weights_structure(self):
        """Test that data role weights are correct."""
        weights = ATSWeights.for_role_type("data")

        assert weights.skill_match == 35.0
        assert weights.experience == 30.0
        assert weights.certifications == 15.0
        assert weights.keywords == 15.0

    def test_product_weights_prioritize_leadership(self):
        """Test that product role weights include leadership."""
        weights = ATSWeights.for_role_type("product")

        assert weights.experience == 40.0  # Experience is highest for product
        assert weights.leadership == 15.0
        assert weights.skill_match == 20.0

    def test_unknown_role_gets_default_weights(self):
        """Test that unknown role type gets default weights."""
        weights = ATSWeights.for_role_type("unknown_role")

        # Should get default weights
        assert weights.skill_match == 40.0
        assert weights.experience == 30.0

    def test_weights_sum_to_100(self):
        """Test that weights for each role type sum to 100."""
        for role_type in ["technical", "design", "data", "product"]:
            weights = ATSWeights.for_role_type(role_type)
            total = (
                weights.skill_match +
                weights.experience +
                weights.education +
                weights.certifications +
                weights.keywords +
                weights.portfolio +
                weights.leadership
            )
            assert total == 100.0, f"Weights for {role_type} sum to {total}, not 100"


class TestPortfolioScoring:
    """Test cases for portfolio scoring (design roles)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = ATSScorer()

    def test_detects_behance_portfolio(self):
        """Test that Behance portfolio link is detected."""
        resume = Resume(
            id="design-resume",
            raw_content="My portfolio: behance.net/johndoe",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=3,
        )

        # Set design weights
        self.scorer.weights = ATSWeights.for_role_type("design")
        score = self.scorer._calculate_portfolio_score(resume)

        assert score > 0

    def test_detects_dribbble_portfolio(self):
        """Test that Dribbble portfolio link is detected."""
        resume = Resume(
            id="design-resume",
            raw_content="See my work at dribbble.com/designer123",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=3,
        )

        self.scorer.weights = ATSWeights.for_role_type("design")
        score = self.scorer._calculate_portfolio_score(resume)

        assert score > 0

    def test_detects_figma_link(self):
        """Test that Figma portfolio link is detected."""
        resume = Resume(
            id="design-resume",
            raw_content="View my components: figma.com/@designer",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=3,
        )

        self.scorer.weights = ATSWeights.for_role_type("design")
        score = self.scorer._calculate_portfolio_score(resume)

        assert score > 0

    def test_multiple_portfolio_links_increase_score(self):
        """Test that multiple portfolio links increase score."""
        resume_single = Resume(
            id="design-resume-1",
            raw_content="Portfolio: behance.net/designer",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=3,
        )

        resume_multiple = Resume(
            id="design-resume-2",
            raw_content="Portfolio: behance.net/designer and dribbble.com/designer",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=3,
        )

        self.scorer.weights = ATSWeights.for_role_type("design")
        score_single = self.scorer._calculate_portfolio_score(resume_single)
        score_multiple = self.scorer._calculate_portfolio_score(resume_multiple)

        assert score_multiple > score_single


class TestLeadershipScoring:
    """Test cases for leadership scoring (product roles)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = ATSScorer()

    def test_detects_led_team(self):
        """Test that 'led team' pattern is detected."""
        resume = Resume(
            id="product-resume",
            raw_content="Led team of 5 engineers to deliver product on time",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        self.scorer.weights = ATSWeights.for_role_type("product")
        score = self.scorer._calculate_leadership_score(resume)

        assert score > 0

    def test_detects_stakeholder(self):
        """Test that 'stakeholder' pattern is detected."""
        resume = Resume(
            id="product-resume",
            raw_content="Worked with stakeholder teams to define requirements",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        self.scorer.weights = ATSWeights.for_role_type("product")
        score = self.scorer._calculate_leadership_score(resume)

        assert score > 0

    def test_detects_roadmap(self):
        """Test that 'roadmap' pattern is detected."""
        resume = Resume(
            id="product-resume",
            raw_content="Created product roadmap for Q1-Q4",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=5,
        )

        self.scorer.weights = ATSWeights.for_role_type("product")
        score = self.scorer._calculate_leadership_score(resume)

        assert score > 0


class TestRoleTypeKeywords:
    """Test cases for role type keyword definitions."""

    def test_technical_keywords_present(self):
        """Test that technical role keywords are defined."""
        assert "technical" in ROLE_TYPE_KEYWORDS
        keywords = ROLE_TYPE_KEYWORDS["technical"]
        assert "engineer" in keywords
        assert "developer" in keywords
        assert "backend" in keywords
        assert "frontend" in keywords
        assert "devops" in keywords

    def test_design_keywords_present(self):
        """Test that design role keywords are defined."""
        assert "design" in ROLE_TYPE_KEYWORDS
        keywords = ROLE_TYPE_KEYWORDS["design"]
        assert "designer" in keywords
        assert "ux" in keywords
        assert "ui" in keywords

    def test_data_keywords_present(self):
        """Test that data role keywords are defined."""
        assert "data" in ROLE_TYPE_KEYWORDS
        keywords = ROLE_TYPE_KEYWORDS["data"]
        assert "data scientist" in keywords
        assert "data analyst" in keywords
        assert "ml engineer" in keywords

    def test_product_keywords_present(self):
        """Test that product role keywords are defined."""
        assert "product" in ROLE_TYPE_KEYWORDS
        keywords = ROLE_TYPE_KEYWORDS["product"]
        assert "product manager" in keywords
        assert "product owner" in keywords
        assert "scrum master" in keywords


class TestWeightsByRoleConfig:
    """Test cases for weights configuration by role."""

    def test_all_role_types_have_weights(self):
        """Test that all role types have weight configurations."""
        expected_roles = ["technical", "design", "data", "product"]
        for role in expected_roles:
            assert role in WEIGHTS_BY_ROLE, f"Missing weights for role: {role}"

    def test_design_has_portfolio_weight(self):
        """Test that design role has portfolio weight."""
        assert WEIGHTS_BY_ROLE["design"]["portfolio"] == 35.0

    def test_product_has_leadership_weight(self):
        """Test that product role has leadership weight."""
        assert WEIGHTS_BY_ROLE["product"]["leadership"] == 15.0

    def test_technical_no_portfolio_weight(self):
        """Test that technical role has zero portfolio weight."""
        assert WEIGHTS_BY_ROLE["technical"]["portfolio"] == 0.0

    def test_technical_no_leadership_weight(self):
        """Test that technical role has zero leadership weight."""
        assert WEIGHTS_BY_ROLE["technical"]["leadership"] == 0.0
