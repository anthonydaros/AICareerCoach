"""Career Stability Analyzer - Analyzes professional behavior like a Tech Recruiter."""

import logging
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from src.domain.entities.resume import Resume, Experience

logger = logging.getLogger(__name__)


class StabilityFlag(str, Enum):
    """Flags indicating career stability patterns."""
    JOB_HOPPER = "job_hopper"
    SHORT_TENURE = "short_tenure"
    EMPLOYMENT_GAP = "employment_gap"
    SENIORITY_REGRESSION = "seniority_regression"
    CONSECUTIVE_SHORT_JOBS = "consecutive_short_jobs"
    # Positive flags
    STABLE_CAREER = "stable_career"
    CAREER_PROGRESSION = "career_progression"
    LONG_TENURE = "long_tenure"


@dataclass
class GapInfo:
    """Information about an employment gap."""
    after_company: str
    before_company: str
    start_year: int
    end_year: int
    months: int


@dataclass
class TimelineEntry:
    """A single entry in the career timeline."""
    company: str
    title: str
    start_year: int
    end_year: Optional[int]
    duration_months: int
    seniority_level: int


@dataclass
class StabilityResult:
    """Result of career stability analysis."""
    score: int  # 0-100
    flags: List[StabilityFlag]
    indicators: List[str]
    positive_notes: List[str]
    timeline: List[TimelineEntry]
    avg_tenure_months: float
    total_companies: int
    gaps: List[GapInfo]
    companies_in_5_years: int
    consecutive_short_jobs: int


# Title seniority mapping for regression detection
TITLE_SENIORITY_KEYWORDS = {
    # Level 1 - Entry/Intern
    "intern": 1, "estagiario": 1, "estagiária": 1, "trainee": 1, "aprendiz": 1,

    # Level 2 - Junior
    "junior": 2, "júnior": 2, "jr": 2, "associate": 2, "assistente": 2,

    # Level 3 - Mid/Pleno
    "pleno": 3, "mid": 3, "mid-level": 3, "analista": 3,

    # Level 4 - Senior
    "senior": 4, "sênior": 4, "sr": 4, "specialist": 4, "especialista": 4,

    # Level 5 - Lead/Staff
    "lead": 5, "staff": 5, "tech lead": 5, "principal": 5, "líder": 5,
    "lider": 5, "coordenador": 5, "coordinator": 5,

    # Level 6 - Manager/Head
    "manager": 6, "gerente": 6, "head": 6, "supervisor": 6,

    # Level 7 - Director
    "director": 7, "diretor": 7, "vp": 7, "vice president": 7,

    # Level 8 - C-Level
    "cto": 8, "cio": 8, "ceo": 8, "chief": 8, "c-level": 8,
}


