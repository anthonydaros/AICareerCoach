"""Unit tests for Skill Relationships service."""

import pytest
from src.domain.services.skill_relationships import (
    expand_skills,
    normalize_skill,
    get_skill_category,
    SKILL_RELATIONSHIPS,
    SKILL_ALIASES,
)


class TestNormalizeSkill:
    """Test cases for skill normalization."""

    def test_normalizes_lowercase(self):
        """Test that skills are normalized to lowercase."""
        assert normalize_skill("Python") == "python"
        assert normalize_skill("REACT") == "react"

    def test_strips_whitespace(self):
        """Test that whitespace is stripped."""
        assert normalize_skill("  python  ") == "python"

    def test_resolves_common_aliases(self):
        """Test that common aliases are resolved."""
        assert normalize_skill("k8s") == "kubernetes"
        assert normalize_skill("js") == "javascript"
        assert normalize_skill("ts") == "typescript"
        assert normalize_skill("postgres") == "postgresql"

    def test_low_code_aliases(self):
        """Test low-code tool aliases."""
        assert normalize_skill("integromat") == "make"
        assert normalize_skill("make.com") == "make"
        assert normalize_skill("zap") == "zapier"
        assert normalize_skill("power platform") == "power automate"
        assert normalize_skill("ms power automate") == "power automate"

    def test_ai_llm_aliases(self):
        """Test AI/LLM tool aliases."""
        assert normalize_skill("gpt") == "openai api"
        assert normalize_skill("chatgpt") == "openai api"
        assert normalize_skill("openai") == "openai api"
        assert normalize_skill("lc") == "langchain"
        assert normalize_skill("hf") == "hugging face"
        assert normalize_skill("huggingface") == "hugging face"
        assert normalize_skill("claude") == "anthropic api"
        assert normalize_skill("retrieval augmented generation") == "rag"


class TestExpandSkills:
    """Test cases for skill expansion."""

    def test_expands_programming_languages(self):
        """Test that programming languages expand to related skills."""
        skills = {"python"}
        expanded = expand_skills(skills)

        assert "python" in expanded
        assert "pytorch" in expanded
        assert "fastapi" in expanded
        assert "pandas" in expanded

    def test_expands_javascript(self):
        """Test JavaScript skill expansion."""
        skills = {"javascript"}
        expanded = expand_skills(skills)

        assert "javascript" in expanded
        assert "react" in expanded
        assert "node.js" in expanded
        assert "typescript" in expanded

    def test_expands_cloud_platforms(self):
        """Test cloud platform skill expansion."""
        skills = {"aws"}
        expanded = expand_skills(skills)

        assert "aws" in expanded
        assert "ec2" in expanded
        assert "s3" in expanded
        assert "lambda" in expanded

    def test_expands_low_code_tools(self):
        """Test low-code tool skill expansion."""
        # Test n8n
        skills = {"n8n"}
        expanded = expand_skills(skills)
        assert "n8n" in expanded
        assert "webhooks" in expanded
        assert "automation workflows" in expanded

        # Test Make (Integromat)
        skills = {"make"}
        expanded = expand_skills(skills)
        assert "make" in expanded
        assert "integromat" in expanded
        assert "automation" in expanded

        # Test Zapier
        skills = {"zapier"}
        expanded = expand_skills(skills)
        assert "zapier" in expanded
        assert "zaps" in expanded
        assert "integrations" in expanded

    def test_expands_ai_llm_tools(self):
        """Test AI/LLM tool skill expansion."""
        # Test LangChain
        skills = {"langchain"}
        expanded = expand_skills(skills)
        assert "langchain" in expanded
        assert "llms" in expanded
        assert "rag" in expanded
        assert "agents" in expanded

        # Test CrewAI
        skills = {"crewai"}
        expanded = expand_skills(skills)
        assert "crewai" in expanded
        assert "multi-agent systems" in expanded
        assert "task orchestration" in expanded

        # Test RAG
        skills = {"rag"}
        expanded = expand_skills(skills)
        assert "rag" in expanded
        assert "vector databases" in expanded
        assert "embeddings" in expanded
        assert "langchain" in expanded

    def test_expands_vector_databases(self):
        """Test vector database skill expansion."""
        # Test Pinecone
        skills = {"pinecone"}
        expanded = expand_skills(skills)
        assert "pinecone" in expanded
        assert "vector database" in expanded
        assert "embeddings" in expanded

        # Test Chroma
        skills = {"chroma"}
        expanded = expand_skills(skills)
        assert "chroma" in expanded
        assert "rag" in expanded
        assert "langchain" in expanded

    def test_handles_aliases_in_expansion(self):
        """Test that aliases are resolved before expansion."""
        # "integromat" should normalize to "make" and expand
        skills = {"integromat"}
        expanded = expand_skills(skills)
        assert "make" in expanded
        assert "automation" in expanded

        # "chatgpt" should normalize to "openai api" and expand
        skills = {"chatgpt"}
        expanded = expand_skills(skills)
        assert "openai api" in expanded
        assert "prompt engineering" in expanded

    def test_multiple_skills_expansion(self):
        """Test expansion with multiple skills."""
        skills = {"python", "langchain", "n8n"}
        expanded = expand_skills(skills)

        # Python related
        assert "pytorch" in expanded
        assert "pandas" in expanded

        # LangChain related
        assert "rag" in expanded
        assert "agents" in expanded

        # n8n related
        assert "webhooks" in expanded
        assert "automation workflows" in expanded

    def test_empty_skills_returns_empty(self):
        """Test that empty input returns empty set."""
        expanded = expand_skills(set())
        assert expanded == set()

    def test_unknown_skill_preserved(self):
        """Test that unknown skills are preserved."""
        skills = {"unknown_skill_xyz"}
        expanded = expand_skills(skills)
        assert "unknown_skill_xyz" in expanded


