"""Skill extractor service for normalizing and extracting skills."""

import re
from typing import Optional


class SkillExtractor:
    """Service for extracting and normalizing skills from text."""

    # Common skill name normalizations
    SKILL_NORMALIZATIONS = {
        # Programming languages
        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "py": "Python",
        "python": "Python",
        "python3": "Python",
        "golang": "Go",
        "go lang": "Go",
        "c++": "C++",
        "cpp": "C++",
        "c#": "C#",
        "csharp": "C#",
        "rb": "Ruby",
        "ruby": "Ruby",

        # Cloud platforms
        "aws": "AWS",
        "amazon web services": "AWS",
        "gcp": "Google Cloud Platform",
        "google cloud": "Google Cloud Platform",
        "azure": "Microsoft Azure",
        "ms azure": "Microsoft Azure",

        # Containers & Orchestration
        "k8s": "Kubernetes",
        "kubernetes": "Kubernetes",
        "docker": "Docker",

        # Databases
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "mongo": "MongoDB",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "dynamodb": "DynamoDB",

        # Frameworks
        "react": "React",
        "reactjs": "React",
        "react.js": "React",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "angular": "Angular",
        "angularjs": "Angular",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "express": "Express.js",
        "expressjs": "Express.js",
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "spring": "Spring",
        "spring boot": "Spring Boot",
        "springboot": "Spring Boot",
        "rails": "Ruby on Rails",
        "ruby on rails": "Ruby on Rails",
        "nextjs": "Next.js",
        "next.js": "Next.js",

        # AI/ML
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",
        "dl": "Deep Learning",
        "deep learning": "Deep Learning",
        "nlp": "Natural Language Processing",
        "natural language processing": "Natural Language Processing",
        "langchain": "LangChain",
        "llm": "Large Language Models",
        "rag": "RAG",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",

        # DevOps & Tools
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "ci cd": "CI/CD",
        "terraform": "Terraform",
        "ansible": "Ansible",
        "jenkins": "Jenkins",
        "github actions": "GitHub Actions",
        "gitlab ci": "GitLab CI",
        "git": "Git",
        "linux": "Linux",

        # Methodologies
        "agile": "Agile",
        "scrum": "Scrum",
        "kanban": "Kanban",
        "tdd": "Test-Driven Development",
        "bdd": "Behavior-Driven Development",

        # Data
        "sql": "SQL",
        "nosql": "NoSQL",
        "graphql": "GraphQL",
        "rest": "REST API",
        "rest api": "REST API",
        "restful": "REST API",
        "api": "API Development",
    }

    @classmethod
    def normalize_skill(cls, skill_name: str) -> str:
        """
        Normalize a skill name to its standard form.

        Args:
            skill_name: Raw skill name

        Returns:
            Normalized skill name
        """
        # Clean the input
        cleaned = skill_name.strip().lower()

        # Check direct normalizations
        if cleaned in cls.SKILL_NORMALIZATIONS:
            return cls.SKILL_NORMALIZATIONS[cleaned]

        # Return title case if no normalization found
        return skill_name.strip().title()

    @classmethod
    def extract_skills_from_text(cls, text: str) -> list[str]:
        """
        Extract potential skill keywords from text.

        Args:
            text: Text to extract skills from

        Returns:
            List of extracted skill names (normalized)
        """
        skills = set()

        # Convert to lowercase for matching
        text_lower = text.lower()

        # Check for known skills
        for raw_name, normalized in cls.SKILL_NORMALIZATIONS.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(raw_name) + r'\b'
            if re.search(pattern, text_lower):
                skills.add(normalized)

        return list(skills)

    @classmethod
    def estimate_skill_level(
        cls,
        years_experience: Optional[float] = None,
        context: Optional[str] = None,
    ) -> str:
        """
        Estimate skill level based on experience and context.

        Args:
            years_experience: Years of experience with the skill
            context: Additional context (e.g., "lead", "senior", "learning")

        Returns:
            Skill level: beginner, intermediate, advanced, or expert
        """
        # Check context for level hints
        if context:
            context_lower = context.lower()
            if any(word in context_lower for word in ["lead", "architect", "principal", "expert"]):
                return "expert"
            elif any(word in context_lower for word in ["senior", "advanced", "specialist"]):
                return "advanced"
            elif any(word in context_lower for word in ["learning", "basic", "familiar"]):
                return "beginner"

        # Use years of experience
        if years_experience is not None:
            if years_experience >= 5:
                return "expert"
            elif years_experience >= 3:
                return "advanced"
            elif years_experience >= 1:
                return "intermediate"
            else:
                return "beginner"

        # Default to intermediate
        return "intermediate"
