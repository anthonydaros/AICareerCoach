"""Generate Coaching Tips Use Case."""

from typing import Any, Optional

from src.domain.entities.analysis_result import (
    CoachingTip,
    CoachingResult,
    GapAnalysis,
    GapImpact,
)
from src.infrastructure.llm import OpenAIGateway


# Learning path tiers with estimated times (P3.3)
LEARNING_PATHS: dict[str, dict[str, Any]] = {
    # Programming Languages
    "python": {"tier": "foundational", "hours": 40, "resources": ["Codecademy", "Python.org", "freeCodeCamp"]},
    "javascript": {"tier": "foundational", "hours": 50, "resources": ["MDN Web Docs", "freeCodeCamp", "JavaScript.info"]},
    "typescript": {"tier": "intermediate", "hours": 20, "resources": ["TypeScript Docs", "Total TypeScript"]},
    "java": {"tier": "foundational", "hours": 60, "resources": ["Oracle Java Tutorials", "Codecademy"]},
    "go": {"tier": "intermediate", "hours": 30, "resources": ["Go Tour", "Go by Example", "Gophercises"]},
    "rust": {"tier": "advanced", "hours": 80, "resources": ["Rust Book", "Rustlings", "Exercism"]},

    # Frameworks
    "react": {"tier": "intermediate", "hours": 40, "resources": ["React Docs", "Scrimba", "freeCodeCamp"]},
    "django": {"tier": "intermediate", "hours": 35, "resources": ["Django Docs", "Django Girls", "MDN"]},
    "fastapi": {"tier": "intermediate", "hours": 20, "resources": ["FastAPI Docs", "TestDriven.io"]},
    "node.js": {"tier": "intermediate", "hours": 30, "resources": ["Node.js Docs", "NodeSchool", "freeCodeCamp"]},
    "spring": {"tier": "advanced", "hours": 50, "resources": ["Spring.io", "Baeldung"]},
    "next.js": {"tier": "intermediate", "hours": 25, "resources": ["Next.js Docs", "Vercel Tutorials"]},

    # DevOps & Cloud
    "docker": {"tier": "intermediate", "hours": 25, "resources": ["Docker Docs", "Docker Mastery", "KodeKloud"]},
    "kubernetes": {"tier": "advanced", "hours": 60, "resources": ["Kubernetes.io", "KodeKloud", "CKAD Course"]},
    "aws": {"tier": "advanced", "hours": 80, "resources": ["AWS Training", "A Cloud Guru", "Tutorials Dojo"]},
    "terraform": {"tier": "intermediate", "hours": 30, "resources": ["Terraform Docs", "HashiCorp Learn"]},
    "ci/cd": {"tier": "intermediate", "hours": 20, "resources": ["GitHub Actions Docs", "GitLab CI Tutorials"]},
    "linux": {"tier": "foundational", "hours": 40, "resources": ["Linux Foundation", "Linux Journey"]},

    # Data & ML
    "sql": {"tier": "foundational", "hours": 30, "resources": ["SQLZoo", "Mode Analytics", "W3Schools"]},
    "postgresql": {"tier": "intermediate", "hours": 25, "resources": ["PostgreSQL Docs", "PostgreSQL Tutorial"]},
    "machine learning": {"tier": "advanced", "hours": 100, "resources": ["Andrew Ng's ML Course", "Fast.ai", "Kaggle"]},
    "pytorch": {"tier": "advanced", "hours": 60, "resources": ["PyTorch Tutorials", "Fast.ai", "Deep Learning with PyTorch"]},
    "tensorflow": {"tier": "advanced", "hours": 60, "resources": ["TensorFlow Tutorials", "Coursera Specialization"]},
    "langchain": {"tier": "intermediate", "hours": 25, "resources": ["LangChain Docs", "DeepLearning.AI Course"]},
    "llm": {"tier": "advanced", "hours": 50, "resources": ["Hugging Face Course", "DeepLearning.AI", "OpenAI Docs"]},

    # Soft Skills
    "leadership": {"tier": "advanced", "hours": 40, "resources": ["HBR Articles", "Manager Tools", "The Manager's Path"]},
    "communication": {"tier": "foundational", "hours": 20, "resources": ["Toastmasters", "Crucial Conversations Book"]},
    "system design": {"tier": "advanced", "hours": 60, "resources": ["System Design Primer", "Designing Data-Intensive Apps", "ByteByteGo"]},
}

TIER_ORDER = {"foundational": 1, "intermediate": 2, "advanced": 3}


