"""Skill Relationships - Maps skills to inferred related skills.

This module provides intelligent skill inference. When a resume lists "Python",
we can infer familiarity with common Python libraries. This improves matching
accuracy since most resumes don't list every individual library.
"""

from typing import Dict, List, Optional, Set

# Skills that imply knowledge of related technologies
SKILL_RELATIONSHIPS: Dict[str, List[str]] = {
    # Programming Languages -> Frameworks/Libraries
    "python": [
        "pytorch", "tensorflow", "numpy", "pandas", "scikit-learn",
        "fastapi", "django", "flask", "keras", "opencv", "matplotlib",
        "seaborn", "sqlalchemy", "pydantic", "celery", "asyncio",
    ],
    "javascript": [
        "react", "node.js", "typescript", "vue.js", "angular",
        "express", "next.js", "npm", "webpack", "babel", "jest",
        "redux", "graphql", "jquery", "html", "css",
    ],
    "typescript": [
        "javascript", "react", "node.js", "angular", "next.js",
        "express", "npm", "webpack", "jest", "redux",
    ],
    "java": [
        "spring", "spring boot", "maven", "gradle", "hibernate",
        "junit", "jpa", "tomcat", "kafka", "jdbc",
    ],
    "go": [
        "golang", "gin", "gorilla", "grpc", "protobuf",
    ],
    "rust": [
        "cargo", "tokio", "actix", "serde",
    ],
    "c#": [
        ".net", "asp.net", "entity framework", "unity", "linq",
    ],
    "ruby": [
        "rails", "ruby on rails", "rspec", "sidekiq",
    ],
    "php": [
        "laravel", "symfony", "composer", "wordpress",
    ],

    # Cloud Platforms -> Services
    "aws": [
        "ec2", "s3", "lambda", "rds", "cloudformation", "eks",
        "ecs", "dynamodb", "sqs", "sns", "cloudwatch", "iam",
        "api gateway", "route53", "cloudfront",
    ],
    "gcp": [
        "google cloud", "cloud functions", "bigquery", "cloud run",
        "gke", "cloud storage", "pub/sub", "cloud sql", "vertex ai",
    ],
    "azure": [
        "azure functions", "cosmos db", "aks", "azure devops",
        "azure storage", "azure sql", "app service",
    ],

    # AI/ML implies related tools
    "machine learning": [
        "pytorch", "tensorflow", "scikit-learn", "keras", "numpy",
        "pandas", "data science", "neural networks", "deep learning",
    ],
    "deep learning": [
        "pytorch", "tensorflow", "keras", "neural networks",
        "cnn", "rnn", "transformer", "gpu",
    ],
    "ai": [
        "llm", "langchain", "openai", "machine learning", "nlp",
        "chatgpt", "gpt", "artificial intelligence",
    ],
    "llm": [
        "langchain", "openai", "prompt engineering", "rag",
        "chatgpt", "gpt", "embeddings", "vector database",
    ],
    "nlp": [
        "natural language processing", "spacy", "nltk", "transformers",
        "bert", "gpt", "text mining", "sentiment analysis",
    ],
    "data science": [
        "python", "pandas", "numpy", "machine learning", "statistics",
        "data analysis", "jupyter", "visualization",
    ],

    # DevOps/Infrastructure
    "docker": [
        "kubernetes", "containerization", "docker-compose", "dockerfile",
        "container", "devops",
    ],
    "kubernetes": [
        "k8s", "helm", "docker", "container orchestration",
        "pods", "kubectl", "devops",
    ],
    "devops": [
        "ci/cd", "docker", "kubernetes", "jenkins", "github actions",
        "terraform", "ansible", "monitoring",
    ],
    "terraform": [
        "infrastructure as code", "iac", "aws", "devops",
    ],
    "ci/cd": [
        "jenkins", "github actions", "gitlab ci", "devops",
        "continuous integration", "continuous deployment",
    ],

    # Databases
    "sql": [
        "postgresql", "mysql", "database", "data modeling",
        "queries", "relational database",
    ],
    "postgresql": [
        "sql", "postgres", "database", "relational database",
    ],
    "mysql": [
        "sql", "database", "relational database",
    ],
    "mongodb": [
        "nosql", "database", "document database",
    ],
    "redis": [
        "caching", "in-memory database", "nosql",
    ],

    # Data Engineering
    "data engineering": [
        "sql", "etl", "spark", "airflow", "data pipeline",
        "data warehouse", "python", "big data",
    ],
    "spark": [
        "apache spark", "pyspark", "big data", "data processing",
    ],
    "kafka": [
        "apache kafka", "streaming", "message queue", "event driven",
    ],

    # Frontend
    "react": [
        "javascript", "redux", "jsx", "hooks", "react native",
        "next.js", "typescript", "frontend",
    ],
    "vue.js": [
        "javascript", "vuex", "nuxt.js", "frontend",
    ],
    "angular": [
        "typescript", "rxjs", "frontend", "javascript",
    ],
    "frontend": [
        "html", "css", "javascript", "responsive design", "ui/ux",
    ],

    # Backend
    "backend": [
        "api", "rest", "database", "server", "microservices",
    ],
    "rest": [
        "api", "restful", "http", "json",
    ],
    "graphql": [
        "api", "apollo", "query language",
    ],
    "microservices": [
        "api", "docker", "kubernetes", "distributed systems",
    ],

    # Version Control
    "git": [
        "github", "gitlab", "bitbucket", "version control",
    ],

    # Agile/Methodology
    "agile": [
        "scrum", "kanban", "jira", "sprint",
    ],
    "scrum": [
        "agile", "sprint", "jira", "product management",
    ],

    # =========================================
    # DESIGN SKILLS
    # =========================================

    # UX/UI Design
    "ux design": [
        "ui design", "user research", "wireframing", "prototyping",
        "usability testing", "information architecture", "user flows",
        "persona creation", "journey mapping", "accessibility",
    ],
    "ui design": [
        "ux design", "visual design", "design systems", "responsive design",
        "mobile design", "web design", "interaction design",
    ],
    "figma": [
        "prototyping", "design systems", "ui design", "wireframing",
        "auto layout", "components", "variants", "ux design",
    ],
    "sketch": [
        "ui design", "prototyping", "symbols", "design systems", "ux design",
    ],
    "adobe xd": [
        "prototyping", "ui design", "wireframing", "design systems", "ux design",
    ],
    "graphic design": [
        "photoshop", "illustrator", "indesign", "typography",
        "branding", "visual design", "print design", "logo design",
    ],
    "photoshop": [
        "image editing", "photo retouching", "adobe creative suite",
        "graphic design", "digital art",
    ],
    "illustrator": [
        "vector graphics", "logo design", "illustration",
        "adobe creative suite", "graphic design",
    ],
    "indesign": [
        "print design", "layout design", "adobe creative suite",
        "graphic design", "typography",
    ],
    "product design": [
        "ux design", "ui design", "design thinking", "prototyping",
        "user research", "figma", "design systems",
    ],
    "design thinking": [
        "user research", "ideation", "prototyping", "empathy mapping",
        "brainstorming", "problem solving",
    ],
    "motion design": [
        "after effects", "animation", "video editing", "motion graphics",
    ],
    "after effects": [
        "motion design", "animation", "video editing", "adobe creative suite",
    ],

    # =========================================
    # PRODUCT/MANAGEMENT SKILLS
    # =========================================

    "product owner": [
        "product management", "backlog management", "user stories",
        "agile", "scrum", "stakeholder management", "roadmap",
        "prioritization", "jira", "requirements gathering",
    ],
    "product management": [
        "product strategy", "roadmap", "user stories", "agile",
        "stakeholder management", "market research", "okrs", "kpis",
    ],
    "scrum master": [
        "agile", "scrum", "facilitation", "sprint planning",
        "retrospectives", "jira", "kanban", "coaching",
    ],
    "tech lead": [
        "technical leadership", "architecture", "code review",
        "mentoring", "agile", "system design", "team management",
    ],
    "project management": [
        "jira", "confluence", "agile", "scrum", "kanban",
        "stakeholder management", "risk management", "budgeting",
    ],
    "engineering manager": [
        "people management", "technical leadership", "hiring",
        "performance reviews", "agile", "team building",
    ],
    "jira": [
        "agile", "project management", "bug tracking", "sprint planning",
        "backlog management", "confluence",
    ],
    "confluence": [
        "documentation", "jira", "wiki", "collaboration",
    ],

    # =========================================
    # QA/TESTING SKILLS
    # =========================================

    "qa": [
        "testing", "test cases", "bug tracking", "manual testing",
        "regression testing", "test planning", "quality assurance",
    ],
    "qa engineer": [
        "test automation", "selenium", "cypress", "api testing",
        "manual testing", "test cases", "bug tracking", "jira",
    ],
    "test automation": [
        "selenium", "cypress", "playwright", "pytest", "jest",
        "ci/cd", "api testing", "e2e testing",
    ],
    "selenium": [
        "test automation", "webdriver", "python", "java",
        "xpath", "css selectors", "page object model",
    ],
    "cypress": [
        "test automation", "javascript", "e2e testing",
        "api testing", "component testing",
    ],
    "playwright": [
        "test automation", "e2e testing", "api testing",
        "cross-browser testing", "typescript",
    ],
    "api testing": [
        "postman", "rest api", "json", "test automation",
        "integration testing",
    ],
    "postman": [
        "api testing", "rest api", "json", "api documentation",
    ],
    "performance testing": [
        "jmeter", "load testing", "stress testing",
        "gatling", "k6", "benchmarking",
    ],
    "jmeter": [
        "performance testing", "load testing", "stress testing",
    ],
    "sdet": [
        "test automation", "software development", "ci/cd",
        "api testing", "selenium", "programming",
    ],
    "manual testing": [
        "test cases", "bug tracking", "qa", "regression testing",
        "exploratory testing",
    ],

    # =========================================
    # DATA/ANALYTICS SKILLS
    # =========================================

    "database analyst": [
        "sql", "database design", "data modeling", "etl",
        "stored procedures", "query optimization", "reporting",
    ],
    "dba": [
        "database administration", "sql", "postgresql", "mysql",
        "oracle", "backup", "recovery", "performance tuning",
    ],
    "data analyst": [
        "sql", "excel", "tableau", "power bi", "python",
        "data visualization", "statistics", "reporting",
    ],
    "business analyst": [
        "requirements gathering", "sql", "data analysis",
        "stakeholder management", "documentation", "jira",
    ],
    "bi analyst": [
        "tableau", "power bi", "looker", "sql", "data visualization",
        "dashboards", "reporting", "etl",
    ],
    "tableau": [
        "data visualization", "dashboards", "sql", "bi",
        "reporting", "analytics",
    ],
    "power bi": [
        "data visualization", "dax", "dashboards", "sql",
        "reporting", "microsoft", "analytics",
    ],
    "looker": [
        "data visualization", "dashboards", "sql", "bi",
        "lookml", "analytics",
    ],
    "excel": [
        "spreadsheets", "data analysis", "pivot tables", "vlookup",
        "macros", "vba",
    ],

    # =========================================
    # OTHER TECH ROLES
    # =========================================

    "solutions architect": [
        "system design", "cloud architecture", "aws", "azure", "gcp",
        "microservices", "integration", "technical leadership",
    ],
    "technical writer": [
        "documentation", "api documentation", "markdown",
        "confluence", "readme", "technical communication",
    ],
    "devrel": [
        "developer relations", "technical writing", "public speaking",
        "community management", "documentation", "demos",
    ],
    "security engineer": [
        "cybersecurity", "penetration testing", "owasp",
        "vulnerability assessment", "security audits", "encryption",
    ],
    "cybersecurity": [
        "security", "penetration testing", "owasp", "encryption",
        "firewall", "network security",
    ],
    "sre": [
        "site reliability", "monitoring", "incident management",
        "kubernetes", "terraform", "observability", "on-call",
    ],
    "support engineer": [
        "troubleshooting", "customer support", "debugging",
        "ticketing systems", "technical support",
    ],
}

