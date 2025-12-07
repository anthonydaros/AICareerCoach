"""Job Matcher Service - Matches resume against multiple job postings."""

from src.domain.entities.resume import Resume
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.analysis_result import JobMatch, MatchLevel, SkillGap
from src.domain.services.skill_relationships import expand_skills, normalize_skill


class JobMatcher:
    """Service for matching resume against multiple job postings."""

    def match_all(
        self,
        resume: Resume,
        jobs: list[JobPosting],
    ) -> list[JobMatch]:
        """
        Match resume against all jobs and rank them.

        Args:
            resume: Parsed resume entity
            jobs: List of job posting entities

        Returns:
            List of JobMatch results, sorted by match percentage (descending)
        """
        if not jobs:
            return []

        matches = [self._match_single(resume, job) for job in jobs]

        # Sort by match percentage (descending)
        matches.sort(key=lambda m: m.match_percentage, reverse=True)

        # Mark best fit (first in sorted list)
        if matches:
            best = matches[0]
            matches[0] = JobMatch(
                job_id=best.job_id,
                job_title=best.job_title,
                company=best.company,
                match_percentage=best.match_percentage,
                match_level=best.match_level,
                matched_skills=best.matched_skills,
                missing_skills=best.missing_skills,
                skill_gaps=best.skill_gaps,
                strengths=best.strengths,
                concerns=best.concerns,
                is_best_fit=True,
            )

        return matches

    def _match_single(self, resume: Resume, job: JobPosting) -> JobMatch:
        """
        Calculate match for a single job with intelligent skill inference.

        Args:
            resume: Parsed resume entity
            job: Job posting entity

        Returns:
            JobMatch result
        """
        resume_skills = resume.get_skill_names()
        required = job.get_required_skills()
        preferred = job.get_nice_to_have_skills()

        # Normalize all skills for consistent matching
        normalized_resume = {normalize_skill(s) for s in resume_skills}
        normalized_required = {normalize_skill(s) for s in required}
        normalized_preferred = {normalize_skill(s) for s in preferred}

        # Expand resume skills with inferred knowledge
        # e.g., "Python" -> includes "pytorch", "tensorflow", etc.
        expanded_resume_skills = expand_skills(normalized_resume)

        # Calculate skill matches using expanded skills
        matched_required = expanded_resume_skills & normalized_required
        matched_preferred = expanded_resume_skills & normalized_preferred
        missing_required = normalized_required - expanded_resume_skills
        missing_preferred = normalized_preferred - expanded_resume_skills

        # Calculate match percentage
        # Weight: 70% required skills, 20% preferred skills, 10% experience
        required_match = len(matched_required) / len(normalized_required) if normalized_required else 1.0
        preferred_match = len(matched_preferred) / len(normalized_preferred) if normalized_preferred else 1.0

        # Experience factor
        if job.min_experience_years > 0:
            exp_factor = min(resume.total_experience_years / job.min_experience_years, 1.0)
        else:
            exp_factor = 1.0

        match_pct = (
            (required_match * 0.70) +
            (preferred_match * 0.20) +
            (exp_factor * 0.10)
        ) * 100

        # Determine match level
        match_level = self._get_match_level(match_pct)

        # Build skill gaps with suggestions
        skill_gaps = self._build_skill_gaps(missing_required, missing_preferred)

        # Identify strengths
        strengths = self._identify_strengths(
            resume=resume,
            job=job,
            matched_required=matched_required,
            matched_preferred=matched_preferred,
        )

        # Identify concerns
        concerns = self._identify_concerns(
            resume=resume,
            job=job,
            missing_required=missing_required,
        )

        return JobMatch(
            job_id=job.id,
            job_title=job.title or "Unknown Position",
            company=job.company,
            match_percentage=round(match_pct, 1),
            match_level=match_level,
            matched_skills=list(matched_required | matched_preferred),
            missing_skills=list(missing_required | missing_preferred),
            skill_gaps=skill_gaps,
            strengths=strengths,
            concerns=concerns,
            is_best_fit=False,
        )

    def _get_match_level(self, percentage: float) -> MatchLevel:
        """Determine match level from percentage."""
        if percentage >= 80:
            return MatchLevel.EXCELLENT
        elif percentage >= 60:
            return MatchLevel.GOOD
        elif percentage >= 40:
            return MatchLevel.FAIR
        else:
            return MatchLevel.POOR

    def _build_skill_gaps(
        self,
        missing_required: set[str],
        missing_preferred: set[str],
    ) -> list[SkillGap]:
        """Build detailed skill gap list."""
        gaps = []

        # Required skills first
        for skill in sorted(missing_required):
            gaps.append(SkillGap(
                skill=skill,
                is_required=True,
                suggestion=f"Learn {skill} to qualify for this role - it's a required skill",
                learning_resources=self._get_learning_resources(skill),
            ))

        # Preferred skills (top 3)
        for skill in sorted(list(missing_preferred)[:3]):
            gaps.append(SkillGap(
                skill=skill,
                is_required=False,
                suggestion=f"{skill} would strengthen your application as a nice-to-have skill",
                learning_resources=self._get_learning_resources(skill),
            ))

        return gaps

    def _get_learning_resources(self, skill: str) -> list[str]:
        """Get learning resources for a skill."""
        # General resources - could be expanded with a larger mapping
        skill_lower = skill.lower()

        if any(kw in skill_lower for kw in ["python", "javascript", "typescript", "java", "go"]):
            return [
                "Official documentation",
                "Codecademy free course",
                "Build a personal project",
            ]
        elif any(kw in skill_lower for kw in ["kubernetes", "k8s", "docker"]):
            return [
                "Kubernetes official tutorials",
                "Docker/K8s Udemy courses",
                "Deploy a personal project to K8s",
            ]
        elif any(kw in skill_lower for kw in ["aws", "gcp", "azure", "cloud"]):
            return [
                "Cloud provider free tier",
                "A Cloud Guru courses",
                "Get certified (AWS SAA, etc.)",
            ]
        elif any(kw in skill_lower for kw in ["ml", "machine learning", "ai", "langchain"]):
            return [
                "Fast.ai free course",
                "LangChain documentation",
                "Build a RAG project",
            ]
        else:
            return [
                "Online tutorials and documentation",
                "Udemy/Coursera courses",
                "Practice with personal projects",
            ]

    def _identify_strengths(
        self,
        resume: Resume,
        job: JobPosting,
        matched_required: set[str],
        matched_preferred: set[str],
    ) -> list[str]:
        """Identify candidate strengths for this role."""
        strengths = []

        # Experience match
        if resume.total_experience_years >= job.min_experience_years:
            if resume.total_experience_years > job.min_experience_years:
                strengths.append(
                    f"Experience ({resume.total_experience_years:.0f} yrs) exceeds "
                    f"requirement ({job.min_experience_years} yrs)"
                )
            else:
                strengths.append(
                    f"Experience ({resume.total_experience_years:.0f} yrs) meets requirement"
                )

        # Strong skill matches
        if len(matched_required) >= 3:
            top_skills = list(matched_required)[:3]
            strengths.append(
                f"Strong match on core skills: {', '.join(top_skills)}"
            )
        elif matched_required:
            strengths.append(
                f"Matches {len(matched_required)} required skill(s)"
            )

        # Preferred skills bonus
        if matched_preferred:
            strengths.append(
                f"Also has {len(matched_preferred)} preferred skill(s)"
            )

        # Education (if relevant)
        if resume.education:
            strengths.append(f"Has relevant education: {resume.education[0].degree}")

        # Certifications
        if resume.certifications:
            strengths.append(
                f"Has {len(resume.certifications)} certification(s)"
            )

        return strengths

    def _identify_concerns(
        self,
        resume: Resume,
        job: JobPosting,
        missing_required: set[str],
    ) -> list[str]:
        """Identify potential concerns for this role."""
        concerns = []

        # Missing required skills
        if missing_required:
            count = len(missing_required)
            if count >= 3:
                concerns.append(f"Missing {count} required skills - significant gap")
            elif count > 0:
                concerns.append(f"Missing {count} required skill(s)")

        # Experience gap
        exp_gap = job.min_experience_years - resume.total_experience_years
        if exp_gap > 0:
            concerns.append(f"Need {exp_gap:.0f} more year(s) of experience")

        # Low skill match overall
        required = job.get_required_skills()
        if required:
            match_rate = (len(required) - len(missing_required)) / len(required)
            if match_rate < 0.5:
                concerns.append("Less than 50% skill match with requirements")

        return concerns
