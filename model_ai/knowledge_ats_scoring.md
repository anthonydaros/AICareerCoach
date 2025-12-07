# ATS Scoring Knowledge Base

## Scoring Weights (100 points total)

| Component | Weight | Description |
|-----------|--------|-------------|
| Skills Match | 40% | Technical skills alignment with job requirements |
| Experience | 30% | Years of relevant experience |
| Education | 15% | Degree relevance and level |
| Certifications | 10% | Industry certifications |
| Keywords | 5% | ATS keyword density |

## Detailed Scoring Breakdown

### 1. Contact Information (15 points)
- Email present: 5 pts
- Phone number present: 5 pts
- LinkedIn profile: 5 pts

**Regex Patterns:**
- Email: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}`
- Phone: `\d{3}[-.\s]?\d{3}[-.\s]?\d{4}`
- LinkedIn: `linkedin\.com`

### 2. Section Structure (15 points)
Required sections (3 pts each):
- Experience/Work History
- Education
- Skills
- Summary/Profile
- Projects (optional but valuable)

### 3. Technical Keywords (25 points)
Points = min(keywords_found * 2, 25)

**Keywords Database by Category:**

#### Languages
Python, Java, JavaScript, TypeScript, Go, Rust, C++, Ruby, PHP, Swift, Kotlin, SQL

#### Frameworks
React, Angular, Vue.js, Node.js, Django, Flask, Spring Boot, FastAPI, .NET, Rails, Next.js

#### Cloud & Infrastructure
AWS, Azure, GCP, Docker, Kubernetes, Terraform, Jenkins, CI/CD, GitHub Actions, Ansible

#### Data
PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, Kafka, Spark, Airflow, Snowflake

#### AI/ML
TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, LLM, RAG, LangChain, OpenAI

#### Methodologies
Agile, Scrum, Kanban, TDD, Microservices, REST API, GraphQL, Event-Driven

### 4. Action Verbs (15 points)
Points = min(verbs_found * 2, 15)

**Strong Action Verbs:**
- Leadership: led, managed, directed, coordinated, supervised, mentored
- Achievement: achieved, delivered, exceeded, increased, reduced, improved
- Technical: developed, implemented, designed, built, created, architected
- Innovation: pioneered, launched, automated, optimized, migrated, scaled
- Collaboration: collaborated, partnered, facilitated, supported, trained

### 5. Quantified Results (15 points)
Points = min(metrics_found * 3, 15)

**Patterns to Detect:**
- Percentages: `\d+%`
- Currency: `\$\d+`
- Multipliers: `\d+x`
- Growth indicators: `\d+\+`

**Examples of Good Metrics:**
- "Reduced deployment time by 40%"
- "Managed $2M budget"
- "Increased performance 3x"
- "Supported 100+ engineers"

### 6. Length Check (15 points)
| Word Count | Score |
|------------|-------|
| 300-800 | 15 pts (optimal) |
| 200-300 or 800-1000 | 10 pts |
| <200 or >1000 | 5 pts |

## Score Interpretation

| Score Range | Rating | Recommendation |
|-------------|--------|----------------|
| 80-100 | Excellent | High ATS pass-through likelihood |
| 60-79 | Good | Some optimizations recommended |
| 40-59 | Fair | Significant improvements needed |
| 0-39 | Poor | Major rework required |

## Common ATS Issues to Flag

### Format Issues (Critical)
- Tables or columns (ATS parsing failure)
- Headers/footers with important info
- Images or graphics
- Non-standard fonts
- Text boxes
- Unusual file formats (.pages, .odt)

### Content Issues (High Priority)
- Missing contact information
- No dates on experience
- Vague job titles
- Missing keywords
- No quantified achievements

### Structure Issues (Medium Priority)
- Non-chronological order
- Missing section headers
- Inconsistent date formats
- Gaps not explained

## Improvement Suggestions Logic

### If Skills Score < 40%:
```
Add these high-value keywords to your skills section:
[List missing keywords from job description]
```

### If Experience Score < 30%:
```
Strengthen your experience section:
- Add quantified achievements (numbers, percentages)
- Use strong action verbs
- Align job titles with industry standards
```

### If Education Score < 15%:
```
Enhance your education section:
- Add relevant coursework
- Include certifications
- List academic projects
```

### If Format Issues Detected:
```
Critical format fixes needed:
- Remove tables/columns
- Use standard section headers
- Save as .pdf or .docx
- Use single-column layout
```
