"""ATS Scoring Service - Calculates ATS compatibility scores."""

import re
from dataclasses import dataclass, field
from typing import Optional, Dict, List

from src.domain.entities.resume import Resume
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.analysis_result import ATSResult, KeywordAnalysis, KeywordWeight
from src.domain.services.skill_relationships import expand_skills, normalize_skill


# =========================================
# ROLE TYPE DETECTION KEYWORDS
# =========================================

ROLE_TYPE_KEYWORDS = {
    "technical": [
        "engineer", "developer", "programmer", "backend", "frontend",
        "fullstack", "full-stack", "devops", "sre", "architect",
        "engenheiro", "desenvolvedor",
    ],
    "design": [
        "designer", "ux", "ui", "product design", "visual design",
        "creative", "criativo", "interaction design",
    ],
    "data": [
        "data scientist", "data analyst", "data engineer", "ml engineer",
        "ai engineer", "machine learning", "analytics", "cientista de dados",
    ],
    "product": [
        "product manager", "product owner", "pm", "scrum master",
        "gerente de produto", "po",
    ],
}

# =========================================
# WEIGHT CONFIGURATIONS PER ROLE TYPE
# =========================================

WEIGHTS_BY_ROLE = {
    "technical": {
        "skill_match": 40.0,
        "experience": 30.0,
        "education": 15.0,
        "certifications": 10.0,
        "keywords": 5.0,
        "portfolio": 0.0,
        "leadership": 0.0,
    },
    "design": {
        "skill_match": 30.0,
        "experience": 20.0,
        "education": 5.0,
        "certifications": 5.0,
        "keywords": 5.0,
        "portfolio": 35.0,  # Portfolio is critical for design roles
        "leadership": 0.0,
    },
    "data": {
        "skill_match": 35.0,
        "experience": 30.0,
        "education": 5.0,
        "certifications": 15.0,
        "keywords": 15.0,
        "portfolio": 0.0,
        "leadership": 0.0,
    },
    "product": {
        "skill_match": 20.0,
        "experience": 40.0,
        "education": 10.0,
        "certifications": 5.0,
        "keywords": 10.0,
        "portfolio": 0.0,
        "leadership": 15.0,
    },
}


@dataclass
class ATSWeights:
    """Configurable ATS scoring weights (must sum to 100)."""
    skill_match: float = 40.0       # Skills matching job requirements
    experience: float = 30.0        # Years of experience
    education: float = 15.0         # Education match
    certifications: float = 10.0    # Relevant certifications
    keywords: float = 5.0           # Keyword optimization
    portfolio: float = 0.0          # Portfolio quality (design roles)
    leadership: float = 0.0         # Leadership signals (product roles)

    @classmethod
    def for_role_type(cls, role_type: str) -> "ATSWeights":
        """Create weights configured for a specific role type."""
        if role_type in WEIGHTS_BY_ROLE:
            return cls(**WEIGHTS_BY_ROLE[role_type])
        return cls()  # Default weights


