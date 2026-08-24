from __future__ import annotations

from engineering_intelligence_llm.domain.models import (
    LLMRequest,
    LLMResponse,
)
from engineering_intelligence_llm.domain.protocols import LLMProvider
from engineering_intelligence_llm.routing import LLMRouter

class FakeProvider:
    @property
    def name(self) -> str:
        return "fake"
      
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError

    async def stream(self, request: LLMRequest):
        raise NotImplementedError

class FakeRouter:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider


    def select(self, request: LLMRequest) -> LLMProvider:
        return self._provider

def test_router_selects_provider() -> None:
    provider = FakeProvider()
    router = FakeRouter(provider)

    request = LLMRequest(
        model="fake-model",
        messages=(),
    )

    selected_provider = router.select(request)

    assert selected_provider is provider    
        