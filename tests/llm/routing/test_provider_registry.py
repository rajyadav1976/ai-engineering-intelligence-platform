from __future__ import annotations
import re

import pytest

from engineering_intelligence_llm.domain.models import (
    LLMRequest,
    LLMResponse,
)
from engineering_intelligence_llm.routing import ProviderRegistry

class FakeProvider:
    def __init__(self, provider_name: str):
        self._name = provider_name
    
    @property
    def name(self) -> str:
        return self._name

    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError

    async def stream(self, request: LLMRequest):
        raise NotImplementedError

def test_provider_can_be_registered_and_retrieved() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider("fake")
    registry.register(provider)
    
    assert registry.get("fake") is provider
    assert registry.contains("fake")
    assert registry.names() == ("fake",)

def test_duplicate_provider_registration_is_rejected() -> None:
    registry = ProviderRegistry()
    registry.register(FakeProvider("fake"))

    with pytest.raises(ValueError, match="LLM provider 'fake' is already registered"):
        registry.register(FakeProvider("fake"))

def test_unknown_provider_is_rejected() -> None:
    registry = ProviderRegistry()

    with pytest.raises(ValueError, match="LLM provider 'unknown' is not registered"):
        registry.get("unknown")