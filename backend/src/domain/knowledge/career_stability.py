"""Career Stability Knowledge Base - Stability scoring, flags, and adjustments."""

from datetime import datetime
from typing import Any, Optional

# Stability flags and their score impacts
STABILITY_FLAGS: dict[str, dict[str, Any]] = {
    "job_hopper": {
        "description": "Multiple jobs with short tenure (< 1 year)",
        "threshold": 3,  # 3+ short stints
        "score_impact": -25,
        "severity": "high",
    },
    "frequent_changes": {
        "description": "Average tenure below 18 months",
        "threshold": 18,  # months
        "score_impact": -15,
        "severity": "medium",
    },
    "employment_gaps": {
        "description": "Gaps > 3 months between jobs",
        "threshold": 3,  # months
        "score_impact": -10,
        "severity": "medium",
    },
    "career_pivot": {
        "description": "Major industry/role change",
        "score_impact": -5,
        "severity": "low",
        "note": "Can be positive if well-explained",
    },
    "contractor_heavy": {
        "description": "Mostly contract/freelance work",
        "score_impact": -5,
        "severity": "low",
        "note": "Industry dependent - acceptable in tech",
    },
}

# Positive stability indicators
STABILITY_BONUSES: dict[str, dict[str, Any]] = {
    "long_tenure": {
        "description": "5+ years at single company",
        "threshold": 60,  # months
        "score_bonus": 15,
    },
    "promotions": {
        "description": "Internal promotions within company",
        "threshold": 2,  # promotions
        "score_bonus": 10,
    },
    "consistent_domain": {
        "description": "Consistent career domain/industry",
        "score_bonus": 10,
    },
    "growth_trajectory": {
        "description": "Clear upward career progression",
        "score_bonus": 10,
    },
    "leadership_retention": {
        "description": "Stayed through company growth/IPO",
        "score_bonus": 5,
    },
}

# Brazilian employment context (PJ vs CLT)
PJ_CLT_ADJUSTMENTS: dict[str, dict[str, Any]] = {
    "pj": {
        "name": "Pessoa Juridica (Contractor)",
        "typical_tenure_months": 12,  # Shorter contracts are normal
        "stability_weight": 0.7,  # Less weight on tenure
        "notes": [
            "PJ contracts typically shorter by nature",
            "Focus on project completion vs tenure",
            "Common in Brazilian tech industry",
        ],
    },
    "clt": {
        "name": "CLT (Full Employment)",
        "typical_tenure_months": 24,  # Standard expectation
        "stability_weight": 1.0,
        "notes": [
            "Full employment benefits",
            "Standard tenure expectations apply",
            "Leaving early may indicate issues",
        ],
    },
}

# Tech layoffs context 2022-2024 (for stability assessment)
TECH_LAYOFF_COMPANIES: set[str] = {
    # Major 2022-2024 layoffs - should not count against candidate
    "meta",
    "facebook",
    "amazon",
    "google",
    "alphabet",
    "microsoft",
    "twitter",
    "x corp",
    "salesforce",
    "snap",
    "snapchat",
    "shopify",
    "stripe",
    "coinbase",
    "robinhood",
    "peloton",
    "netflix",
    "intel",
    "cisco",
    "dell",
    "hp",
    "ibm",
    "oracle",
    "paypal",
    "ebay",
    "linkedin",
    "lyft",
    "uber",
    "airbnb",
    "doordash",
    "instacart",
    "spotify",
    "zoom",
    "docusign",
    "twilio",
    "datadog",
    "mongodb",
    "cloudflare",
    "snowflake",
    "palantir",
    "unity",
    "roblox",
    "dropbox",
    "box",
    "asana",
    "notion",
    "figma",
    "canva",
    "airtable",
    "hubspot",
    "zendesk",
    "atlassian",
    "github",
    # Brazilian companies with layoffs
    "nubank",
    "ifood",
    "99",
    "quinto andar",
    "quintoandar",
    "loft",
    "creditas",
    "ebanx",
    "stone",
    "pagseguro",
    "mercado livre",
    "magazineluiza",
    "americanas",
    "vtex",
    "gympass",
    "wellhub",
    "loggi",
    "madeira madeira",
}

# Layoff period (for context-aware stability scoring)
LAYOFF_PERIOD = {
    "start": datetime(2022, 1, 1),
    "peak": datetime(2023, 6, 1),
    "end": datetime(2024, 6, 30),  # Approximate end of major waves
}

