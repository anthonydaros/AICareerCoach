"""Career Coach Orchestrator - Coordinates the full analysis workflow."""

import asyncio
import logging
from typing import Any, Optional, List, Dict

from src.infrastructure.llm import OpenAIGateway
from src.domain.services.ats_scorer import ATSScorer
from src.domain.services.job_matcher import JobMatcher
from src.domain.services.seniority_detector import SeniorityDetector
from src.domain.services.stability_analyzer import StabilityAnalyzer
from src.application.use_cases import (
    ParseResumeUseCase,
    ParseJobPostingUseCase,
    CalculateATSScoreUseCase,
    MatchJobsUseCase,
    GenerateInterviewPrepUseCase,
    GenerateCoachingTipsUseCase,
)
from src.application.dtos.analysis_dto import (
    ATSResultDTO,
    JobMatchDTO,
    SkillGapDTO,
    BestFitDTO,
    InterviewQuestionDTO,
    CoachingTipDTO,
)

logger = logging.getLogger(__name__)


class CareerCoachOrchestrator:
    """
    Main orchestrator for career coach analysis.

    Coordinates the full workflow:
    1. Parse resume
    2. Parse job postings
    3. Calculate ATS score (against first job for overall score)
    4. Match resume against all jobs
    5. Identify best fit
    """

    def __init__(
        self,
        llm_gateway: Optional[OpenAIGateway] = None,
        ats_scorer: Optional[ATSScorer] = None,
        job_matcher: Optional[JobMatcher] = None,
        seniority_detector: Optional[SeniorityDetector] = None,
        stability_analyzer: Optional[StabilityAnalyzer] = None,
    ):
        self.llm_gateway = llm_gateway or OpenAIGateway()
        self.ats_scorer = ats_scorer or ATSScorer()
        self.job_matcher = job_matcher or JobMatcher()
        self.seniority_detector = seniority_detector or SeniorityDetector()
        self.stability_analyzer = stability_analyzer or StabilityAnalyzer()

        # Initialize use cases
        self.parse_resume_uc = ParseResumeUseCase(self.llm_gateway)
        self.parse_job_uc = ParseJobPostingUseCase(self.llm_gateway)
        self.calculate_ats_uc = CalculateATSScoreUseCase(self.ats_scorer)
        self.match_jobs_uc = MatchJobsUseCase(self.job_matcher)
        self.interview_prep_uc = GenerateInterviewPrepUseCase(self.llm_gateway)
        self.coaching_tips_uc = GenerateCoachingTipsUseCase(self.llm_gateway)

    async def analyze(
        self,
        resume_text: str,
        job_postings: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Perform full analysis of resume against job postings.

        Args:
            resume_text: Raw resume text
            job_postings: List of dicts with 'id' and 'text' keys

        Returns:
            Dictionary with ats_result, job_matches, and best_fit
        """
        logger.info(f"Starting analysis for {len(job_postings)} job(s)")

        # 1. Parse resume
        resume = await self.parse_resume_uc.execute(resume_text)
        logger.info(f"Parsed resume: {len(resume.skills)} skills, {resume.total_experience_years} years exp")

        # 2. Parse all job postings in parallel (PERFORMANCE: avoids N+1 sequential calls)
        async def parse_job(jp: dict) -> Any:
            job = await self.parse_job_uc.execute(jp["id"], jp["text"])
            logger.info(f"Parsed job: {job.title} with {len(job.requirements)} requirements")
            return job

        jobs = await asyncio.gather(*[parse_job(jp) for jp in job_postings])
        jobs = list(jobs)  # Convert tuple to list

        # 3. Calculate ATS score (use first job as reference)
        if jobs:
            ats_result = self.calculate_ats_uc.execute(resume, jobs[0])
        else:
            # No jobs, create empty result
            from src.domain.entities.analysis_result import ATSResult
            ats_result = ATSResult(
                total_score=0,
                skill_score=0,
                experience_score=0,
                education_score=0,
                certification_score=0,
                keyword_score=0,
                matched_keywords=[],
                missing_keywords=[],
                format_issues=[],
                improvement_suggestions=["Please add job postings to analyze"],
            )

        # 4. Match resume against all jobs
        job_matches = self.match_jobs_uc.execute(resume, jobs)

        # 5. Identify best fit
        best_fit = None
        if job_matches:
            best_match = job_matches[0]  # Already sorted by percentage
            best_fit = self._create_best_fit(best_match)

        # 6. Detect seniority level (pass first job for job fit comparison)
        first_job = jobs[0] if jobs else None
        seniority = self.seniority_detector.detect(resume, first_job)
        logger.info(f"Detected seniority: {seniority.level.value} ({seniority.confidence}% confidence)")

        # 7. Analyze career stability
        stability = self.stability_analyzer.analyze(resume)
        logger.info(f"Stability score: {stability.score}/100, flags: {[f.value for f in stability.flags]}")

        # 8. Generate interview prep for best-fit job
        interview_prep_data = None
        if best_fit and jobs:
            best_job = jobs[0]  # Already sorted by match percentage
            best_match = job_matches[0] if job_matches else None
            skill_gaps = list(best_match.missing_skills)[:5] if best_match else []

            try:
                interview_questions = await self.llm_gateway.generate_interview_questions(
                    resume_summary=self._get_resume_summary(resume),
                    job_summary=self._get_job_summary(best_job),
                    skill_gaps=skill_gaps,
                    seniority_level=seniority.level.value if seniority else "mid",
                )
                interview_prep_data = {
                    "job_title": best_job.get_display_title(),
                    "questions": interview_questions,
                }
                logger.info(f"Generated {len(interview_questions)} interview questions")
            except Exception as e:
                logger.warning(f"Failed to generate interview prep: {e}")
                interview_prep_data = {"job_title": None, "questions": []}

        # 9. Generate coaching tips
        coaching_tips_data = None
        try:
            match_results_for_coaching = [
                {
                    "job_title": m.job_title,
                    "match_percentage": m.match_percentage,
                    "missing_skills": list(m.missing_skills),
                }
                for m in job_matches
            ]
            coaching_tips = await self.llm_gateway.generate_coaching_tips(
                resume_summary=self._get_resume_summary(resume),
                jobs_summary="\n".join(j.get_display_title() for j in jobs) if jobs else "",
                match_results=match_results_for_coaching,
            )
            coaching_tips_data = {
                "tips": coaching_tips,
            }
            logger.info(f"Generated {len(coaching_tips)} coaching tips")
        except Exception as e:
            logger.warning(f"Failed to generate coaching tips: {e}")
            coaching_tips_data = {"tips": []}

        # Convert to DTOs
        return {
            "ats_result": self._ats_to_dto(ats_result),
            "job_matches": [self._match_to_dto(m) for m in job_matches],
            "best_fit": best_fit,
            "seniority": self._seniority_to_dto(seniority),
            "stability": self._stability_to_dto(stability),
            "interview_prep": interview_prep_data,
            "coaching_tips": coaching_tips_data,
        }

    async def generate_interview_prep(
        self,
        resume_text: str,
        job_text: str,
        skill_gaps: Optional[List[str]] = None,
    ) -> dict[str, Any]:
        """
        Generate interview preparation questions for a specific job.

        Args:
            resume_text: Raw resume text
            job_text: Raw job posting text
            skill_gaps: Optional list of known skill gaps

        Returns:
            Dictionary with job_title and questions
        """
        # Parse resume and job
        resume = await self.parse_resume_uc.execute(resume_text)
        job = await self.parse_job_uc.execute("interview-job", job_text)

        # Get resume summary
        resume_summary = self._get_resume_summary(resume)

        # Get job summary
        job_summary = self._get_job_summary(job)

        # Calculate gaps if not provided
        if not skill_gaps:
            match = self.job_matcher.match_all(resume, [job])
            if match:
                skill_gaps = list(match[0].missing_skills)[:5]
            else:
                skill_gaps = []

        # Generate interview prep (now returns InterviewPrep entity)
        interview_prep = await self.interview_prep_uc.execute(
            resume_summary=resume_summary,
            job_summary=job_summary,
            skill_gaps=skill_gaps,
            job_title=job.get_display_title(),
        )

        # Convert questions by category to DTO
        questions_by_category_dto = {
            cat: [self._question_to_dto(q) for q in qs]
            for cat, qs in interview_prep.questions_by_category.items()
        }

        return {
            "job_title": job.get_display_title(),
            "questions": [self._question_to_dto(q) for q in interview_prep.questions],
            # Enhanced fields
            "questions_by_category": questions_by_category_dto,
            "preparation_tips": list(interview_prep.preparation_tips),
            "questions_to_ask_interviewer": list(interview_prep.questions_to_ask_interviewer),
        }

    async def generate_coaching_tips(
        self,
        resume_text: str,
        job_postings: list[dict[str, str]],
        match_results: Optional[List[Dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """
        Generate career coaching tips.

        Args:
            resume_text: Raw resume text
            job_postings: List of job posting dicts
            match_results: Optional pre-computed match results

        Returns:
            Dictionary with tips
        """
        # Parse resume and jobs
        resume = await self.parse_resume_uc.execute(resume_text)

        jobs = []
        for jp in job_postings:
            job = await self.parse_job_uc.execute(jp["id"], jp["text"])
            jobs.append(job)

        # Calculate matches if not provided
        if not match_results:
            matches = self.job_matcher.match_all(resume, jobs)
            match_results = [
                {
                    "job_title": m.job_title,
                    "match_percentage": m.match_percentage,
                    "missing_skills": list(m.missing_skills),
                }
                for m in matches
            ]

        # Get summaries
        resume_summary = self._get_resume_summary(resume)
        jobs_summary = "\n".join(j.get_display_title() for j in jobs)

        # Calculate ATS score and seniority for coaching context
        ats_score = None
        seniority_match = None
        if jobs:
            ats_result = self.calculate_ats_uc.execute(resume, jobs[0])
            ats_score = ats_result.total_score
            seniority = self.seniority_detector.detect(resume, jobs[0])
            seniority_match = getattr(seniority, 'seniority_match', None)

        # Generate coaching result (now returns CoachingResult entity)
        coaching_result = await self.coaching_tips_uc.execute(
            resume_summary=resume_summary,
            jobs_summary=jobs_summary,
            match_results=match_results,
            ats_score=ats_score,
            seniority_match=seniority_match,
        )

        return {
            "tips": [self._tip_to_dto(t) for t in coaching_result.tips],
            # Enhanced fields
            "gap_analysis": [
                {
                    "gap": g.gap,
                    "impact": g.impact.value,
                    "action": g.action,
                    "priority": g.priority,
                }
                for g in coaching_result.gap_analysis
            ],
            "success_probability": coaching_result.success_probability,
            "honest_recommendation": coaching_result.honest_recommendation,
            "alternative_paths": list(coaching_result.alternative_paths),
        }

    def _get_resume_summary(self, resume) -> str:
        """Create a text summary of the resume."""
        parts = []
        parts.append(f"Experience: {resume.total_experience_years:.0f} years")

        if resume.skills:
            skill_names = [s.normalized_name for s in resume.skills[:10]]
            parts.append(f"Skills: {', '.join(skill_names)}")

        if resume.experiences:
            exp = resume.experiences[0]
            parts.append(f"Recent role: {exp.title} at {exp.company}")

        if resume.education:
            edu = resume.education[0]
            parts.append(f"Education: {edu.degree} in {edu.field}")

        if resume.certifications:
            parts.append(f"Certifications: {', '.join(resume.certifications[:3])}")

        return "\n".join(parts)

    def _get_job_summary(self, job) -> str:
        """Create a text summary of the job posting."""
        parts = []
        parts.append(f"Position: {job.get_display_title()}")

        required = job.get_required_skills()
        if required:
            parts.append(f"Required: {', '.join(list(required)[:10])}")

        preferred = job.get_nice_to_have_skills()
        if preferred:
            parts.append(f"Preferred: {', '.join(list(preferred)[:5])}")

        if job.min_experience_years > 0:
            parts.append(f"Min experience: {job.min_experience_years} years")

        return "\n".join(parts)

    def _create_best_fit(self, match) -> dict[str, Any]:
        """Create best fit recommendation from match."""
        if match.match_percentage >= 80:
            rec = "Apply immediately - you're highly qualified"
        elif match.match_percentage >= 60:
            rec = "Strong candidate - apply with confidence"
        elif match.match_percentage >= 40:
            rec = "Consider applying but address skill gaps"
        else:
            rec = "May need upskilling before applying"

        return {
            "job_id": match.job_id,
            "job_title": f"{match.job_title}" + (f" @ {match.company}" if match.company else ""),
            "match_percentage": match.match_percentage,
            "recommendation": rec,
        }

    def _ats_to_dto(self, result) -> dict[str, Any]:
        """Convert ATSResult to DTO dict."""
        return {
            "total_score": result.total_score,
            "skill_score": result.skill_score,
            "experience_score": result.experience_score,
            "education_score": result.education_score,
            "certification_score": result.certification_score,
            "keyword_score": result.keyword_score,
            "matched_keywords": list(result.matched_keywords),
            "missing_keywords": list(result.missing_keywords),
            "format_issues": list(result.format_issues),
            "improvement_suggestions": list(result.improvement_suggestions),
            # Enhanced fields
            "keyword_analysis": [
                {
                    "keyword": ka.keyword,
                    "found_in_resume": ka.found_in_resume,
                    "weight": ka.weight.value,
                    "observation": ka.observation,
                }
                for ka in result.keyword_analysis
            ],
            "score_calculation": result.score_calculation,
            "methodology": result.methodology,
        }

    def _match_to_dto(self, match) -> dict[str, Any]:
        """Convert JobMatch to DTO dict."""
        return {
            "job_id": match.job_id,
            "job_title": match.job_title,
            "company": match.company,
            "match_percentage": match.match_percentage,
            "match_level": match.match_level.value,
            "matched_skills": list(match.matched_skills),
            "missing_skills": list(match.missing_skills),
            "skill_gaps": [
                {
                    "skill": g.skill,
                    "is_required": g.is_required,
                    "suggestion": g.suggestion,
                    "learning_resources": list(g.learning_resources),
                }
                for g in match.skill_gaps
            ],
            "strengths": list(match.strengths),
            "concerns": list(match.concerns),
            "is_best_fit": match.is_best_fit,
            # Enhanced fields
            "requirement_matrix": [
                {
                    "requirement": rm.requirement,
                    "candidate_experience": rm.candidate_experience,
                    "match_percentage": rm.match_percentage,
                    "logic": rm.logic,
                }
                for rm in match.requirement_matrix
            ],
            "weighted_calculation": match.weighted_calculation,
            "transferable_skills": list(match.transferable_skills),
        }

    def _question_to_dto(self, q) -> dict[str, Any]:
        """Convert InterviewQuestion to DTO dict."""
        result = {
            "question": q.question,
            "category": q.category,
            "why_asked": q.why_asked,
            "what_to_say": list(q.what_to_say),
            "what_to_avoid": list(q.what_to_avoid),
            # Enhanced fields
            "your_angle": q.your_angle,
            "star_guidance": None,
        }
        # Add STAR guidance if present
        if q.star_guidance:
            result["star_guidance"] = {
                "situation": q.star_guidance.situation,
                "task": q.star_guidance.task,
                "action": q.star_guidance.action,
                "result": q.star_guidance.result,
            }
        return result

    def _tip_to_dto(self, t) -> dict[str, Any]:
        """Convert CoachingTip to DTO dict."""
        return {
            "category": t.category,
            "title": t.title,
            "description": t.description,
            "action_items": list(t.action_items),
            "priority": t.priority,
        }

    def _seniority_to_dto(self, seniority) -> dict[str, Any]:
        """Convert SeniorityResult to DTO dict."""
        result = {
            "level": seniority.level.value,
            "confidence": seniority.confidence,
            "years_experience": seniority.years_experience,
            "scores": {
                "experience": round(seniority.scores.get("experience", 0), 2),
                "complexity": round(seniority.scores.get("complexity", 0), 2),
                "autonomy": round(seniority.scores.get("autonomy", 0), 2),
                "skills": round(seniority.scores.get("skills", 0), 2),
                "leadership": round(seniority.scores.get("leadership", 0), 2),
                "impact": round(seniority.scores.get("impact", 0), 2),
            },
            "indicators": list(seniority.indicators),
            # Enhanced fields
            "axis_comparison": [
                {
                    "axis": ax.axis,
                    "candidate_level": ax.candidate_level,
                    "evidence": ax.evidence,
                    "job_expected_level": ax.job_expected_level,
                }
                for ax in seniority.axis_comparison
            ] if hasattr(seniority, 'axis_comparison') else [],
            "job_fit_assessment": getattr(seniority, 'job_fit_assessment', ""),
            "gap_analysis": getattr(seniority, 'gap_analysis', ""),
            "seniority_match": getattr(seniority, 'seniority_match', ""),
        }
        return result

    def _stability_to_dto(self, stability) -> dict[str, Any]:
        """Convert StabilityResult to DTO dict."""
        return {
            "score": stability.score,
            "flags": [f.value for f in stability.flags],
            "indicators": list(stability.indicators),
            "positive_notes": list(stability.positive_notes),
            "avg_tenure_months": stability.avg_tenure_months,
            "total_companies": stability.total_companies,
            "companies_in_5_years": stability.companies_in_5_years,
            "consecutive_short_jobs": stability.consecutive_short_jobs,
            "gaps": [
                {
                    "after_company": g.after_company,
                    "before_company": g.before_company,
                    "start_year": g.start_year,
                    "end_year": g.end_year,
                    "months": g.months,
                }
                for g in stability.gaps
            ],
        }
