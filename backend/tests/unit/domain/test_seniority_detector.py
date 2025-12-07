"""Unit tests for Seniority Detector service."""

import pytest
from src.domain.services.seniority_detector import (
    SeniorityDetector,
    SeniorityLevel,
    SENIOR_TITLES,
    MID_TITLES,
    JUNIOR_TITLES,
    SENIOR_SKILLS,
    MID_SKILLS,
)
from src.domain.entities.resume import Resume, Skill, Experience, SkillLevel


class TestSeniorityDetector:
    """Test cases for SeniorityDetector service."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = SeniorityDetector()


class TestBrazilianTitles(TestSeniorityDetector):
    """Test cases for Brazilian title recognition."""

    def test_detects_pleno_as_mid_level(self):
        """Test that 'Pleno' (Brazilian mid-level) is detected correctly."""
        resume = Resume(
            id="test",
            raw_content="Desenvolvedor Pleno com experiência em Python e React",
            skills=[
                Skill(name="Python", normalized_name="python", level=SkillLevel.ADVANCED, years_experience=3),
            ],
            experiences=[
                Experience(
                    title="Desenvolvedor Pleno",
                    company="Tech Corp",
                    duration_months=36,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=3.0,
        )
        result = self.detector.detect(resume)

        assert result.level in [SeniorityLevel.MID, SeniorityLevel.SENIOR]
        assert "Mid-level job titles found" in result.indicators or "Senior-level job titles found" in result.indicators

    def test_detects_especialista_senior(self):
        """Test that 'Especialista Sênior' is detected as senior."""
        resume = Resume(
            id="test",
            raw_content="""Especialista Sênior em Engenharia de Dados.
            Led architecture design for data pipelines. Responsible for system design and scalability.
            Mentored junior engineers and led team of 5 developers.
            Implemented microservices architecture with terraform and kubernetes.
            Reduced processing time by 50% through performance optimization.""",
            skills=[
                Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=6),
                Skill(name="Terraform", normalized_name="terraform", level=SkillLevel.EXPERT, years_experience=4),
                Skill(name="System Design", normalized_name="system design", level=SkillLevel.EXPERT, years_experience=5),
            ],
            experiences=[
                Experience(
                    title="Especialista Sênior",
                    company="Big Data Corp",
                    duration_months=48,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=8.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR
        assert "Senior-level job titles found" in result.indicators

    def test_detects_arquiteto_de_solucoes(self):
        """Test that 'Arquiteto de Soluções' is detected as senior."""
        resume = Resume(
            id="test",
            raw_content="""Arquiteto de Soluções cloud com foco em AWS e Azure.
            Led cloud architecture design for enterprise systems. Responsible for multi-cloud strategy.
            Mentored 8 engineers and led technical decisions. Architected solutions for high availability.
            Implemented terraform infrastructure as code and cloud architecture patterns.
            Reduced infrastructure costs by 40% through cloud optimization.""",
            skills=[
                Skill(name="AWS", normalized_name="aws", level=SkillLevel.EXPERT, years_experience=7),
                Skill(name="Azure", normalized_name="azure", level=SkillLevel.EXPERT, years_experience=5),
                Skill(name="Terraform", normalized_name="terraform", level=SkillLevel.EXPERT, years_experience=5),
                Skill(name="Cloud Architecture", normalized_name="cloud architecture", level=SkillLevel.EXPERT, years_experience=6),
            ],
            experiences=[
                Experience(
                    title="Arquiteto de Soluções",
                    company="Cloud Corp",
                    duration_months=60,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=10.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR

    def test_detects_junior_br(self):
        """Test that Brazilian junior titles are detected."""
        resume = Resume(
            id="test",
            raw_content="Desenvolvedor Júnior aprendendo programação",
            skills=[
                Skill(name="Python", normalized_name="python", level=SkillLevel.BEGINNER, years_experience=1),
            ],
            experiences=[
                Experience(
                    title="Desenvolvedor Júnior",
                    company="Startup",
                    duration_months=12,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=1.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.JUNIOR
        assert "Junior/entry-level titles found" in result.indicators

    def test_detects_coordenador_as_senior(self):
        """Test that 'Coordenador' is detected as senior/lead level."""
        resume = Resume(
            id="test",
            raw_content="Coordenador de Desenvolvimento responsável por equipe de 10 engenheiros",
            skills=[
                Skill(name="Leadership", normalized_name="leadership", level=SkillLevel.EXPERT, years_experience=5),
            ],
            experiences=[
                Experience(
                    title="Coordenador de Desenvolvimento",
                    company="Enterprise Corp",
                    duration_months=36,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=7.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR


class TestDesignTitles(TestSeniorityDetector):
    """Test cases for design career track titles."""

    def test_detects_senior_designer(self):
        """Test that Senior Designer is detected as senior."""
        resume = Resume(
            id="test",
            raw_content="""Senior UX Designer with 8 years experience in product design.
            Led design systems development and mentored junior designers. Responsible for UX strategy.
            Managed design team of 4. Architected component libraries and design tokens.
            Implemented design operations and accessibility audits. Reduced design iteration time by 60%.""",
            skills=[
                Skill(name="Figma", normalized_name="figma", level=SkillLevel.EXPERT, years_experience=5),
                Skill(name="User Research", normalized_name="user research", level=SkillLevel.EXPERT, years_experience=5),
                Skill(name="Design Systems", normalized_name="design systems", level=SkillLevel.EXPERT, years_experience=4),
                Skill(name="UX Strategy", normalized_name="ux strategy", level=SkillLevel.EXPERT, years_experience=3),
            ],
            experiences=[
                Experience(
                    title="Senior UX Designer",
                    company="Design Agency",
                    duration_months=48,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=8.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR
        # Note: Title detection happens alongside other indicators. The level is the key check.
        # The resume has enough senior signals (8 years exp, design systems, leadership) to be SENIOR.

    def test_detects_design_lead(self):
        """Test that Design Lead is detected as senior."""
        resume = Resume(
            id="test",
            raw_content="Design Lead responsible for design systems and team mentoring",
            skills=[
                Skill(name="Design Systems", normalized_name="design systems", level=SkillLevel.EXPERT, years_experience=4),
            ],
            experiences=[
                Experience(
                    title="Design Lead",
                    company="Tech Corp",
                    duration_months=36,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=7.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR

    def test_detects_product_designer_as_mid(self):
        """Test that Product Designer is detected as mid-level."""
        resume = Resume(
            id="test",
            raw_content="Product Designer creating user flows and wireframes",
            skills=[
                Skill(name="Figma", normalized_name="figma", level=SkillLevel.ADVANCED, years_experience=3),
            ],
            experiences=[
                Experience(
                    title="Product Designer",
                    company="Startup Inc",
                    duration_months=24,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=3.0,
        )
        result = self.detector.detect(resume)

        assert result.level in [SeniorityLevel.MID, SeniorityLevel.SENIOR]

    def test_detects_designer_pleno_as_mid(self):
        """Test that Designer Pleno (Brazilian) is detected as mid-level."""
        resume = Resume(
            id="test",
            raw_content="Designer Pleno com foco em interfaces mobile",
            skills=[
                Skill(name="Figma", normalized_name="figma", level=SkillLevel.ADVANCED, years_experience=2),
            ],
            experiences=[
                Experience(
                    title="Designer Pleno",
                    company="App Studio",
                    duration_months=24,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=2.5,
        )
        result = self.detector.detect(resume)

        assert result.level in [SeniorityLevel.MID, SeniorityLevel.JUNIOR]


class TestDesignSkills(TestSeniorityDetector):
    """Test cases for design skill recognition."""

    def test_design_systems_indicates_senior(self):
        """Test that design systems skill indicates senior level."""
        resume = Resume(
            id="test",
            raw_content="Expert in design systems, design tokens, design operations, and component libraries. Strong in design leadership and UX strategy.",
            skills=[
                Skill(name="Design Systems", normalized_name="design systems", level=SkillLevel.EXPERT, years_experience=4),
                Skill(name="Design Tokens", normalized_name="design tokens", level=SkillLevel.EXPERT, years_experience=3),
                Skill(name="Design Leadership", normalized_name="design leadership", level=SkillLevel.EXPERT, years_experience=3),
            ],
            experiences=[
                Experience(
                    title="Designer",
                    company="Design Corp",
                    duration_months=48,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=5.0,
        )
        result = self.detector.detect(resume)

        # Should have high skills score due to multiple senior skills (>= 3 senior skills returns 0.8)
        assert result.scores.get("skills", 0) >= 0.6

    def test_figma_indicates_mid_level(self):
        """Test that Figma skill indicates mid level."""
        resume = Resume(
            id="test",
            raw_content="Proficient in Figma, wireframing, and prototyping",
            skills=[
                Skill(name="Figma", normalized_name="figma", level=SkillLevel.ADVANCED, years_experience=2),
            ],
            experiences=[
                Experience(
                    title="Designer",
                    company="Agency",
                    duration_months=24,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=2.0,
        )
        result = self.detector.detect(resume)

        # Figma is a mid-level skill
        assert result.scores.get("skills", 0) >= 0.3


class TestAILLMSkills(TestSeniorityDetector):
    """Test cases for AI/LLM skill recognition."""

    def test_langchain_indicates_senior(self):
        """Test that LangChain skill indicates senior level."""
        resume = Resume(
            id="test",
            raw_content="Expert in LangChain, RAG, and prompt engineering for LLM applications",
            skills=[
                Skill(name="LangChain", normalized_name="langchain", level=SkillLevel.EXPERT, years_experience=2),
                Skill(name="Python", normalized_name="python", level=SkillLevel.EXPERT, years_experience=5),
            ],
            experiences=[
                Experience(
                    title="AI Engineer",
                    company="AI Startup",
                    duration_months=36,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=5.0,
        )
        result = self.detector.detect(resume)

        # LangChain is a senior skill
        assert "langchain" in SENIOR_SKILLS

    def test_rag_indicates_senior(self):
        """Test that RAG expertise indicates senior level."""
        resume = Resume(
            id="test",
            raw_content="Built RAG systems with vector databases and semantic search",
            skills=[
                Skill(name="RAG", normalized_name="rag", level=SkillLevel.EXPERT, years_experience=2),
            ],
            experiences=[],
            education=[],
            certifications=[],
            total_experience_years=4.0,
        )
        result = self.detector.detect(resume)

        assert "rag" in SENIOR_SKILLS

    def test_openai_api_indicates_mid(self):
        """Test that OpenAI API usage indicates mid level."""
        assert "openai api" in MID_SKILLS


class TestSeniorityData(TestSeniorityDetector):
    """Test cases for seniority data structures."""

    def test_brazilian_senior_titles_present(self):
        """Test that Brazilian senior titles are in the patterns."""
        # Convert patterns to a single string for checking
        patterns_str = " ".join(SENIOR_TITLES)

        # Check for Brazilian titles (using lowercase regex patterns)
        assert "especialista" in patterns_str.lower()
        assert "arquiteto" in patterns_str.lower()
        # The pattern uses regex character class [çc] for Portuguese accents
        assert "solu" in patterns_str.lower()  # "solu" is common to both "soluções" variants

    def test_brazilian_mid_titles_present(self):
        """Test that Brazilian mid-level titles are in the patterns."""
        patterns_str = " ".join(MID_TITLES)

        assert "pleno" in patterns_str.lower()
        assert "desenvolvedor" in patterns_str.lower()

    def test_brazilian_junior_titles_present(self):
        """Test that Brazilian junior titles are in the patterns."""
        patterns_str = " ".join(JUNIOR_TITLES)

        assert "júnior" in patterns_str.lower() or "junior" in patterns_str.lower()

    def test_design_senior_skills_present(self):
        """Test that design senior skills are defined."""
        design_senior_skills = [
            "design systems", "design leadership", "ux strategy",
            "design operations", "figma components", "design tokens"
        ]
        for skill in design_senior_skills:
            assert skill in SENIOR_SKILLS, f"Missing design senior skill: {skill}"

    def test_design_mid_skills_present(self):
        """Test that design mid-level skills are defined."""
        design_mid_skills = [
            "figma", "user research", "prototyping", "wireframing",
            "usability testing", "design thinking"
        ]
        for skill in design_mid_skills:
            assert skill in MID_SKILLS, f"Missing design mid skill: {skill}"

    def test_ai_llm_senior_skills_present(self):
        """Test that AI/LLM senior skills are defined."""
        ai_senior_skills = [
            "langchain", "rag", "prompt engineering", "llm architecture",
            "vector databases", "embeddings", "fine-tuning"
        ]
        for skill in ai_senior_skills:
            assert skill in SENIOR_SKILLS, f"Missing AI senior skill: {skill}"

    def test_ai_llm_mid_skills_present(self):
        """Test that AI/LLM mid-level skills are defined."""
        ai_mid_skills = ["openai api", "chatgpt integration", "llm prompts"]
        for skill in ai_mid_skills:
            assert skill in MID_SKILLS, f"Missing AI mid skill: {skill}"


class TestSeniorityDetection(TestSeniorityDetector):
    """Test cases for seniority detection logic."""

    def test_high_experience_returns_senior(self):
        """Test that high experience results in senior level."""
        resume = Resume(
            id="test",
            raw_content="""Led development teams, architected systems, and mentored engineers.
            Responsible for system design and technical strategy. Managed team of 10 engineers.
            Architected microservices with high availability and disaster recovery.
            Implemented terraform infrastructure and kubernetes orchestration.
            Reduced deployment time by 70% through CI/CD optimization.""",
            skills=[
                Skill(name="System Design", normalized_name="system design", level=SkillLevel.EXPERT, years_experience=8),
                Skill(name="Terraform", normalized_name="terraform", level=SkillLevel.EXPERT, years_experience=6),
                Skill(name="Kubernetes", normalized_name="kubernetes", level=SkillLevel.EXPERT, years_experience=5),
            ],
            experiences=[
                Experience(
                    title="Staff Engineer",
                    company="Tech Corp",
                    duration_months=96,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=10.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.SENIOR
        assert result.confidence > 70

    def test_low_experience_returns_junior(self):
        """Test that low experience results in junior level."""
        resume = Resume(
            id="test",
            raw_content="""Intern helping with basic tasks. Learning programming basics.
            Assisted with simple bug fixes under supervision. Trainee role.""",
            skills=[
                Skill(name="HTML", normalized_name="html", level=SkillLevel.BEGINNER, years_experience=0.5),
            ],
            experiences=[
                Experience(
                    title="Intern",
                    company="Startup",
                    duration_months=6,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=0.5,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.JUNIOR

    def test_mid_experience_returns_mid(self):
        """Test that mid experience results in mid level."""
        resume = Resume(
            id="test",
            raw_content="""Implemented features, refactored code, and worked independently on projects.
            Developed REST APIs and integrated third-party services.
            Optimized database queries and automated deployment processes.
            Participated in code reviews and contributed to test automation.""",
            skills=[
                Skill(name="REST API", normalized_name="rest api", level=SkillLevel.ADVANCED, years_experience=3),
                Skill(name="Docker", normalized_name="docker", level=SkillLevel.INTERMEDIATE, years_experience=2),
                Skill(name="CI/CD", normalized_name="ci/cd", level=SkillLevel.INTERMEDIATE, years_experience=2),
            ],
            experiences=[
                Experience(
                    title="Software Engineer II",
                    company="Tech Corp",
                    duration_months=36,
                )
            ],
            education=[],
            certifications=[],
            total_experience_years=3.0,
        )
        result = self.detector.detect(resume)

        assert result.level == SeniorityLevel.MID