# Startup tenure adjustments
STARTUP_TENURE_ADJUSTMENTS: dict[str, float] = {
    "pre_seed": 0.5,  # 50% weight - very early, high risk
    "seed": 0.6,
    "series_a": 0.7,
    "series_b": 0.8,
    "series_c": 0.9,
    "public": 1.0,  # Full weight for public companies
}

# Industry-specific tenure expectations (months)
INDUSTRY_TENURE_EXPECTATIONS: dict[str, int] = {
    "startup": 18,  # Shorter tenure expected
    "consulting": 24,  # Project-based, moderate
    "enterprise": 36,  # Longer tenure expected
    "agency": 18,  # High turnover is normal
    "fintech": 24,
    "big_tech": 30,
    "government": 48,  # Very stable expected
}


def calculate_stability_score(
    experiences: list[dict[str, Any]],
    region: str = "us",
    industry: str = "startup",
) -> dict[str, Any]:
    """
    Calculate career stability score based on work history.

    Args:
        experiences: List of work experiences with start_date, end_date, company
        region: Market region ('us' or 'br')
        industry: Industry context for tenure expectations

    Returns:
        Dict with score, flags, and analysis
    """
    if not experiences:
        return {
            "score": 50,  # Neutral score for no data
            "flags": [],
            "positive_indicators": [],
            "analysis": "No work history provided",
            "avg_tenure_months": 0,
        }

    # Calculate basic metrics
    tenures = _calculate_tenures(experiences)
    gaps = _calculate_gaps(experiences)

    # Base score starts at 100
    score = 100
    flags = []
    positive_indicators = []

    # Apply stability flags
    short_jobs = sum(1 for t in tenures if t < 12)
    if short_jobs >= STABILITY_FLAGS["job_hopper"]["threshold"]:
        score += STABILITY_FLAGS["job_hopper"]["score_impact"]
        flags.append({
            "flag": "job_hopper",
            "description": STABILITY_FLAGS["job_hopper"]["description"],
            "impact": STABILITY_FLAGS["job_hopper"]["score_impact"],
        })

    avg_tenure = sum(tenures) / len(tenures) if tenures else 0
    if avg_tenure < STABILITY_FLAGS["frequent_changes"]["threshold"]:
        score += STABILITY_FLAGS["frequent_changes"]["score_impact"]
        flags.append({
            "flag": "frequent_changes",
            "description": f"Average tenure: {avg_tenure:.0f} months",
            "impact": STABILITY_FLAGS["frequent_changes"]["score_impact"],
        })

    # Check for gaps
    long_gaps = sum(1 for g in gaps if g > STABILITY_FLAGS["employment_gaps"]["threshold"])
    if long_gaps > 0:
        impact = STABILITY_FLAGS["employment_gaps"]["score_impact"] * long_gaps
        score += impact
        flags.append({
            "flag": "employment_gaps",
            "description": f"{long_gaps} gap(s) > 3 months",
            "impact": impact,
        })

    # Apply positive bonuses
    if max(tenures, default=0) >= STABILITY_BONUSES["long_tenure"]["threshold"]:
        score += STABILITY_BONUSES["long_tenure"]["score_bonus"]
        positive_indicators.append({
            "indicator": "long_tenure",
            "description": "5+ years at single company",
            "bonus": STABILITY_BONUSES["long_tenure"]["score_bonus"],
        })

    # Check for layoff context
    layoff_affected = _check_layoff_context(experiences)
    if layoff_affected:
        # Reduce negative impact for layoff-affected candidates
        for flag in flags:
            flag["impact"] = int(flag["impact"] * 0.5)  # Halve the penalty
        positive_indicators.append({
            "indicator": "layoff_context",
            "description": "Job change during tech layoff period",
            "note": "Stability penalties reduced",
        })

    # Adjust for region (Brazil PJ context)
    if region == "br":
        pj_count = sum(1 for e in experiences if _is_pj_contract(e))
        if pj_count > len(experiences) * 0.5:
            # Mostly PJ - reduce tenure expectations
            adjustment = PJ_CLT_ADJUSTMENTS["pj"]["stability_weight"]
            for flag in flags:
                flag["impact"] = int(flag["impact"] * adjustment)
            positive_indicators.append({
                "indicator": "pj_context",
                "description": "PJ (contractor) work history - adjusted expectations",
            })

    # Industry adjustment
    expected_tenure = INDUSTRY_TENURE_EXPECTATIONS.get(industry, 24)
    if avg_tenure >= expected_tenure:
        score += 5
        positive_indicators.append({
            "indicator": "meets_industry_standards",
            "description": f"Tenure meets {industry} expectations",
        })

    # Recalculate score with adjusted flags
    score = 100 + sum(f["impact"] for f in flags) + sum(p.get("bonus", 0) for p in positive_indicators)

    # Clamp score to 0-100
    score = max(0, min(100, score))

    return {
        "score": score,
        "flags": flags,
        "positive_indicators": positive_indicators,
        "avg_tenure_months": round(avg_tenure, 1),
        "total_companies": len(experiences),
        "short_stints": short_jobs,
        "gaps": gaps,
        "analysis": _generate_stability_analysis(score, flags, positive_indicators),
    }


