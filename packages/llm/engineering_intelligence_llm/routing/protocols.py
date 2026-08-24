from __future__ import annotations

from typing import Protocol

from engineering_intelligence_llm.domain.models import LLMRequest
from engineering_intelligence_llm.domain.protocols import LLMProvider

class LLMRouter(Protocol):
    """Protocol for routing LLM requests to providers."""

    def select(self, request: LLMRequest) -> LLMProvider:
        """Select an LLM provider for a given request."""
        
        ...