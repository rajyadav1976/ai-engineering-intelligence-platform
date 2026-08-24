from __future__ import annotations

from engineering_intelligence_llm.domain.models import LLMRequest
from engineering_intelligence_llm.domain.protocols import LLMProvider

from .protocols import LLMRouter
from .registry import ProviderRegistry

class DefaultLLMRouter:
    '''Default provider router based on an explicit provider hint.'''

    def __init__(self, provider_registry: ProviderRegistry) -> None:
        self._registry = provider_registry

    def select(self, request: LLMRequest) -> LLMProvider:
        provider_name= request.metadata.get("provider")

        if not provider_name:
            raise ValueError("LLM request does not specify a provider")

        if not isinstance(provider_name, str):
            raise ValueError("LLM request provider metadata must be a string")

        return self._registry.get(provider_name)
    
        
         