def _calculate_tenures(experiences: list[dict]) -> list[float]:
    """Calculate tenure in months for each experience."""
    tenures = []
    for exp in experiences:
        start = exp.get("start_date")
        end = exp.get("end_date") or datetime.now().strftime("%Y-%m")

        if start:
            try:
                start_date = _parse_date(start)
                end_date = _parse_date(end)
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                tenures.append(max(1, months))  # Minimum 1 month
            except (ValueError, AttributeError):
                tenures.append(12)  # Default assumption
        else:
            tenures.append(12)  # Default assumption

    return tenures


def _calculate_gaps(experiences: list[dict]) -> list[float]:
    """Calculate gaps between jobs in months."""
    if len(experiences) < 2:
        return []

    # Sort by start date
    sorted_exp = sorted(
        experiences,
        key=lambda x: _parse_date(x.get("start_date", "2000-01")),
    )

    gaps = []
    for i in range(1, len(sorted_exp)):
        prev_end = sorted_exp[i - 1].get("end_date")
        curr_start = sorted_exp[i].get("start_date")

        if prev_end and curr_start:
            try:
                end_date = _parse_date(prev_end)
                start_date = _parse_date(curr_start)
                gap_months = (start_date.year - end_date.year) * 12 + (start_date.month - end_date.month)
                if gap_months > 0:
                    gaps.append(gap_months)
            except (ValueError, AttributeError):
                pass

    return gaps


def _parse_date(date_str: str) -> datetime:
    """Parse date string to datetime."""
    if isinstance(date_str, datetime):
        return date_str

    # Try common formats
    for fmt in ["%Y-%m", "%Y-%m-%d", "%m/%Y", "%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Default to January of the year if only year provided
    if len(date_str) == 4 and date_str.isdigit():
        return datetime(int(date_str), 1, 1)

    raise ValueError(f"Cannot parse date: {date_str}")


def _check_layoff_context(experiences: list[dict]) -> bool:
    """Check if candidate was affected by tech layoffs."""
    for exp in experiences:
        company = (exp.get("company") or "").lower()
        end_date_str = exp.get("end_date")

        if not end_date_str:
            continue

        try:
            end_date = _parse_date(end_date_str)
        except ValueError:
            continue

        # Check if company had layoffs and job ended during layoff period
        company_had_layoffs = any(
            layoff_co in company for layoff_co in TECH_LAYOFF_COMPANIES
        )
        during_layoff_period = LAYOFF_PERIOD["start"] <= end_date <= LAYOFF_PERIOD["end"]

        if company_had_layoffs and during_layoff_period:
            return True

    return False


def _is_pj_contract(experience: dict) -> bool:
    """Check if experience appears to be PJ (contractor) work."""
    title = (experience.get("title") or "").lower()
    company = (experience.get("company") or "").lower()

    pj_indicators = [
        "contractor",
        "freelance",
        "consultant",
        "pj",
        "autonomo",
        "autônomo",
        "mei",
        "consultoria",
    ]

    return any(ind in title or ind in company for ind in pj_indicators)


def _generate_stability_analysis(
    score: int,
    flags: list[dict],
    positive_indicators: list[dict],
) -> str:
    """Generate human-readable stability analysis."""
    if score >= 90:
        base = "Excellent career stability."
    elif score >= 75:
        base = "Good career stability with minor concerns."
    elif score >= 60:
        base = "Moderate stability - some red flags present."
    elif score >= 40:
        base = "Below average stability - multiple concerns."
    else:
        base = "Significant stability concerns identified."

    details = []
    if flags:
        details.append(f"Concerns: {', '.join(f['flag'] for f in flags)}")
    if positive_indicators:
        details.append(f"Strengths: {', '.join(p['indicator'] for p in positive_indicators)}")

    return f"{base} {' | '.join(details)}" if details else base


def is_layoff_affected_company(company_name: str) -> bool:
    """Check if a company is known to have had layoffs 2022-2024."""
    return company_name.lower() in TECH_LAYOFF_COMPANIES


def get_tenure_expectation(industry: str) -> int:
    """Get expected tenure in months for an industry."""
    return INDUSTRY_TENURE_EXPECTATIONS.get(industry, 24)