class GenerateCoachingTipsUseCase:
    """Use case for generating career coaching tips with enhanced gap analysis."""

    def __init__(self, llm_gateway: OpenAIGateway):
        self.llm_gateway = llm_gateway

    async def execute(
        self,
        resume_summary: str,
        jobs_summary: str,
        match_results: list[dict[str, Any]],
        ats_score: Optional[float] = None,
        seniority_match: Optional[str] = None,
    ) -> CoachingResult:
        """
        Generate career coaching tips with gap analysis.

        Args:
            resume_summary: Summary of candidate's resume
            jobs_summary: Summary of all job postings
            match_results: List of job match results
            ats_score: Optional ATS score for probability calculation
            seniority_match: Optional seniority match status

        Returns:
            CoachingResult with tips, gap analysis, and recommendations
        """
        # Generate tips using LLM
        tips_data = await self.llm_gateway.generate_coaching_tips(
            resume_summary=resume_summary,
            jobs_summary=jobs_summary,
            match_results=match_results,
        )

        # Parse tips
        tips = self._parse_tips(tips_data)

        # Generate gap analysis from match results
        gap_analysis = self._generate_gap_analysis(match_results)

        # Calculate success probability
        success_probability = self._calculate_success_probability(
            match_results=match_results,
            ats_score=ats_score,
            seniority_match=seniority_match,
        )

        # Generate honest recommendation
        honest_recommendation = self._generate_honest_recommendation(
            match_results=match_results,
            success_probability=success_probability,
            seniority_match=seniority_match,
        )

        # Suggest alternative paths if needed
        alternative_paths = self._suggest_alternative_paths(
            match_results=match_results,
            success_probability=success_probability,
        )

        return CoachingResult(
            tips=tips,
            gap_analysis=gap_analysis,
            success_probability=success_probability,
            honest_recommendation=honest_recommendation,
            alternative_paths=alternative_paths,
        )

    def _parse_tips(self, tips_data: list[dict[str, Any]]) -> list[CoachingTip]:
        """Parse tips from LLM response."""
        tips = []
        for t in tips_data:
            if not isinstance(t, dict):
                continue

            title = t.get("title", "")
            if not title:
                continue

            tips.append(CoachingTip(
                category=t.get("category", "general"),
                title=title,
                description=t.get("description", ""),
                action_items=t.get("action_items", []),
                priority=t.get("priority", "medium"),
            ))

        return tips

    def _generate_gap_analysis(
        self,
        match_results: list[dict[str, Any]],
    ) -> list[GapAnalysis]:
        """Generate prioritized gap analysis from match results."""
        gaps = []
        priority = 1

        # Extract all missing skills and concerns from match results
        all_missing_required = set()
        all_concerns = []

        for match in match_results:
            # Get missing skills
            missing = match.get("missing_skills", [])
            skill_gaps = match.get("skill_gaps", [])

            # Required skills are high priority
            for gap in skill_gaps:
                if isinstance(gap, dict) and gap.get("is_required"):
                    all_missing_required.add(gap.get("skill", ""))

            # Collect concerns
            concerns = match.get("concerns", [])
            all_concerns.extend(concerns)

        # Create gap entries for missing required skills
        for skill in list(all_missing_required)[:5]:  # Top 5
            if not skill:
                continue

            impact = GapImpact.ELIMINATORY if priority <= 2 else GapImpact.HIGH

            gaps.append(GapAnalysis(
                gap=f"Missing required skill: {skill}",
                impact=impact,
                action=f"Learn {skill} through online courses, projects, or certifications",
                priority=priority,
            ))
            priority += 1

        # Add experience gaps from concerns
        for concern in all_concerns[:3]:
            if "experience" in concern.lower() or "year" in concern.lower():
                gaps.append(GapAnalysis(
                    gap=concern,
                    impact=GapImpact.HIGH,
                    action="Gain more experience through side projects, freelance work, or current role",
                    priority=priority,
                ))
                priority += 1
            elif "match" in concern.lower() or "skill" in concern.lower():
                gaps.append(GapAnalysis(
                    gap=concern,
                    impact=GapImpact.MEDIUM,
                    action="Address in cover letter by highlighting transferable skills",
                    priority=priority,
                ))
                priority += 1

        return gaps

    def _calculate_success_probability(
        self,
        match_results: list[dict[str, Any]],
        ats_score: Optional[float] = None,
        seniority_match: Optional[str] = None,
    ) -> str:
        """Calculate estimated success probability range."""
        if not match_results:
            return "Unknown"

        # Get best match percentage
        best_match = max(
            (m.get("match_percentage", 0) for m in match_results),
            default=0
        )

        # Start with base probability from match
        if best_match >= 80:
            base_prob = (60, 80)
        elif best_match >= 60:
            base_prob = (30, 50)
        elif best_match >= 40:
            base_prob = (15, 30)
        else:
            base_prob = (5, 15)

        # Adjust for ATS score
        if ats_score is not None:
            if ats_score >= 80:
                base_prob = (min(base_prob[0] + 10, 90), min(base_prob[1] + 10, 95))
            elif ats_score < 50:
                base_prob = (max(base_prob[0] - 10, 1), max(base_prob[1] - 10, 5))

        # Adjust for seniority match
        if seniority_match == "under-qualified":
            base_prob = (max(base_prob[0] - 15, 1), max(base_prob[1] - 10, 5))
        elif seniority_match == "over-qualified":
            base_prob = (max(base_prob[0] - 5, 5), max(base_prob[1] - 5, 15))

        return f"{base_prob[0]}-{base_prob[1]}%"

    def _generate_honest_recommendation(
        self,
        match_results: list[dict[str, Any]],
        success_probability: str,
        seniority_match: Optional[str] = None,
    ) -> str:
        """Generate honest assessment and recommendation."""
        if not match_results:
            return "Unable to provide assessment without match data."

        best_match = max(
            (m.get("match_percentage", 0) for m in match_results),
            default=0
        )

        # Parse probability for assessment
        prob_parts = success_probability.replace("%", "").split("-")
        max_prob = int(prob_parts[1]) if len(prob_parts) > 1 else 50

        if max_prob >= 50:
            return (
                "Strong application potential. Your profile aligns well with the target role(s). "
                "Focus on highlighting your relevant experience and preparing thoroughly for interviews. "
                "Address any skill gaps in your cover letter and be ready to discuss growth areas."
            )
        elif max_prob >= 25:
            return (
                "Moderate fit with room for growth. You have some relevant qualifications but also "
                "notable gaps. Consider this a stretch opportunity. Be strategic about which roles "
                "to apply for and invest time in addressing the most critical skill gaps before applying."
            )
        elif max_prob >= 10:
            return (
                "This role may be a significant stretch. Your current profile has substantial gaps "
                "compared to requirements. Consider: (1) gaining more relevant experience first, "
                "(2) targeting similar roles at a lower level, or (3) focusing on building the missing skills."
            )
        else:
            return (
                "Honest assessment: This role may not be the right fit currently. The gap between "
                "your profile and the requirements is significant. We recommend focusing on skill "
                "development and targeting roles that better match your current level. See alternative "
                "paths below for suggestions."
            )

    def _suggest_alternative_paths(
        self,
        match_results: list[dict[str, Any]],
        success_probability: str,
    ) -> list[str]:
        """Suggest alternative career paths if current match is low."""
        prob_parts = success_probability.replace("%", "").split("-")
        max_prob = int(prob_parts[1]) if len(prob_parts) > 1 else 50

        paths = []

        if max_prob < 30:
            # Collect matched skills to suggest related paths
            all_matched = set()
            for match in match_results:
                all_matched.update(match.get("matched_skills", []))

            paths.append(
                "Consider roles at one level below the target (e.g., if targeting Senior, apply for Mid-level)"
            )
            paths.append(
                "Look for similar roles in smaller companies where requirements may be more flexible"
            )
            paths.append(
                "Focus on building the missing skills through projects, courses, or certifications before applying"
            )

            if all_matched:
                skills_str = ", ".join(list(all_matched)[:3])
                paths.append(
                    f"Leverage your strengths ({skills_str}) in roles that prioritize these skills"
                )

        return paths

    def generate_learning_path(
        self,
        missing_skills: list[str],
    ) -> list[dict[str, Any]]:
        """
        Generate a prioritized learning path for missing skills (P3.3).

        Args:
            missing_skills: List of skills the candidate needs to learn

        Returns:
            List of learning milestones with tier, hours, and resources
        """
        learning_path = []

        for skill in missing_skills:
            skill_lower = skill.lower().strip()

            # Try exact match first
            if skill_lower in LEARNING_PATHS:
                path_info = LEARNING_PATHS[skill_lower]
                learning_path.append({
                    "skill": skill,
                    "tier": path_info["tier"],
                    "estimated_hours": path_info["hours"],
                    "resources": path_info["resources"],
                    "milestone": f"Complete {skill} fundamentals",
                })
            else:
                # Try partial match
                matched = False
                for known_skill, path_info in LEARNING_PATHS.items():
                    if known_skill in skill_lower or skill_lower in known_skill:
                        learning_path.append({
                            "skill": skill,
                            "tier": path_info["tier"],
                            "estimated_hours": path_info["hours"],
                            "resources": path_info["resources"],
                            "milestone": f"Complete {skill} fundamentals",
                        })
                        matched = True
                        break

                if not matched:
                    # Default learning path for unknown skills
                    learning_path.append({
                        "skill": skill,
                        "tier": "intermediate",
                        "estimated_hours": 30,
                        "resources": ["Udemy", "Coursera", "YouTube Tutorials", "Official Documentation"],
                        "milestone": f"Gain foundational knowledge in {skill}",
                    })

        # Sort by tier order (foundational first, then intermediate, then advanced)
        learning_path.sort(key=lambda x: TIER_ORDER.get(x["tier"], 2))

        return learning_path

    def get_total_learning_hours(self, learning_path: list[dict[str, Any]]) -> int:
        """Calculate total estimated learning hours for the path."""
        return sum(item.get("estimated_hours", 0) for item in learning_path)