class TestGetSkillCategory:
    """Test cases for skill category detection."""

    def test_detects_python_libraries(self):
        """Test that Python libraries are categorized correctly."""
        assert get_skill_category("pytorch") == "python"
        assert get_skill_category("pandas") == "python"
        assert get_skill_category("fastapi") == "python"

    def test_detects_javascript_frameworks(self):
        """Test that JavaScript frameworks are categorized correctly."""
        assert get_skill_category("react") == "javascript"
        assert get_skill_category("node.js") == "javascript"

    def test_returns_none_for_unknown(self):
        """Test that unknown skills return None."""
        # Parent categories don't have parents themselves, but may be children of other categories
        # Use truly unknown skills for this test
        assert get_skill_category("unknown_skill_xyz") is None
        assert get_skill_category("nonexistent_framework") is None
        # Test that direct children are correctly categorized (not None)
        assert get_skill_category("pytorch") == "python"  # pytorch is a Python child


class TestSkillRelationshipsData:
    """Test cases for skill relationships data structure."""

    def test_low_code_tools_present(self):
        """Test that all low-code tools are defined."""
        low_code_tools = ["n8n", "make", "zapier", "power automate", "airtable",
                         "notion", "retool", "bubble", "webflow", "appsmith"]
        for tool in low_code_tools:
            assert tool in SKILL_RELATIONSHIPS, f"Missing low-code tool: {tool}"

    def test_ai_llm_tools_present(self):
        """Test that all AI/LLM tools are defined."""
        ai_tools = ["langchain", "crewai", "openai api", "rag", "prompt engineering",
                    "hugging face", "pinecone", "weaviate", "chroma", "faiss",
                    "ollama", "llamaindex", "semantic kernel", "anthropic api",
                    "embeddings", "fine-tuning"]
        for tool in ai_tools:
            assert tool in SKILL_RELATIONSHIPS, f"Missing AI/LLM tool: {tool}"

    def test_design_skills_present(self):
        """Test that design skills are defined."""
        design_skills = ["ux design", "ui design", "figma", "sketch", "adobe xd",
                         "photoshop", "illustrator", "product design"]
        for skill in design_skills:
            assert skill in SKILL_RELATIONSHIPS, f"Missing design skill: {skill}"

    def test_qa_skills_present(self):
        """Test that QA skills are defined."""
        qa_skills = ["qa", "qa engineer", "test automation", "selenium", "cypress",
                     "playwright", "api testing", "postman"]
        for skill in qa_skills:
            assert skill in SKILL_RELATIONSHIPS, f"Missing QA skill: {skill}"

    def test_low_code_aliases_present(self):
        """Test that low-code aliases are defined."""
        assert SKILL_ALIASES.get("integromat") == "make"
        assert SKILL_ALIASES.get("make.com") == "make"
        assert SKILL_ALIASES.get("power platform") == "power automate"
        assert SKILL_ALIASES.get("zap") == "zapier"

    def test_ai_llm_aliases_present(self):
        """Test that AI/LLM aliases are defined."""
        assert SKILL_ALIASES.get("gpt") == "openai api"
        assert SKILL_ALIASES.get("chatgpt") == "openai api"
        assert SKILL_ALIASES.get("lc") == "langchain"
        assert SKILL_ALIASES.get("hf") == "hugging face"
        assert SKILL_ALIASES.get("claude") == "anthropic api"
