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
    # Brazilian employment context
    contract_type: str = "unknown"  # pj, clt, freelancer, unknown
    # Startup context
    startup_stage: str = "unknown"  # early_stage, series_a, series_b, late_stage, unknown
    # Layoff context
    is_layoff_period: bool = False  # True if ended during 2022-2024 at known layoff company


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

# =========================================
# BRAZILIAN EMPLOYMENT CONTEXT (PJ vs CLT)
# =========================================

CONTRACT_TYPE_KEYWORDS = {
    "pj": [
        "pj", "pessoa jurídica", "pessoa juridica", "contractor", "consultor",
        "prestador", "prestador de serviço", "prestador de servico",
    ],
    "clt": [
        "clt", "efetivo", "empregado", "funcionário", "funcionario",
        "carteira assinada",
    ],
    "freelancer": [
        "freelance", "freelancer", "autônomo", "autonomo", "independente",
    ],
}

# =========================================
# TECH LAYOFFS 2022-2024 CONTEXT
# =========================================

LAYOFF_COMPANIES_2022_2024 = {
    # FAANG/MAANG
    "google", "alphabet", "meta", "facebook", "amazon", "microsoft", "apple",
    # Major Tech
    "twitter", "x corp", "salesforce", "ibm", "intel", "cisco", "dell",
    "spotify", "stripe", "coinbase", "robinhood", "netflix", "snap",
    "uber", "lyft", "airbnb", "doordash", "instacart", "zillow",
    "twilio", "shopify", "atlassian", "dropbox", "zoom", "docusign",
    "paypal", "square", "block", "affirm", "plaid", "brex",
    # Brazilian Tech
    "nubank", "ifood", "creditas", "loft", "quinto andar", "quintoandar",
    "loggi", "ebanx", "stone", "pagseguro", "vtex", "totvs",
}

LAYOFF_KEYWORDS = [
    "layoff", "laid off", "downsized", "restructured", "demitido em massa",
    "company shutdown", "startup closed", "acquisition", "acquired",
    "position eliminated", "role eliminated", "team dissolved", "rif",
    "reduction in force", "desligamento em massa", "reestruturação",
]

# =========================================
# STARTUP STAGE INDICATORS
# =========================================

