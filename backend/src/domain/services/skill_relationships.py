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

    # =========================================
    # LOW-CODE & AUTOMATION TOOLS
    # =========================================

    "n8n": [
        "webhooks", "apis", "json", "automation workflows", "http requests",
        "integrations", "triggers", "data transformation", "low-code",
    ],
    "make": [
        "integromat", "scenarios", "modules", "data transformation",
        "filters", "automation", "webhooks", "api",
    ],
    "zapier": [
        "zaps", "triggers", "actions", "multi-step workflows", "paths",
        "automation", "integrations",
    ],
    "power automate": [
        "microsoft 365", "azure", "sharepoint", "power platform",
        "flows", "automation", "microsoft",
    ],
    "airtable": [
        "spreadsheets", "databases", "apis", "views", "automations",
        "no-code", "formulas",
    ],
    "notion": [
        "databases", "templates", "formulas", "api", "integrations",
        "documentation", "wiki",
    ],
    "retool": [
        "sql", "react basics", "internal tools", "database queries",
        "apis", "admin panels",
    ],
    "bubble": [
        "no-code apps", "workflows", "database design", "visual programming",
    ],
    "webflow": [
        "html", "css", "responsive design", "cms", "visual design",
        "no-code", "web design",
    ],
    "appsmith": [
        "sql", "javascript", "internal tools", "apis", "admin dashboards",
    ],

    # =========================================
    # AI & LLM TOOLS (EXPANDED)
    # =========================================

    "langchain": [
        "python", "llms", "chains", "agents", "rag", "memory",
        "prompts", "retrievers", "vector stores", "openai",
    ],
    "crewai": [
        "multi-agent systems", "langchain", "python", "task orchestration",
        "agents", "llm", "ai agents",
    ],
    "openai api": [
        "rest apis", "prompt engineering", "tokens", "function calling",
        "embeddings", "gpt", "chat completions", "llm",
    ],
    "rag": [
        "vector databases", "embeddings", "semantic search", "chunking",
        "retrieval", "langchain", "llamaindex", "llm",
    ],
    "prompt engineering": [
        "llms", "chatgpt", "claude", "chain-of-thought", "few-shot learning",
        "prompts", "gpt", "ai",
    ],
    "hugging face": [
        "transformers", "pytorch", "model fine-tuning", "datasets",
        "models", "nlp", "machine learning",
    ],
    "pinecone": [
        "vector database", "embeddings", "similarity search", "rag",
        "semantic search", "llm",
    ],
    "weaviate": [
        "vector database", "embeddings", "semantic search", "rag",
        "graphql", "llm",
    ],
    "chroma": [
        "vector database", "embeddings", "local", "rag", "langchain",
        "llm", "python",
    ],
    "faiss": [
        "vector search", "embeddings", "similarity search", "meta",
        "rag", "machine learning",
    ],
    "ollama": [
        "local llms", "model deployment", "apis", "quantization",
        "llama", "mistral", "self-hosted", "llm",
    ],
    "llamaindex": [
        "rag", "data connectors", "indexing", "query engines",
        "llm", "embeddings", "python",
    ],
    "semantic kernel": [
        ".net", "ai orchestration", "plugins", "memory", "microsoft",
        "llm", "c#",
    ],
    "anthropic api": [
        "claude", "llm", "prompt engineering", "tokens",
        "chat completions", "ai",
    ],
    "embeddings": [
        "vector databases", "semantic search", "rag", "similarity",
        "nlp", "machine learning",
    ],
    "fine-tuning": [
        "model training", "machine learning", "llm", "hugging face",
        "pytorch", "transfer learning",
    ],

    # =========================================
    # EXPANDED AI/LLM TOOLS
    # =========================================

    "autogen": [
        "multi-agent systems", "microsoft", "llm", "agents",
        "conversational ai", "python", "ai orchestration",
    ],
    "dspy": [
        "llm programming", "prompt optimization", "python",
        "machine learning", "llm", "stanford",
    ],
    "guidance": [
        "llm control", "constrained generation", "microsoft",
        "python", "llm", "structured output",
    ],
    "instructor": [
        "structured output", "pydantic", "llm", "python",
        "function calling", "json schema",
    ],
    "litellm": [
        "llm gateway", "api proxy", "openai", "anthropic",
        "unified api", "python", "llm",
    ],
    "vllm": [
        "llm inference", "high throughput", "serving", "gpu",
        "llm", "deployment", "python",
    ],
    "text-generation-inference": [
        "llm serving", "hugging face", "deployment", "gpu",
        "llm", "inference", "tgi",
    ],
    "mlflow": [
        "experiment tracking", "model registry", "mlops",
        "machine learning", "model deployment",
    ],
    "weights & biases": [
        "experiment tracking", "mlops", "visualization",
        "machine learning", "model monitoring", "wandb",
    ],
    "modal": [
        "serverless gpu", "python", "deployment", "inference",
        "machine learning", "cloud",
    ],

    # =========================================
    # PRODUCT & ANALYTICS EXPANDED
    # =========================================

    "amplitude": [
        "product analytics", "user behavior", "cohort analysis",
        "funnels", "retention", "analytics",
    ],
    "mixpanel": [
        "product analytics", "event tracking", "user flows",
        "retention analysis", "analytics",
    ],
    "segment": [
        "customer data platform", "data collection", "integrations",
        "analytics", "cdp",
    ],
    "heap": [
        "auto-capture analytics", "product analytics", "user behavior",
        "retroactive analysis", "analytics",
    ],
    "hotjar": [
        "heatmaps", "session recordings", "user research",
        "feedback", "ux research",
    ],
    "fullstory": [
        "session replay", "digital experience", "user behavior",
        "analytics", "ux research",
    ],
    "google analytics": [
        "web analytics", "ga4", "user behavior", "reporting",
        "marketing analytics", "analytics",
    ],
    "snowflake": [
        "data warehouse", "cloud data", "sql", "data engineering",
        "analytics", "data lake",
    ],
    "databricks": [
        "data engineering", "spark", "delta lake", "machine learning",
        "analytics", "mlops",
    ],
    "dbt": [
        "data transformation", "sql", "analytics engineering",
        "data modeling", "elt", "data engineering",
    ],
    "fivetran": [
        "data integration", "etl", "connectors", "data engineering",
        "data pipeline",
    ],
    "airbyte": [
        "data integration", "open source", "etl", "connectors",
        "data engineering", "elt",
    ],

    # =========================================
    # MOBILE DEVELOPMENT EXPANDED
    # =========================================

    "swift": [
        "ios", "swiftui", "uikit", "xcode", "apple",
        "mobile development", "macos",
    ],
    "kotlin": [
        "android", "jetpack compose", "android studio",
        "mobile development", "jvm",
    ],
    "react native": [
        "javascript", "mobile development", "ios", "android",
        "cross-platform", "expo", "react",
    ],
    "flutter": [
        "dart", "mobile development", "ios", "android",
        "cross-platform", "google",
    ],
    "expo": [
        "react native", "mobile development", "cross-platform",
        "javascript", "eas",
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

    # Low-code/Automation aliases
    "integromat": "make",
    "make.com": "make",
    "power platform": "power automate",
    "ms power automate": "power automate",
    "microsoft power automate": "power automate",
    "zap": "zapier",

    # AI/LLM aliases
    "gpt": "openai api",
    "chatgpt": "openai api",
    "openai": "openai api",
    "gpt-4": "openai api",
    "gpt-3.5": "openai api",
    "lc": "langchain",
    "hf": "hugging face",
    "huggingface": "hugging face",
    "transformers": "hugging face",
    "claude": "anthropic api",
    "claude api": "anthropic api",
    "vector db": "vector databases",
    "vectordb": "vector databases",
    "retrieval augmented generation": "rag",

    # Additional AI/ML aliases
    "ag2": "autogen",
    "autogen studio": "autogen",
    "w&b": "weights & biases",
    "wandb": "weights & biases",
    "tgi": "text-generation-inference",
    "llama.cpp": "local llms",
    "llamacpp": "local llms",

    # Analytics aliases
    "ga": "google analytics",
    "ga4": "google analytics",
    "data build tool": "dbt",

    # Mobile aliases
    "rn": "react native",
    "swiftui": "swift",
    "jetpack": "kotlin",
    "jetpack compose": "kotlin",
}

