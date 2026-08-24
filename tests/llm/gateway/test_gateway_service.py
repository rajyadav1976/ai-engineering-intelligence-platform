from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from engineering_intelligence_llm.domain.models import (
    LLMRequest,
    LLMResponse,
    Message,
    MessageRole,
)
from engineering_intelligence_llm.gateway import LLMGatewayService


class FakeLLMProvider:
    """Fake LLM provider for testing purposes."""

    @property
    def name(self) -> str:
        return "fake"

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        return LLMResponse(
            content="fake response",
            model=request.model or "fake-model",
            messages=(
                Message(
                    role=MessageRole.ASSISTANT,
                    content="This is a fake response.",
                ),
            ),
            provider=self.name,
        )

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        yield LLMResponse(
            content="fake",
            model=request.model or "fake-model",
            messages=(
                Message(
                    role=MessageRole.ASSISTANT,
                    content="fake",
                ),
            ),
            provider=self.name,
        )


class FakeRouter:
    """Fake router for Gateway unit tests."""

    def __init__(self, provider: FakeLLMProvider) -> None:
        self._provider = provider

    def select(
        self,
        request: LLMRequest,
    ) -> FakeLLMProvider:
        return self._provider


@pytest.mark.asyncio
async def test_gateway_routes_generate_to_selected_provider() -> None:
    provider = FakeLLMProvider()
    router = FakeRouter(provider)

    gateway = LLMGatewayService(router=router)

    request = LLMRequest(
        model="fake-model",
        messages=(
            Message(
                role=MessageRole.USER,
                content="Hello",
            ),
        ),
    )

    response = await gateway.generate(request)

    assert response.content == "fake response"
    assert response.model == "fake-model"
    assert response.provider == "fake"


@pytest.mark.asyncio
async def test_gateway_routes_stream_to_selected_provider() -> None:
    provider = FakeLLMProvider()
    router = FakeRouter(provider)

    gateway = LLMGatewayService(router=router)

    request = LLMRequest(
        model="fake-model",
        messages=(
            Message(
                role=MessageRole.USER,
                content="Hello",
            ),
        ),
    )

    responses = [
        response
        async for response in gateway.stream(request)
    ]

    assert len(responses) == 1
    assert responses[0].content == "fake"
    assert responses[0].provider == "fake"