class ATSScorer:
    """
    ATS Scoring Engine.

    Calculates how well a resume matches a job posting
    using industry-standard ATS criteria with dynamic weights
    based on role type (Technical, Design, Data, Product):
    - Skill match (varies by role)
    - Experience (varies by role)
    - Education (varies by role)
    - Certifications (varies by role)
    - Keywords (varies by role)
    - Portfolio (design roles only)
    - Leadership (product roles only)
    """

    def __init__(self, weights: Optional[ATSWeights] = None):
        self.weights = weights or ATSWeights()

    def _detect_role_type(self, job: JobPosting) -> str:
        """Detect role type from job posting to apply appropriate weights."""
        job_text = f"{job.title or ''} {job.raw_text or ''}".lower()

        for role_type, keywords in ROLE_TYPE_KEYWORDS.items():
            if any(kw in job_text for kw in keywords):
                return role_type

        return "technical"  # Default to technical if no match

    def _calculate_portfolio_score(self, resume: Resume) -> float:
        """Calculate portfolio score for design roles."""
        text_lower = resume.raw_content.lower()
        score = 0.0

        # Check for portfolio links
        if re.search(r"behance\.net/", text_lower):
            score += 10.0
        if re.search(r"dribbble\.com/", text_lower):
            score += 10.0
        if re.search(r"portfolio|work\s+samples|case\s+stud", text_lower):
            score += 10.0
        # Design-specific platforms
        if re.search(r"figma\.com/", text_lower):
            score += 5.0

        return min(score, self.weights.portfolio)

    def _calculate_leadership_score(self, resume: Resume) -> float:
        """Calculate leadership score for product/management roles."""
        text_lower = resume.raw_content.lower()
        score = 0.0

        leadership_patterns = [
            r"led\s+team", r"managed\s+team", r"liderou",
            r"mentored", r"mentorou", r"coached",
            r"cross-functional", r"stakeholder",
            r"roadmap", r"strategy", r"estratégia",
            r"product\s+launch", r"lançamento",
        ]

        for pattern in leadership_patterns:
            if re.search(pattern, text_lower):
                score += 3.0

        return min(score, self.weights.leadership)

    def calculate(self, resume: Resume, job: JobPosting) -> ATSResult:
        """
        Calculate ATS score for resume against job.

        Args:
            resume: Parsed resume entity
            job: Parsed job posting entity

        Returns:
            ATSResult with score breakdown
        """
        # Detect role type and apply appropriate weights
        role_type = self._detect_role_type(job)
        self.weights = ATSWeights.for_role_type(role_type)

        resume_skills = resume.get_skill_names()
        required_skills = job.get_required_skills()
        all_job_skills = job.get_all_skills()

        # 1. Skill Match Score (weight varies by role)
        skill_score, matched_skills, missing_skills = self._calculate_skill_score(
            resume_skills, required_skills, all_job_skills
        )

        # 2. Experience Score (weight varies by role)
        experience_score = self._calculate_experience_score(
            resume.total_experience_years, job.min_experience_years
        )

        # 3. Education Score (weight varies by role)
        education_score = self._calculate_education_score(resume, job)

        # 4. Certification Score (weight varies by role)
        certification_score = self._calculate_certification_score(resume)

        # 5. Keyword Score (weight varies by role)
        keyword_score, matched_kw, missing_kw = self._calculate_keyword_score(
            resume.raw_content, job.keywords
        )

        # 6. Portfolio Score (design roles only)
        portfolio_score = 0.0
        if self.weights.portfolio > 0:
            portfolio_score = self._calculate_portfolio_score(resume)

        # 7. Leadership Score (product roles only)
        leadership_score = 0.0
        if self.weights.leadership > 0:
            leadership_score = self._calculate_leadership_score(resume)

        # Calculate total
        total_score = (
            skill_score +
            experience_score +
            education_score +
            certification_score +
            keyword_score +
            portfolio_score +
            leadership_score
        )

        # Detect format issues
        format_issues = self._detect_format_issues(resume.raw_content)

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(
            missing_required=missing_skills,
            missing_keywords=set(missing_kw),
            format_issues=format_issues,
            experience_gap=max(0, job.min_experience_years - resume.total_experience_years),
            resume=resume,
        )

        # Add role-specific suggestions
        if role_type == "design" and portfolio_score < self.weights.portfolio * 0.5:
            suggestions.append(
                "PORTFOLIO: Add portfolio links (Behance, Dribbble, personal site) - "
                "critical for design roles"
            )
        if role_type == "product" and leadership_score < self.weights.leadership * 0.5:
            suggestions.append(
                "LEADERSHIP: Highlight cross-functional collaboration, roadmap ownership, "
                "and stakeholder management experience"
            )

        # Generate detailed keyword analysis
        keyword_analysis = self._generate_keyword_analysis(
            resume.raw_content,
            required_skills,
            all_job_skills,
            job.keywords,
            matched_skills,
            missing_skills,
        )

        # Generate score calculation explanation
        score_calculation = self._generate_score_calculation(
            skill_score=skill_score,
            experience_score=experience_score,
            education_score=education_score,
            certification_score=certification_score,
            keyword_score=keyword_score,
            total_score=total_score,
            matched_required=len(matched_skills & required_skills) if required_skills else 0,
            total_required=len(required_skills) if required_skills else 0,
        )

        # Role-specific methodology explanation
        weight_details = {
            "technical": "Skills (40%), Experience (30%), Education (15%), Certifications (10%), Keywords (5%)",
            "design": "Portfolio (35%), Skills (30%), Experience (20%), Certifications (5%), Education (5%), Keywords (5%)",
            "data": "Skills (35%), Experience (30%), Keywords (15%), Certifications (15%), Education (5%)",
            "product": "Experience (40%), Skills (20%), Leadership (15%), Education (10%), Keywords (10%), Certifications (5%)",
        }

        methodology = (
            f"ATS (Applicant Tracking System) score measures how well your resume matches "
            f"the job requirements. This analysis detected a **{role_type.upper()}** role and uses "
            f"role-specific weighted criteria: {weight_details.get(role_type, weight_details['technical'])}. "
            f"Critical keywords must appear exactly as stated in the job posting. "
            f"Scores above 80% typically pass initial screening."
        )

        return ATSResult(
            total_score=round(total_score, 1),
            skill_score=round(skill_score, 1),
            experience_score=round(experience_score, 1),
            education_score=round(education_score, 1),
            certification_score=round(certification_score, 1),
            keyword_score=round(keyword_score, 1),
            matched_keywords=list(matched_skills | set(matched_kw)),
            missing_keywords=list(missing_skills | set(missing_kw)),
            format_issues=format_issues,
            improvement_suggestions=suggestions,
            keyword_analysis=keyword_analysis,
            score_calculation=score_calculation,
            methodology=methodology,
        )

    def _calculate_skill_score(
        self,
        resume_skills: set[str],
        required_skills: set[str],
        all_job_skills: set[str],
    ) -> tuple[float, set[str], set[str]]:
        """Calculate skill match score with intelligent skill inference."""
        # Normalize all skills for consistent matching
        normalized_resume = {normalize_skill(s) for s in resume_skills}
        normalized_required = {normalize_skill(s) for s in required_skills}
        normalized_all_job = {normalize_skill(s) for s in all_job_skills}

        # Expand resume skills with inferred knowledge
        # e.g., "Python" -> includes "pytorch", "tensorflow", etc.
        expanded_resume_skills = expand_skills(normalized_resume)

        # Match against required skills with expanded set
        matched_required = expanded_resume_skills & normalized_required
        missing_required = normalized_required - expanded_resume_skills

        # Also check all skills for additional matches
        matched_all = expanded_resume_skills & normalized_all_job

        if normalized_required:
            skill_ratio = len(matched_required) / len(normalized_required)
        elif normalized_all_job:
            skill_ratio = len(matched_all) / len(normalized_all_job)
        else:
            skill_ratio = 1.0  # No requirements = full score

        score = skill_ratio * self.weights.skill_match

        return score, matched_all, missing_required

    def _calculate_experience_score(
        self,
        actual_years: float,
        required_years: int,
    ) -> float:
        """Calculate experience score."""
        if required_years <= 0:
            return self.weights.experience  # No requirement = full score

        if actual_years >= required_years:
            return self.weights.experience  # Meets or exceeds requirement

        if actual_years > 0:
            # Partial credit based on ratio (minimum 50% if any experience)
            ratio = actual_years / required_years
            return max(ratio * self.weights.experience, self.weights.experience * 0.5)

        return 0  # No experience

    def _calculate_education_score(self, resume: Resume, job: JobPosting) -> float:
        """Calculate education match score."""
        if not resume.education:
            # No education listed, give partial credit
            return self.weights.education * 0.3

        if not job.education_requirements:
            # No requirements, give full credit
            return self.weights.education

        job_fields = {f.lower() for f in job.education_requirements}

        # Check for field match
        for edu in resume.education:
            edu_field = edu.field.lower()
            # Direct match
            if edu_field in job_fields:
                return self.weights.education
            # Partial match (e.g., "Computer Science" matches "CS")
            if any(keyword in edu_field for keyword in ["computer", "software", "engineering", "science"]):
                if any(keyword in req for keyword in ["cs", "computer", "software", "engineering"] for req in job_fields):
                    return self.weights.education

        # Generic degree credit
        return self.weights.education * 0.5

    def _calculate_certification_score(self, resume: Resume) -> float:
        """Calculate certification score."""
        cert_count = len(resume.certifications)

        if cert_count == 0:
            return 0
        elif cert_count == 1:
            return self.weights.certifications * 0.5
        elif cert_count == 2:
            return self.weights.certifications * 0.75
        else:
            return self.weights.certifications

    def _calculate_keyword_score(
        self,
        resume_text: str,
        keywords: list[str],
    ) -> tuple[float, list[str], list[str]]:
        """Calculate keyword density score."""
        if not keywords:
            return self.weights.keywords, [], []

        text_lower = resume_text.lower()
        matched = [kw for kw in keywords if kw.lower() in text_lower]
        missing = [kw for kw in keywords if kw.lower() not in text_lower]

        coverage = len(matched) / len(keywords)
        score = coverage * self.weights.keywords

        return score, matched, missing

    def _detect_format_issues(self, text: str) -> list[str]:
        """Detect potential formatting problems."""
        issues = []

        # Check for table-like formatting (pipes suggest tables)
        if "|" in text and text.count("|") > 10:
            issues.append("Tables detected - ATS may not parse correctly")

        # Check length
        word_count = len(text.split())
        if word_count < 200:
            issues.append("Resume seems too short - consider adding more detail")
        elif word_count > 1500:
            issues.append("Resume may be too long - consider condensing to 2 pages")

        # Check for common issues
        if text.count("  ") > 20:
            issues.append("Excessive spacing detected - may cause parsing issues")

        # Check for special characters that might cause issues
        special_chars = ["", "", "", "", ""]
        if any(char in text for char in special_chars):
            issues.append("Special characters detected - use standard bullets and symbols")

        return issues

    def _generate_suggestions(
        self,
        missing_required: set[str],
        missing_keywords: set[str],
        format_issues: list[str],
        experience_gap: float,
        resume: Resume,
    ) -> list[str]:
        """Generate actionable improvement suggestions."""
        suggestions = []

        # Missing skills
        if missing_required:
            skills_list = ", ".join(list(missing_required)[:5])
            suggestions.append(
                f"Add these skills if you have experience: {skills_list}"
            )

        # Missing keywords
        if missing_keywords:
            kw_list = ", ".join(list(missing_keywords)[:5])
            suggestions.append(f"Consider adding keywords: {kw_list}")

        # Experience gap
        if experience_gap > 0:
            suggestions.append(
                f"You're {experience_gap:.0f} year(s) short of the experience requirement - "
                "highlight relevant projects and achievements"
            )

        # Check for quantification
        has_numbers = any(char.isdigit() for char in resume.raw_content)
        if not has_numbers:
            suggestions.append(
                "Add quantifiable achievements (e.g., 'increased sales by 30%', "
                "'reduced latency by 50ms')"
            )

        # Certification suggestion
        if len(resume.certifications) < 2:
            suggestions.append(
                "Consider adding relevant certifications to strengthen your application"
            )

        # Format issues
        if format_issues:
            suggestions.append("Fix formatting issues for better ATS parsing")

        return suggestions

    def _generate_keyword_analysis(
        self,
        resume_text: str,
        required_skills: set[str],
        all_job_skills: set[str],
        keywords: list[str],
        matched_skills: set[str],
        missing_skills: set[str],
    ) -> list[KeywordAnalysis]:
        """Generate detailed keyword-by-keyword analysis with weights."""
        analysis = []
        text_lower = resume_text.lower()

        # Analyze required skills (critical weight)
        for skill in required_skills:
            normalized = normalize_skill(skill)
            found = normalized in matched_skills or skill.lower() in text_lower
            observation = (
                f"Found '{skill}' in your resume - exact match with job requirement"
                if found
                else f"'{skill}' is a required skill but not found in your resume"
            )
            analysis.append(KeywordAnalysis(
                keyword=skill,
                found_in_resume=found,
                weight=KeywordWeight.CRITICAL,
                observation=observation,
            ))

        # Analyze preferred/additional skills (high weight)
        preferred_skills = all_job_skills - required_skills
        for skill in preferred_skills:
            normalized = normalize_skill(skill)
            found = normalized in matched_skills or skill.lower() in text_lower
            observation = (
                f"'{skill}' found - strengthens your application"
                if found
                else f"'{skill}' is preferred but not found - consider adding if applicable"
            )
            analysis.append(KeywordAnalysis(
                keyword=skill,
                found_in_resume=found,
                weight=KeywordWeight.HIGH,
                observation=observation,
            ))

        # Analyze additional keywords (medium weight)
        analyzed_keywords = required_skills | all_job_skills
        for keyword in keywords:
            if keyword.lower() not in {s.lower() for s in analyzed_keywords}:
                found = keyword.lower() in text_lower
                observation = (
                    f"Keyword '{keyword}' present - good for ATS parsing"
                    if found
                    else f"Consider adding '{keyword}' if relevant to your experience"
                )
                analysis.append(KeywordAnalysis(
                    keyword=keyword,
                    found_in_resume=found,
                    weight=KeywordWeight.MEDIUM,
                    observation=observation,
                ))

        return analysis

    def _generate_score_calculation(
        self,
        skill_score: float,
        experience_score: float,
        education_score: float,
        certification_score: float,
        keyword_score: float,
        total_score: float,
        matched_required: int,
        total_required: int,
    ) -> str:
        """Generate human-readable score calculation explanation."""
        lines = [
            "Score Calculation Breakdown:",
            f"",
            f"Skills ({self.weights.skill_match:.0f} pts max):",
            f"  - Matched {matched_required}/{total_required} required skills",
            f"  - Score: {skill_score:.1f}/{self.weights.skill_match:.0f}",
            f"",
            f"Experience ({self.weights.experience:.0f} pts max):",
            f"  - Score: {experience_score:.1f}/{self.weights.experience:.0f}",
            f"",
            f"Education ({self.weights.education:.0f} pts max):",
            f"  - Score: {education_score:.1f}/{self.weights.education:.0f}",
            f"",
            f"Certifications ({self.weights.certifications:.0f} pts max):",
            f"  - Score: {certification_score:.1f}/{self.weights.certifications:.0f}",
            f"",
            f"Keywords ({self.weights.keywords:.0f} pts max):",
            f"  - Score: {keyword_score:.1f}/{self.weights.keywords:.0f}",
            f"",
            f"TOTAL: {total_score:.1f}/100",
        ]
        return "\n".join(lines)
