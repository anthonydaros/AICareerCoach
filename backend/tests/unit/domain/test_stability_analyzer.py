"""Unit tests for Stability Analyzer service."""

import pytest
from src.domain.services.stability_analyzer import (
    StabilityAnalyzer,
    StabilityFlag,
    CONTRACT_TYPE_KEYWORDS,
    LAYOFF_COMPANIES_2022_2024,
    STARTUP_INDICATORS,
)
from src.domain.entities.resume import Resume, Experience


class TestStabilityAnalyzer:
    """Test cases for StabilityAnalyzer service."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = StabilityAnalyzer()

    def _create_resume_with_experiences(self, experiences: list) -> Resume:
        """Helper to create resume with experiences."""
        return Resume(
            id="test-resume",
            raw_content="Test resume content",
            skills=[],
            experiences=experiences,
            education=[],
            certifications=[],
            total_experience_years=sum(e.duration_months for e in experiences) / 12,
        )


class TestBrazilianEmploymentContext(TestStabilityAnalyzer):
    """Test cases for Brazilian employment context (PJ/CLT)."""

    def test_detects_pj_from_title(self):
        """Test that PJ (Pessoa Juridica) is detected from title."""
        experiences = [
            Experience(
                title="Software Engineer PJ",
                company="Tech Corp",
                duration_months=10,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        # Should detect PJ contract
        assert result.timeline[0].contract_type == "pj"

    def test_detects_contractor_as_pj(self):
        """Test that 'contractor' is detected as PJ."""
        experiences = [
            Experience(
                title="Contractor - Backend Developer",
                company="Startup Inc",
                duration_months=8,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].contract_type == "pj"

    def test_detects_consultor_as_pj(self):
        """Test that 'consultor' (Portuguese) is detected as PJ."""
        experiences = [
            Experience(
                title="Consultor de Sistemas",
                company="Consultoria XYZ",
                duration_months=6,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].contract_type == "pj"

    def test_detects_clt_from_title(self):
        """Test that CLT is detected from title."""
        experiences = [
            Experience(
                title="Desenvolvedor CLT",
                company="Empresa LTDA",
                duration_months=36,
                start_year=2020,
                end_year=2023,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].contract_type == "clt"

    def test_detects_freelancer(self):
        """Test that freelancer is detected."""
        experiences = [
            Experience(
                title="Freelance Developer",
                company="Self-employed",
                duration_months=12,
                start_year=2022,
                end_year=2023,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].contract_type == "freelancer"

    def test_pj_reduces_short_tenure_penalty(self):
        """Test that PJ contracts reduce short tenure penalty."""
        # Resume with short PJ tenure
        pj_experiences = [
            Experience(
                title="Software Engineer PJ",
                company="Tech Corp",
                duration_months=10,
                start_year=2023,
                end_year=2024,
            ),
            Experience(
                title="Backend Developer PJ",
                company="Startup Inc",
                duration_months=8,
                start_year=2022,
                end_year=2023,
            ),
        ]
        pj_resume = self._create_resume_with_experiences(pj_experiences)
        pj_result = self.analyzer.analyze(pj_resume)

        # Resume with same tenure but unknown contract
        unknown_experiences = [
            Experience(
                title="Software Engineer",
                company="Tech Corp",
                duration_months=10,
                start_year=2023,
                end_year=2024,
            ),
            Experience(
                title="Backend Developer",
                company="Startup Inc",
                duration_months=8,
                start_year=2022,
                end_year=2023,
            ),
        ]
        unknown_resume = self._create_resume_with_experiences(unknown_experiences)
        unknown_result = self.analyzer.analyze(unknown_resume)

        # PJ should have higher score (less penalty)
        assert pj_result.score >= unknown_result.score


class TestLayoffContext(TestStabilityAnalyzer):
    """Test cases for 2022-2024 layoff context."""

    def test_detects_layoff_at_google(self):
        """Test that short tenure at Google during 2022-2024 is marked as layoff."""
        experiences = [
            Experience(
                title="Software Engineer",
                company="Google",
                duration_months=10,
                start_year=2022,
                end_year=2023,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].is_layoff_period is True

    def test_detects_layoff_at_meta(self):
        """Test that short tenure at Meta during 2022-2024 is marked as layoff."""
        experiences = [
            Experience(
                title="Senior Engineer",
                company="Meta",
                duration_months=8,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].is_layoff_period is True

    def test_detects_layoff_at_brazilian_companies(self):
        """Test that Brazilian tech companies are in layoff list."""
        brazilian_companies = ["Nubank", "iFood", "Creditas", "Loft", "QuintoAndar"]

        for company in brazilian_companies:
            experiences = [
                Experience(
                    title="Developer",
                    company=company,
                    duration_months=8,
                    start_year=2023,
                    end_year=2023,
                ),
            ]
            resume = self._create_resume_with_experiences(experiences)
            result = self.analyzer.analyze(resume)

            assert result.timeline[0].is_layoff_period is True, f"Expected {company} to be marked as layoff period"

    def test_no_layoff_flag_before_2022(self):
        """Test that short tenure before 2022 is not marked as layoff."""
        experiences = [
            Experience(
                title="Software Engineer",
                company="Google",
                duration_months=10,
                start_year=2019,
                end_year=2020,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].is_layoff_period is False

    def test_layoff_context_removes_penalty(self):
        """Test that layoff context removes short tenure penalty."""
        # Short tenure at known layoff company during layoff period
        layoff_experiences = [
            Experience(
                title="Software Engineer",
                company="Google",
                duration_months=8,
                start_year=2023,
                end_year=2023,
            ),
            Experience(
                title="Senior Engineer",
                company="Stable Corp",
                duration_months=36,
                start_year=2020,
                end_year=2023,
            ),
        ]
        layoff_resume = self._create_resume_with_experiences(layoff_experiences)
        layoff_result = self.analyzer.analyze(layoff_resume)

        # Short tenure at unknown company (not layoff)
        no_layoff_experiences = [
            Experience(
                title="Software Engineer",
                company="Unknown Startup",
                duration_months=8,
                start_year=2023,
                end_year=2023,
            ),
            Experience(
                title="Senior Engineer",
                company="Stable Corp",
                duration_months=36,
                start_year=2020,
                end_year=2023,
            ),
        ]
        no_layoff_resume = self._create_resume_with_experiences(no_layoff_experiences)
        no_layoff_result = self.analyzer.analyze(no_layoff_resume)

        # Layoff context should result in higher score
        assert layoff_result.score >= no_layoff_result.score


class TestStartupContext(TestStabilityAnalyzer):
    """Test cases for startup tenure adjustments."""

    def test_detects_early_stage_startup(self):
        """Test that early-stage startup is detected."""
        experiences = [
            Experience(
                title="Founding Engineer",
                company="Startup XYZ (Seed Stage)",
                duration_months=10,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].startup_stage == "early_stage"

    def test_detects_series_a_startup(self):
        """Test that Series A startup is detected."""
        experiences = [
            Experience(
                title="Software Engineer",
                company="TechStartup (Series A)",
                duration_months=14,
                start_year=2023,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].startup_stage == "series_a"

    def test_detects_series_b_startup(self):
        """Test that Series B startup is detected."""
        experiences = [
            Experience(
                title="Senior Engineer",
                company="GrowthCo Series B",
                duration_months=18,
                start_year=2022,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].startup_stage == "series_b"

    def test_detects_late_stage_startup(self):
        """Test that late-stage (Series C+) startup is detected."""
        experiences = [
            Experience(
                title="Staff Engineer",
                company="Unicorn Corp (Series D)",
                duration_months=24,
                start_year=2022,
                end_year=2024,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        assert result.timeline[0].startup_stage == "late_stage"

    def test_startup_reduces_short_tenure_penalty(self):
        """Test that startup context reduces short tenure penalty."""
        # Early-stage startup with short tenure
        startup_experiences = [
            Experience(
                title="Software Engineer",
                company="NewStartup (Seed)",
                duration_months=8,
                start_year=2023,
                end_year=2024,
            ),
        ]
        startup_resume = self._create_resume_with_experiences(startup_experiences)
        startup_result = self.analyzer.analyze(startup_resume)

        # Same tenure at established company
        established_experiences = [
            Experience(
                title="Software Engineer",
                company="BigCorp Inc",
                duration_months=8,
                start_year=2023,
                end_year=2024,
            ),
        ]
        established_resume = self._create_resume_with_experiences(established_experiences)
        established_result = self.analyzer.analyze(established_resume)

        # Startup should have higher score (less penalty)
        assert startup_result.score >= established_result.score


class TestPenaltyReduction(TestStabilityAnalyzer):
    """Test cases for penalty reduction factors."""

    def test_layoff_zero_penalty(self):
        """Test that layoff context results in zero penalty factor."""
        entry = self.analyzer._build_timeline([
            Experience(
                title="Engineer",
                company="Google",
                duration_months=8,
                start_year=2023,
                end_year=2023,
            )
        ])[0]

        factor = self.analyzer._get_penalty_reduction_factor(entry)
        assert factor == 0.0  # Zero penalty for layoff

    def test_pj_half_penalty(self):
        """Test that PJ contract results in 50% penalty factor."""
        entry = self.analyzer._build_timeline([
            Experience(
                title="Consultant PJ",
                company="Consulting Firm",
                duration_months=8,
                start_year=2021,
                end_year=2021,
            )
        ])[0]

        factor = self.analyzer._get_penalty_reduction_factor(entry)
        assert factor == 0.5  # 50% penalty for PJ

    def test_early_stage_startup_reduced_penalty(self):
        """Test that early-stage startup has 70% penalty reduction."""
        entry = self.analyzer._build_timeline([
            Experience(
                title="Founding Engineer",
                company="NewStartup (Seed Stage)",
                duration_months=8,
                start_year=2021,
                end_year=2021,
            )
        ])[0]

        factor = self.analyzer._get_penalty_reduction_factor(entry)
        assert factor == 0.3  # 70% reduction = 30% factor


class TestCOVIDGapHandling(TestStabilityAnalyzer):
    """Test cases for COVID-era gap handling."""

    def test_covid_gap_no_penalty(self):
        """Test that employment gaps during COVID (2020-2021) are not penalized."""
        experiences = [
            Experience(
                title="Senior Engineer",
                company="Post-COVID Corp",
                duration_months=24,
                start_year=2022,
                end_year=2024,
            ),
            Experience(
                title="Software Engineer",
                company="Pre-COVID Corp",
                duration_months=36,
                start_year=2017,
                end_year=2020,
            ),
        ]
        resume = self._create_resume_with_experiences(experiences)
        result = self.analyzer.analyze(resume)

        # Should have COVID gap indicator
        covid_indicators = [i for i in result.indicators if "COVID period" in i]
        assert len(covid_indicators) > 0


class TestDataStructures(TestStabilityAnalyzer):
    """Test cases for data structures."""

    def test_contract_type_keywords_structure(self):
        """Test that contract type keywords are properly structured."""
        assert "pj" in CONTRACT_TYPE_KEYWORDS
        assert "clt" in CONTRACT_TYPE_KEYWORDS
        assert "freelancer" in CONTRACT_TYPE_KEYWORDS

        # Each should have a list of keywords
        assert len(CONTRACT_TYPE_KEYWORDS["pj"]) > 0
        assert len(CONTRACT_TYPE_KEYWORDS["clt"]) > 0
        assert len(CONTRACT_TYPE_KEYWORDS["freelancer"]) > 0

    def test_layoff_companies_list(self):
        """Test that layoff companies list is comprehensive."""
        # FAANG/MAANG
        assert "google" in LAYOFF_COMPANIES_2022_2024
        assert "meta" in LAYOFF_COMPANIES_2022_2024
        assert "amazon" in LAYOFF_COMPANIES_2022_2024
        assert "microsoft" in LAYOFF_COMPANIES_2022_2024

        # Major Tech
        assert "twitter" in LAYOFF_COMPANIES_2022_2024
        assert "salesforce" in LAYOFF_COMPANIES_2022_2024
        assert "spotify" in LAYOFF_COMPANIES_2022_2024

        # Brazilian Tech
        assert "nubank" in LAYOFF_COMPANIES_2022_2024
        assert "ifood" in LAYOFF_COMPANIES_2022_2024

    def test_startup_indicators_structure(self):
        """Test that startup indicators are properly structured."""
        assert "early_stage" in STARTUP_INDICATORS
        assert "series_a" in STARTUP_INDICATORS
        assert "series_b" in STARTUP_INDICATORS
        assert "late_stage" in STARTUP_INDICATORS

        # Each should have relevant keywords
        assert "startup" in STARTUP_INDICATORS["early_stage"]
        assert "seed" in STARTUP_INDICATORS["early_stage"]
        assert "series a" in STARTUP_INDICATORS["series_a"]


class TestEmptyResume(TestStabilityAnalyzer):
    """Test cases for empty resume handling."""

    def test_empty_experiences_returns_neutral_score(self):
        """Test that resume with no experiences returns neutral score."""
        resume = Resume(
            id="empty",
            raw_content="No experience",
            skills=[],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=0,
        )
        result = self.analyzer.analyze(resume)

        assert result.score == 50
        assert result.total_companies == 0
        assert len(result.timeline) == 0
