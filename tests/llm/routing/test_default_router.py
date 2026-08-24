from __future__ import annotations

import pytest

from engineering_intelligence_llm.domain.models import (
    LLMRequest,
    LLMResponse,
)
from engineering_intelligence_llm.routing import (
    DefaultLLMRouter,
    ProviderRegistry,
)


class FakeProvider:
    def __init__(self, provider_name: str) -> None:
        self._name = provider_name

    @property
    def name(self) -> str:
        return self._name

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        raise NotImplementedError

    async def stream(self, request: LLMRequest):
        raise NotImplementedError


def test_default_router_selects_requested_provider() -> None:
    registry = ProviderRegistry()

    ollama = FakeProvider("ollama")
    openai = FakeProvider("openai")

    registry.register(ollama)
    registry.register(openai)

    router = DefaultLLMRouter(registry)

    request = LLMRequest(
        model="qwen3:latest",
        messages=(),
        metadata={
            "provider": "ollama",
        },
    )

    selected = router.select(request)

    assert selected is ollama


def test_default_router_can_select_different_provider() -> None:
    registry = ProviderRegistry()

    ollama = FakeProvider("ollama")
    openai = FakeProvider("openai")

    registry.register(ollama)
    registry.register(openai)

    router = DefaultLLMRouter(registry)

    request = LLMRequest(
        model="some-model",
        messages=(),
        metadata={
            "provider": "openai",
        },
    )

    selected = router.select(request)

    assert selected is openai


def test_default_router_requires_provider() -> None:
    registry = ProviderRegistry()
    router = DefaultLLMRouter(registry)

    request = LLMRequest(
        model="qwen3:latest",
        messages=(),
    )

    with pytest.raises(
        ValueError,
        match="LLM request does not specify a provider",
    ):
        router.select(request)


def test_default_router_rejects_unknown_provider() -> None:
    registry = ProviderRegistry()
    router = DefaultLLMRouter(registry)

    request = LLMRequest(
        model="qwen3:latest",
        messages=(),
        metadata={
            "provider": "unknown",
        },
    )

    with pytest.raises(
        ValueError,
        match="LLM provider 'unknown' is not registered",
    ):
        router.select(request)