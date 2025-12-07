# Career Stability Analysis Knowledge Base

## Stability Flags

| Flag | Severity | Condition | Score Deduction |
|------|----------|-----------|-----------------|
| Job Hopper | High | 3+ jobs in 3 years with avg tenure < 18 months | -25 points |
| Short Tenure | Medium | Any role < 12 months (except current) | -10 points each |
| Employment Gap | Medium | Gap > 6 months unexplained | -15 points |
| Seniority Regression | High | Moved to lower-level role | -20 points |

## Stability Score Calculation

**Base Score: 100 points**

### Deductions

```
For each job in last 5 years:
  - If tenure < 6 months: -15 points
  - If tenure 6-12 months: -10 points
  - If tenure 12-18 months: -5 points

For employment gaps:
  - Gap 3-6 months: -5 points
  - Gap 6-12 months: -10 points
  - Gap > 12 months: -15 points

For career trajectory:
  - Lateral moves (same level): 0 points
  - Promotions: +5 points each
  - Demotions: -20 points each
```

## Title Seniority Mapping (Levels 1-8)

| Level | Titles | Typical Years |
|-------|--------|---------------|
| 1 | Intern, Trainee | 0 |
| 2 | Junior, Associate, Entry-level | 0-2 |
| 3 | Developer, Engineer, Analyst | 2-4 |
| 4 | Senior Developer, Senior Engineer | 4-7 |
| 5 | Lead, Tech Lead, Team Lead | 6-10 |
| 6 | Staff, Principal, Architect | 8-12 |
| 7 | Director, Head of, Manager | 10-15 |
| 8 | VP, C-level, Executive | 12+ |

## Positive Stability Indicators

### Long Tenure (+5 each)
- Same company 3+ years
- Promoted within same company
- Consistent industry focus

### Career Growth (+3 each)
- Title progression visible
- Increasing scope of work
- Growing team responsibilities

### Commitment Signals (+2 each)
- Side projects showing passion
- Continuous learning (certifications)
- Conference speaking/writing

## Red Flag Patterns

### Job Hopping Profile
```
Pattern: 3+ roles in 36 months, average tenure < 18 months

Warning Signs:
- Frequent lateral moves (same level, different companies)
- No clear reason for transitions
- Vague departure explanations

Questions to Probe:
- "I see you've had several transitions. What drove those changes?"
- "What are you looking for in your next long-term role?"
```

### Short Tenure Pattern
```
Pattern: Multiple roles < 12 months

Warning Signs:
- Pattern of leaving during probation
- No promotions despite years of experience
- Declining company caliber

Mitigating Factors:
- Contract roles (expected short duration)
- Startup failures (company-side issue)
- Relocations (life circumstances)
```

### Employment Gap Analysis
```
Gap Duration | Risk Level | Common Explanations
< 3 months   | Low        | Job searching, transition
3-6 months   | Medium     | Extended search, personal time
6-12 months  | High       | Career change, health, family
> 12 months  | Very High  | Requires strong explanation
```

### Seniority Regression
```
Pattern: Senior → Mid or Lead → Individual Contributor

Concerning When:
- No explanation provided
- Multiple regressions in history
- Pattern of stepping back

Acceptable When:
- Startup to enterprise transition (title adjustment)
- Career pivot to new field
- Work-life balance choice (explicit)
- Company restructuring/layoffs
```

## Stability Score Interpretation

| Score | Rating | Assessment |
|-------|--------|------------|
| 90-100 | Excellent | Very stable, low flight risk |
| 75-89 | Good | Generally stable with minor flags |
| 60-74 | Fair | Some concerns, needs discussion |
| 40-59 | Concerning | Significant stability issues |
| 0-39 | High Risk | Major red flags present |

## Context Considerations

### Industry Norms
| Industry | Typical Tenure | Notes |
|----------|---------------|-------|
| Startups | 1-2 years | Shorter is normal |
| Enterprise | 3-5 years | Longer expected |
| Consulting | 2-3 years | Project-based |
| Finance | 3-4 years | Moderate |
| Government | 5+ years | Very stable |

### Career Stage
| Stage | Acceptable Tenure |
|-------|------------------|
| Early Career (0-5 yrs) | 1-2 years acceptable |
| Mid Career (5-10 yrs) | 2-3 years expected |
| Senior (10+ yrs) | 3-5 years expected |

### Geographic Factors
- Silicon Valley: Shorter tenures common
- Traditional markets: Longer tenures expected
- Remote roles: Variable expectations

## Brazilian Employment Context

### PJ (Pessoa Jurídica) vs CLT

In Brazil, many tech professionals work as PJ (contractors) rather than CLT (traditional employment). This affects stability analysis significantly.

