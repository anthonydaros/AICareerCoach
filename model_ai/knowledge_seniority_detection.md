# Seniority Detection Knowledge Base

## Seniority Level Thresholds

| Level | Years | Title Patterns | Key Indicators |
|-------|-------|---------------|----------------|
| Junior | 0-2 | Junior, Associate, Entry-level | Learning, supporting, assisting |
| Mid | 2-5 | Developer, Engineer, Analyst | Building, implementing, contributing |
| Senior | 5-8 | Senior, Lead, Principal | Leading, architecting, mentoring |
| Staff+ | 8+ | Staff, Principal, Architect, Director | Strategic, organizational impact |

## Detection Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| Experience Years | 15% | Total relevant work experience |
| Task Complexity | 20% | Complexity of work described |
| Autonomy Level | 20% | Independence in decision-making |
| Technical Skills | 20% | Depth and breadth of skills |
| Leadership Signals | 15% | Team leadership, mentoring |
| Impact Scope | 10% | Individual vs. organizational impact |

## Action Verb Patterns

### Senior-Level Verbs (High Impact)
**English:**
led, architected, designed, drove, established, defined, directed, mentored, pioneered, spearheaded, transformed, scaled, owned, strategized

**Portuguese (PT-BR):**
liderou, arquitetou, projetou, conduziu, estabeleceu, definiu, dirigiu, mentorou, criou, orquestrou, transformou, escalou

### Mid-Level Verbs (Moderate Impact)
**English:**
developed, implemented, built, created, managed, optimized, improved, coordinated, collaborated, maintained, integrated

**Portuguese (PT-BR):**
desenvolveu, implementou, construiu, criou, gerenciou, otimizou, melhorou, coordenou, colaborou, manteve

### Junior-Level Verbs (Learning/Supporting)
**English:**
assisted, supported, helped, learned, participated, contributed, worked on, shadowed, researched

**Portuguese (PT-BR):**
auxiliou, apoiou, ajudou, aprendeu, participou, contribuiu, trabalhou em, pesquisou

## Skill Indicators by Level

### Senior/Lead Skills
- System design, Architecture patterns
- Microservices, Distributed systems
- Performance optimization at scale
- Security architecture
- Technical leadership
- Cross-functional collaboration
- Strategic planning

### Mid-Level Skills
- Full-stack development
- API design and implementation
- Database optimization
- CI/CD pipelines
- Code review practices
- Testing strategies
- Agile methodologies

### Junior-Level Skills
- Programming fundamentals
- Version control (Git)
- Basic debugging
- Unit testing
- Documentation
- Learning frameworks
- Following best practices

## Title Pattern Recognition

### Seniority Progression Indicators

| Indicator | Points | Examples |
|-----------|--------|----------|
| "Senior" in title | +3 | Senior Developer, Senior Engineer |
| "Lead" in title | +4 | Tech Lead, Team Lead |
| "Principal" in title | +5 | Principal Engineer |
| "Staff" in title | +5 | Staff Engineer |
| "Architect" in title | +5 | Solutions Architect |
| "Director" in title | +6 | Engineering Director |
| "VP" in title | +7 | VP of Engineering |
| "Junior" in title | -2 | Junior Developer |
| "Associate" in title | -1 | Associate Engineer |
| "Intern" in title | -3 | Software Intern |

## Impact Scope Classification

### Individual Contributor Scope
- "Completed assigned tasks"
- "Fixed bugs in the codebase"
- "Wrote unit tests"
- Impact: Own work only

### Team-Level Scope
- "Collaborated with team of 5"
- "Mentored 2 junior developers"
- "Led sprint planning"
- Impact: Direct team

### Organization-Level Scope
- "Designed architecture used by 10 teams"
- "Reduced company-wide costs by 30%"
- "Established engineering standards"
- Impact: Multiple teams/departments

### Company-Level Scope
- "Defined technical strategy"
- "Reported to C-suite"
- "Influenced product roadmap"
- Impact: Entire organization

## Quantified Experience Patterns

### Years of Experience Extraction
Look for patterns:
- "X years of experience"
- "X+ years in"
- Date ranges (2018-2023 = 5 years)
- "Since 2015" (calculate from current date)

### Team Size Indicators
- "Team of X" → Leadership indicator
- "Managed X engineers" → Direct reports
- "Collaborated with X team members" → Team context

## Confidence Scoring

| Confidence | Criteria |
|------------|----------|
| High (>80%) | Multiple strong indicators align (verbs + skills + years + title) |
| Medium (50-80%) | Some indicators present but mixed signals |
| Low (<50%) | Few indicators, conflicting signals, unclear experience |

## Special Cases

### Career Changers
- May have senior years but junior-level tech skills
- Look at tech-specific experience, not total years
- Weight skills and projects higher than years

### Consultants/Contractors
- Often have varied experience levels
- Look at project scope and complexity
- Consider client caliber and project size

### Startup Experience
- Titles may be inflated
- Look at actual responsibilities
- Consider company stage and team size
