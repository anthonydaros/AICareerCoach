"""Dependency injection for API routes."""

from functools import lru_cache

from src.infrastructure.llm import OpenAIGateway
from src.domain.services.ats_scorer import ATSScorer
from src.domain.services.job_matcher import JobMatcher
from src.application.orchestrator import CareerCoachOrchestrator


@lru_cache
def get_llm_gateway() -> OpenAIGateway:
    """Get LLM gateway instance."""
    return OpenAIGateway()


@lru_cache
def get_ats_scorer() -> ATSScorer:
    """Get ATS scorer instance."""
    return ATSScorer()


@lru_cache
def get_job_matcher() -> JobMatcher:
    """Get job matcher instance."""
    return JobMatcher()


@lru_cache
def get_orchestrator() -> CareerCoachOrchestrator:
    """Get orchestrator instance."""
    return CareerCoachOrchestrator(
        llm_gateway=get_llm_gateway(),
        ats_scorer=get_ats_scorer(),
        job_matcher=get_job_matcher(),
    )