# Transferable skills matrix - maps skills that can transfer to other roles
TRANSFERABLE_SKILLS: Dict[str, List[str]] = {
    # From backend to related areas
    "python": ["data science", "machine learning", "automation", "scripting"],
    "java": ["android", "enterprise", "microservices"],
    "javascript": ["frontend", "full stack", "react native"],

    # From data to related areas
    "sql": ["data analysis", "business intelligence", "data engineering"],
    "pandas": ["data analysis", "data science", "automation"],
    "excel": ["data analysis", "business intelligence", "reporting"],

    # From DevOps to related areas
    "docker": ["kubernetes", "devops", "cloud", "sre"],
    "terraform": ["cloud", "infrastructure", "devops"],
    "aws": ["cloud architecture", "solutions architecture", "devops"],

    # From ML to related areas
    "machine learning": ["data science", "ai engineering", "mlops"],
    "pytorch": ["deep learning", "research", "computer vision", "nlp"],
    "langchain": ["ai engineering", "rag", "llm applications"],

    # From management to related areas
    "project management": ["product management", "scrum master", "team lead"],
    "agile": ["scrum master", "product owner", "project management"],
    "leadership": ["management", "tech lead", "director"],

    # From QA to related areas
    "test automation": ["sdet", "devops", "software engineering"],
    "selenium": ["test automation", "web scraping", "automation"],

    # From design to related areas
    "figma": ["product design", "ux design", "ui design"],
    "ux design": ["product design", "user research", "product management"],
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


def get_transferable_skills(skills: Set[str]) -> Dict[str, List[str]]:
    """
    Get transferable skills and potential career paths based on current skills.

    Args:
        skills: Set of skill names from resume

    Returns:
        Dict mapping each skill to potential career areas it transfers to
    """
    result = {}

    for skill in skills:
        normalized = normalize_skill(skill)
        if normalized in TRANSFERABLE_SKILLS:
            result[normalized] = TRANSFERABLE_SKILLS[normalized]

    return result


def find_skill_matches(
    resume_skills: Set[str],
    required_skills: List[str],
    preferred_skills: List[str] = None
) -> Dict[str, any]:
    """
    Find matches between resume skills and job requirements.

    Args:
        resume_skills: Set of skills from resume
        required_skills: List of required skills from job
        preferred_skills: List of preferred/nice-to-have skills

    Returns:
        Dict with matched, missing, and partial matches
    """
    preferred_skills = preferred_skills or []

    # Expand resume skills with related skills
    expanded_resume = expand_skills(resume_skills)

    # Normalize all skills
    resume_normalized = {normalize_skill(s) for s in expanded_resume}
    required_normalized = [normalize_skill(s) for s in required_skills]
    preferred_normalized = [normalize_skill(s) for s in preferred_skills]

    # Find matches
    matched_required = []
    missing_required = []

    for skill in required_normalized:
        if skill in resume_normalized:
            matched_required.append(skill)
        else:
            # Check for partial/related matches
            found_related = False
            for resume_skill in resume_normalized:
                if resume_skill in SKILL_RELATIONSHIPS.get(skill, []):
                    matched_required.append(skill)
                    found_related = True
                    break
            if not found_related:
                missing_required.append(skill)

    matched_preferred = [s for s in preferred_normalized if s in resume_normalized]
    missing_preferred = [s for s in preferred_normalized if s not in resume_normalized]

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "required_match_rate": len(matched_required) / len(required_normalized) if required_normalized else 1.0,
        "preferred_match_rate": len(matched_preferred) / len(preferred_normalized) if preferred_normalized else 1.0,
    }
