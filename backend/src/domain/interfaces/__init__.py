"""Domain interfaces - Ports for external dependencies."""

from .llm_gateway import ILLMGateway
from .document_parser import IDocumentParser

__all__ = ["ILLMGateway", "IDocumentParser"]