STARTUP_INDICATORS = {
    "early_stage": [
        "startup", "seed", "pre-seed", "angel", "early stage", "early-stage",
        "fundador", "founder", "co-founder", "cofundador",
    ],
    "series_a": ["series a", "série a", "serie a"],
    "series_b": ["series b", "série b", "serie b"],
    "late_stage": [
        "series c", "series d", "series e", "series f",
        "série c", "série d", "série e",
        "post-ipo", "ipo", "unicorn", "unicórnio",
    ],
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

            # Detect Brazilian employment context
            contract_type = self._detect_contract_type(exp.title, exp.company)

            # Detect startup stage
            startup_stage = self._detect_startup_stage(exp.company, exp.title)

            # Detect layoff context
            is_layoff = self._detect_layoff_context(exp.company, end_year)

            timeline.append(TimelineEntry(
                company=exp.company,
                title=exp.title,
                start_year=start_year or self.current_year,
                end_year=end_year,
                duration_months=exp.duration_months,
                seniority_level=seniority,
                contract_type=contract_type,
                startup_stage=startup_stage,
                is_layoff_period=is_layoff,
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

    def _detect_contract_type(self, title: str, company: str) -> str:
        """Detect if role was PJ, CLT, or Freelancer (Brazilian employment context)."""
        text = f"{title} {company}".lower()

        for contract_type, keywords in CONTRACT_TYPE_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return contract_type

        return "unknown"

    def _detect_startup_stage(self, company: str, title: str = "") -> str:
        """Detect startup stage from company/title info."""
        text = f"{company} {title}".lower()

        # Check stages in order (more specific first)
        for stage in ["late_stage", "series_b", "series_a", "early_stage"]:
            if any(indicator in text for indicator in STARTUP_INDICATORS[stage]):
                return stage

        return "unknown"

    def _detect_layoff_context(self, company: str, end_year: Optional[int]) -> bool:
        """Detect if short tenure might be due to 2022-2024 layoffs."""
        # Check if end year is in layoff period
        if end_year and 2022 <= end_year <= 2024:
            company_lower = company.lower()
            # Check if company is in known layoff list
            if any(lc in company_lower for lc in LAYOFF_COMPANIES_2022_2024):
                return True
        return False

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

    def _get_penalty_reduction_factor(self, entry: TimelineEntry) -> float:
        """
        Calculate penalty reduction factor based on context.

        Returns a multiplier (0.0 to 1.0) to apply to penalties.
        - PJ/Freelancer: 50% reduction (factor = 0.5)
        - Layoff period: 100% reduction (factor = 0.0)
        - Early-stage startup: 70% reduction (factor = 0.3)
        - Series A startup: 50% reduction (factor = 0.5)
        - Series B startup: 25% reduction (factor = 0.75)
        """
        # Layoff period takes precedence - no penalty
        if entry.is_layoff_period:
            return 0.0

        # PJ/Freelancer - reduced expectations
        if entry.contract_type in ["pj", "freelancer"]:
            return 0.5

        # Startup stage adjustments
        startup_factors = {
            "early_stage": 0.3,   # 70% reduction
            "series_a": 0.5,      # 50% reduction
            "series_b": 0.75,     # 25% reduction
            "late_stage": 1.0,    # No reduction
        }
        if entry.startup_stage in startup_factors:
            return startup_factors[entry.startup_stage]

        return 1.0  # Full penalty (no reduction)

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

        # Calculate context-adjusted metrics
        # Count short tenures with context adjustments
        adjusted_short_jobs = 0
        context_adjusted_entries = []

        for entry in timeline:
            factor = self._get_penalty_reduction_factor(entry)
            if entry.duration_months < 12:
                # Apply penalty reduction based on context
                if factor < 1.0:
                    context = []
                    if entry.is_layoff_period:
                        context.append("layoff period")
                    if entry.contract_type in ["pj", "freelancer"]:
                        context.append(f"{entry.contract_type.upper()} contract")
                    if entry.startup_stage != "unknown":
                        context.append(f"{entry.startup_stage.replace('_', ' ')} startup")

                    context_adjusted_entries.append({
                        "company": entry.company,
                        "factor": factor,
                        "context": context,
                    })

                # Only count as short if factor > 0
                if factor > 0:
                    adjusted_short_jobs += factor

        # Short average tenure - with context adjustment
        tenure_penalty = 0
        if avg_tenure < 12:
            base_penalty = 20
            # Check if most short jobs have mitigating context
            if context_adjusted_entries:
                avg_factor = sum(e["factor"] for e in context_adjusted_entries) / len(context_adjusted_entries)
                tenure_penalty = int(base_penalty * avg_factor)
            else:
                tenure_penalty = base_penalty

            if tenure_penalty > 0:
                score -= tenure_penalty
                flags.append(StabilityFlag.SHORT_TENURE)
                indicators.append(f"Very short average tenure of {avg_tenure:.0f} months (below 12 months)")
            else:
                indicators.append(f"Short tenure of {avg_tenure:.0f} months - mitigated by context (PJ/layoffs/startups)")

        elif avg_tenure < 18:
            score -= 10
            indicators.append(f"Below average tenure of {avg_tenure:.0f} months (ideal is 24+ months)")

        # Job hopping - too many companies in 5 years
        # Adjust threshold for Brazilian market (PJ culture)
        has_pj_culture = any(e.contract_type in ["pj", "freelancer"] for e in timeline)
        job_hopping_threshold = 5 if has_pj_culture else 4
        high_threshold = 4 if has_pj_culture else 3

        if companies_5y > job_hopping_threshold:
            score -= 15
            flags.append(StabilityFlag.JOB_HOPPER)
            indicators.append(f"{companies_5y} companies in the last 5 years (indicates job hopping)")
        elif companies_5y > high_threshold:
            score -= 5
            indicators.append(f"{companies_5y} companies in the last 5 years (slightly high)")

        # Employment gaps
        for gap in gaps:
            # Don't penalize COVID-era gaps (2020-2021)
            if 2020 <= gap.start_year <= 2021:
                indicators.append(
                    f"Employment gap of {gap.months} months between "
                    f"{gap.after_company} and {gap.before_company} ({gap.start_year}-{gap.end_year}) - COVID period, no penalty"
                )
            else:
                score -= 10
                flags.append(StabilityFlag.EMPLOYMENT_GAP)
                indicators.append(
                    f"Employment gap of {gap.months} months between "
                    f"{gap.after_company} and {gap.before_company} ({gap.start_year}-{gap.end_year})"
                )

        # Consecutive short jobs - with context adjustment
        if consecutive_short >= 2:
            # Check if consecutive short jobs are all in mitigating context
            consecutive_with_context = sum(
                1 for e in timeline[:consecutive_short]
                if e.is_layoff_period or e.contract_type in ["pj", "freelancer"]
                or e.startup_stage in ["early_stage", "series_a"]
            )

            if consecutive_with_context >= consecutive_short:
                indicators.append(
                    f"{consecutive_short} consecutive short jobs - mitigated by context (PJ/layoffs/startups)"
                )
            else:
                score -= 15
                flags.append(StabilityFlag.CONSECUTIVE_SHORT_JOBS)
                indicators.append(f"{consecutive_short} consecutive jobs with tenure under 12 months")

        # Seniority regression
        if has_regression:
            score -= 20
            flags.append(StabilityFlag.SENIORITY_REGRESSION)
            indicators.append("Career regression detected - moved to lower seniority role")

        # Add positive notes for context awareness
        for entry_info in context_adjusted_entries:
            if entry_info["context"]:
                context_str = ", ".join(entry_info["context"])
                indicators.append(
                    f"Note: Short tenure at {entry_info['company']} considered in context ({context_str})"
                )

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