| Contract Type | Typical Tenure | Notes | Scoring Adjustment |
|---------------|---------------|-------|-------------------|
| CLT | 2-4 years | Traditional employment, longer expected | Standard scoring |
| PJ | 6-18 months | Project-based, shorter is normal | Reduce penalties by 50% |
| Contractor | 3-12 months | Expected to be short-term | Reduce penalties by 70% |
| Freelancer | Variable | Project-to-project | Consider project count instead |

**Detection Keywords:**
- "PJ", "Pessoa Jurídica", "Contractor", "Consultor", "Prestador de Serviço"
- "Freelance", "Freelancer", "Autônomo"
- "Contrato", "Projeto", "Alocação"

**Important Adjustments:**
- PJ contracts should NOT be penalized for short tenure (6-12 months)
- Many senior professionals in Brazil choose PJ for tax benefits
- Look for "PJ" keyword in job title or company description
- If tenure < 6 months as PJ: -5 points (not -15)
- If tenure 6-12 months as PJ: 0 points (not -10)

### Brazilian Market Specifics

| Factor | US Standard | Brazil Adjustment |
|--------|-------------|-------------------|
| Average tenure | 2-3 years | 1.5-2.5 years |
| Job hopping threshold | 3 jobs in 3 years | 4 jobs in 3 years |
| Short tenure flag | < 12 months | < 6 months (PJ) / < 9 months (CLT) |
| Employment gap | > 6 months | > 4 months (economy-dependent) |

## Tech Industry Layoffs (2022-2024)

### Context
Mass layoffs affected the tech industry globally between 2022-2024. This should be considered when analyzing career stability.

**Affected Companies (Partial List):**
- FAANG/MAANG: Google, Meta, Amazon, Microsoft, Apple (10-20% workforce reductions)
- Major Tech: Twitter/X, Salesforce, IBM, Intel, Cisco, Dell
- Startups: Thousands of startups reduced workforce or shut down
- Brazilian Tech: Many international operations reduced, local startups affected

### Detection Patterns
- Short tenure (< 12 months) ending in 2022, 2023, or early 2024
- Company name matches known layoff list
- Multiple roles ending in similar timeframe
- Explicit mention of "layoff", "restructuring", "downsizing", "RIF"

### Scoring Adjustments

```
If role ended 2022-2024:
  - At known layoff company: reduce penalty by 50%
  - With explicit layoff mention: no penalty
  - With "restructuring" mention: reduce penalty by 30%
  - During startup shutdown: no penalty
```

**Keywords to Detect:**
- "layoff", "laid off", "downsized", "restructured"
- "company shutdown", "startup closed", "acquisition"
- "position eliminated", "role eliminated", "team dissolved"
- "RIF" (Reduction in Force)

## Startup-Specific Adjustments

### Tenure Expectations by Stage

| Startup Stage | Expected Tenure | Risk Level | Scoring Adjustment |
|---------------|-----------------|------------|-------------------|
| Pre-seed/Seed | 6-12 months | High failure rate | Reduce penalty by 70% |
| Series A | 1-2 years | Still volatile | Reduce penalty by 50% |
| Series B | 2-3 years | More stable | Reduce penalty by 25% |
| Series C+ | 2-3 years | Stable | Standard scoring |
| Post-IPO | 3+ years | Similar to enterprise | Standard scoring |

### Detection Methods
- Company founding year (recent = early stage)
- Team size mentions (< 50 employees = likely early stage)
- Funding stage mentions in job description
- Company still exists check (if closed = startup failure)

### Startup Failure Signals
```
Pattern: Short tenure + company no longer exists

Mitigating Factors:
- Startup shutdowns are common (90% failure rate)
- Not a reflection of individual performance
- Shows risk tolerance and entrepreneurial spirit

Scoring: No penalty if startup demonstrably failed
```

## Remote Work Considerations (Post-2020)

### Impact on Stability Analysis

| Scenario | Traditional View | Modern Adjustment |
|----------|-----------------|-------------------|
| Multiple short remote gigs | Red flag | Acceptable if project-based |
| Gap during COVID (2020-2021) | Flag | No penalty |
| Company went remote-first | Potential concern | Not a concern |
| Relocation-based change | Flag | Common, reduce penalty |

### Detection
- "Remote", "Distributed", "WFH" in job description
- Location changes without job changes
- "Contractor" or "Freelance" for remote positions

## Analysis Output Format

```markdown
## Career Stability Analysis

### Stability Score: XX/100

### Flags Identified:
1. [Flag Type]: [Description] (-X points)
2. [Flag Type]: [Description] (-X points)

### Positive Indicators:
1. [Indicator]: [Description] (+X points)

### Tenure Summary:
- Average tenure: X.X years
- Longest tenure: X years at [Company]
- Shortest tenure: X months at [Company]

### Risk Assessment:
[Low/Medium/High] - [Explanation]

### Recommendations:
- [How to address concerns in interview]
- [Positioning strategies]
```