# Aliases for skills (alternative names for the same skill)
SKILL_ALIASES: Dict[str, str] = {
    # Developer aliases
    "k8s": "kubernetes",
    "k8": "kubernetes",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "react.js": "react",
    "reactjs": "react",
    "vue": "vue.js",
    "vuejs": "vue.js",
    "node": "node.js",
    "nodejs": "node.js",
    "golang": "go",
    "c sharp": "c#",
    "csharp": "c#",
    "dot net": ".net",
    "dotnet": ".net",
    "ml": "machine learning",
    "dl": "deep learning",
    "ai/ml": "machine learning",
    "nlp": "natural language processing",
    "restful": "rest",
    "ci cd": "ci/cd",
    "github-actions": "github actions",

    # Design aliases
    "ux": "ux design",
    "ui": "ui design",
    "ux/ui": "ux design",
    "ui/ux": "ux design",
    "user experience": "ux design",
    "user interface": "ui design",
    "xd": "adobe xd",
    "ps": "photoshop",
    "ai": "illustrator",  # Note: context-dependent, also used for AI
    "id": "indesign",
    "ae": "after effects",

    # Product/Management aliases
    "po": "product owner",
    "pm": "product management",
    "product manager": "product management",
    "sm": "scrum master",
    "em": "engineering manager",
    "tl": "tech lead",
    "technical lead": "tech lead",
    "lead developer": "tech lead",

    # QA/Testing aliases
    "qa tester": "qa engineer",
    "quality assurance": "qa",
    "qe": "qa engineer",
    "automation tester": "test automation",
    "automation engineer": "test automation",
    "test engineer": "qa engineer",

    # Data/Analytics aliases
    "db admin": "dba",
    "database administrator": "dba",
    "ba": "business analyst",
    "bi": "bi analyst",
    "business intelligence": "bi analyst",
    "data viz": "data visualization",
    "powerbi": "power bi",

    # Other tech roles aliases
    "sa": "solutions architect",
    "solution architect": "solutions architect",
    "tech writer": "technical writer",
    "doc writer": "technical writer",
    "infosec": "cybersecurity",
    "security": "cybersecurity",
    "site reliability engineer": "sre",
}


def normalize_skill(skill: str) -> str:
    """Normalize a skill name to its canonical form."""
    skill_lower = skill.lower().strip()
    return SKILL_ALIASES.get(skill_lower, skill_lower)


def expand_skills(skills: Set[str]) -> Set[str]:
    """
    Expand a set of skills with inferred related skills.

    Args:
        skills: Set of skill names from resume

    Returns:
        Expanded set including original and inferred skills
    """
    expanded = set()

    for skill in skills:
        # Add the original skill
        normalized = normalize_skill(skill)
        expanded.add(normalized)

        # Add related skills
        if normalized in SKILL_RELATIONSHIPS:
            related = SKILL_RELATIONSHIPS[normalized]
            for rel_skill in related:
                expanded.add(rel_skill.lower())

    return expanded


def get_skill_category(skill: str) -> Optional[str]:
    """
    Get the parent category for a skill.

    For example, "pytorch" -> "python", "react" -> "javascript"
    """
    skill_lower = normalize_skill(skill)

    for category, related in SKILL_RELATIONSHIPS.items():
        if skill_lower in [r.lower() for r in related]:
            return category

    return None