class StabilityAnalyzer:
    """
    Analyzes career stability patterns from resume data.

    Performs heuristic analysis without LLM, detecting:
    - Job hopping (too many companies in short time)
    - Short tenure (average time per company)
    - Employment gaps
    - Seniority regression (title downgrade)
    - Consecutive short jobs
    """

    def __init__(self):
        self.current_year = datetime.now().year

    def analyze(self, resume: Resume) -> StabilityResult:
        """
        Analyze career stability from resume.

        Args:
            resume: Parsed resume with experiences

        Returns:
            StabilityResult with score, flags, and indicators
        """
        if not resume.experiences:
            return self._empty_result()

        # Build timeline from experiences
        timeline = self._build_timeline(resume.experiences)

        # Calculate metrics
        avg_tenure = self._calculate_avg_tenure(timeline)
        total_companies = len(set(e.company for e in timeline))
        gaps = self._detect_gaps(timeline)
        companies_5y = self._count_companies_in_window(timeline, years=5)
        consecutive_short = self._count_consecutive_short_jobs(timeline)
        has_regression = self._detect_seniority_regression(timeline)

        # Calculate score and flags
        score, flags, indicators = self._calculate_score(
            avg_tenure=avg_tenure,
            total_companies=total_companies,
            gaps=gaps,
            companies_5y=companies_5y,
            consecutive_short=consecutive_short,
            has_regression=has_regression,
            timeline=timeline,
        )

        # Detect positive patterns
        positive_notes = self._detect_positive_patterns(timeline, avg_tenure)

        return StabilityResult(
            score=score,
            flags=flags,
            indicators=indicators,
            positive_notes=positive_notes,
            timeline=timeline,
            avg_tenure_months=round(avg_tenure, 1),
            total_companies=total_companies,
            gaps=gaps,
            companies_in_5_years=companies_5y,
            consecutive_short_jobs=consecutive_short,
        )

    def _empty_result(self) -> StabilityResult:
        """Return empty result when no experiences."""
        return StabilityResult(
            score=50,
            flags=[],
            indicators=["No work experience to analyze"],
            positive_notes=[],
            timeline=[],
            avg_tenure_months=0,
            total_companies=0,
            gaps=[],
            companies_in_5_years=0,
            consecutive_short_jobs=0,
        )

    def _build_timeline(self, experiences: List[Experience]) -> List[TimelineEntry]:
        """Build chronological timeline from experiences."""
        timeline = []

        for exp in experiences:
            # Extract seniority from title
            seniority = self._extract_seniority_from_title(exp.title)

            # Determine years
            start_year = exp.start_year
            end_year = exp.end_year

            # If no years provided, estimate from duration
            if start_year is None:
                # Estimate backwards from current year or previous job
                estimated_end = end_year or self.current_year
                years_duration = exp.duration_months / 12
                start_year = int(estimated_end - years_duration)

            if end_year is None and start_year:
                # Assume current job or calculate from duration
                end_year = start_year + int(exp.duration_months / 12)
                if end_year >= self.current_year:
                    end_year = None  # Current job

            timeline.append(TimelineEntry(
                company=exp.company,
                title=exp.title,
                start_year=start_year or self.current_year,
                end_year=end_year,
                duration_months=exp.duration_months,
                seniority_level=seniority,
            ))

        # Sort by start year (most recent first)
        timeline.sort(key=lambda x: x.start_year, reverse=True)

        return timeline

    def _extract_seniority_from_title(self, title: str) -> int:
        """Extract seniority level from job title."""
        title_lower = title.lower()

        # Check for specific keywords
        max_level = 3  # Default to mid-level

        for keyword, level in TITLE_SENIORITY_KEYWORDS.items():
            if keyword in title_lower:
                max_level = max(max_level, level)

        return max_level

    def _calculate_avg_tenure(self, timeline: List[TimelineEntry]) -> float:
        """Calculate average tenure in months."""
        if not timeline:
            return 0

        total_months = sum(e.duration_months for e in timeline)
        return total_months / len(timeline)

    def _detect_gaps(self, timeline: List[TimelineEntry]) -> List[GapInfo]:
        """Detect employment gaps > 6 months."""
        gaps = []

        # Need at least 2 jobs to have gaps
        if len(timeline) < 2:
            return gaps

        # Timeline is sorted most recent first, so iterate backwards
        for i in range(len(timeline) - 1, 0, -1):
            older_job = timeline[i]
            newer_job = timeline[i - 1]

            # Calculate gap
            older_end = older_job.end_year or self.current_year
            newer_start = newer_job.start_year

            if newer_start > older_end:
                gap_years = newer_start - older_end
                gap_months = gap_years * 12

                if gap_months >= 6:
                    gaps.append(GapInfo(
                        after_company=older_job.company,
                        before_company=newer_job.company,
                        start_year=older_end,
                        end_year=newer_start,
                        months=gap_months,
                    ))

        return gaps

    def _count_companies_in_window(self, timeline: List[TimelineEntry], years: int = 5) -> int:
        """Count unique companies in the last N years."""
        cutoff_year = self.current_year - years

        companies = set()
        for entry in timeline:
            end_year = entry.end_year or self.current_year
            if end_year >= cutoff_year:
                companies.add(entry.company)

        return len(companies)

    def _count_consecutive_short_jobs(self, timeline: List[TimelineEntry], threshold_months: int = 12) -> int:
        """Count consecutive jobs with tenure < threshold."""
        if len(timeline) < 2:
            return 0

        max_consecutive = 0
        current_streak = 0

        for entry in timeline:
            if entry.duration_months < threshold_months:
                current_streak += 1
                max_consecutive = max(max_consecutive, current_streak)
            else:
                current_streak = 0

        return max_consecutive

    def _detect_seniority_regression(self, timeline: List[TimelineEntry]) -> bool:
        """Detect if candidate had a title downgrade."""
        if len(timeline) < 2:
            return False

        # Timeline is most recent first
        # Check if any older job had higher seniority than a newer job
        for i in range(len(timeline) - 1):
            newer_job = timeline[i]
            older_job = timeline[i + 1]

            # If older job was higher level than newer job = regression
            if older_job.seniority_level > newer_job.seniority_level:
                return True

        return False

    def _calculate_score(
        self,
        avg_tenure: float,
        total_companies: int,
        gaps: List[GapInfo],
        companies_5y: int,
        consecutive_short: int,
        has_regression: bool,
        timeline: List[TimelineEntry],
    ) -> tuple:
        """Calculate stability score and identify flags."""
        score = 100
        flags = []
        indicators = []

        # Short average tenure
        if avg_tenure < 12:
            score -= 20
            flags.append(StabilityFlag.SHORT_TENURE)
            indicators.append(f"Very short average tenure of {avg_tenure:.0f} months (below 12 months)")
        elif avg_tenure < 18:
            score -= 10
            indicators.append(f"Below average tenure of {avg_tenure:.0f} months (ideal is 24+ months)")

        # Job hopping - too many companies in 5 years
        if companies_5y > 4:
            score -= 15
            flags.append(StabilityFlag.JOB_HOPPER)
            indicators.append(f"{companies_5y} companies in the last 5 years (indicates job hopping)")
        elif companies_5y > 3:
            score -= 5
            indicators.append(f"{companies_5y} companies in the last 5 years (slightly high)")

        # Employment gaps
        for gap in gaps:
            score -= 10
            flags.append(StabilityFlag.EMPLOYMENT_GAP)
            indicators.append(
                f"Employment gap of {gap.months} months between "
                f"{gap.after_company} and {gap.before_company} ({gap.start_year}-{gap.end_year})"
            )

        # Consecutive short jobs
        if consecutive_short >= 2:
            score -= 15
            flags.append(StabilityFlag.CONSECUTIVE_SHORT_JOBS)
            indicators.append(f"{consecutive_short} consecutive jobs with tenure under 12 months")

        # Seniority regression
        if has_regression:
            score -= 20
            flags.append(StabilityFlag.SENIORITY_REGRESSION)
            indicators.append("Career regression detected - moved to lower seniority role")

        # Ensure score doesn't go negative
        score = max(0, score)

        return score, flags, indicators

    def _detect_positive_patterns(
        self,
        timeline: List[TimelineEntry],
        avg_tenure: float,
    ) -> List[str]:
        """Detect positive career patterns."""
        positive = []

        # Long tenure bonus
        for entry in timeline:
            if entry.duration_months >= 36:  # 3+ years
                positive.append(f"Long tenure at {entry.company} ({entry.duration_months // 12}+ years)")
                break  # Only report first one

        # Stable career (good average tenure)
        if avg_tenure >= 24:
            positive.append(f"Stable average tenure of {avg_tenure:.0f} months")

        # Career progression
        if len(timeline) >= 2:
            # Check if seniority increased over time
            first_seniority = timeline[-1].seniority_level  # Oldest job
            last_seniority = timeline[0].seniority_level   # Most recent job

            if last_seniority > first_seniority:
                positive.append("Clear career progression from junior to senior levels")

        # Consistent industry (same type of role)
        role_types = set()
        for entry in timeline:
            # Extract base role type (developer, engineer, etc.)
            title_lower = entry.title.lower()
            if "develop" in title_lower or "engineer" in title_lower:
                role_types.add("engineering")
            elif "design" in title_lower:
                role_types.add("design")
            elif "product" in title_lower or "pm" in title_lower:
                role_types.add("product")
            elif "data" in title_lower or "analista" in title_lower:
                role_types.add("data")
            elif "manager" in title_lower or "lead" in title_lower:
                role_types.add("leadership")

        if len(role_types) == 1:
            positive.append("Consistent career focus in same domain")

        return positive
