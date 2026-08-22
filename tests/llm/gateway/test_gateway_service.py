from __future__ import annotations

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
    ):
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


@pytest.mark.asyncio
async def test_gateway_delegates_generate_to_provider() -> None:
    provider = FakeLLMProvider()
    gateway = LLMGatewayService(provider=provider)

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