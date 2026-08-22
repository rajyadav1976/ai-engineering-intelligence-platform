from __future__ import annotations

from collections.abc import AsyncIterator
from engineering_intelligence_llm.domain.models import LLMRequest, LLMResponse
from engineering_intelligence_llm.domain.protocols import LLMProvider

class LLMGatewayService:
    """Default implementation of the platform LLM Gateway."""

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a complete LLM response."""
        return await self._provider.generate(request)

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        """Generate complete LLM response as a streaming."""
        async for response in self._provider.stream(request):
            yield response

