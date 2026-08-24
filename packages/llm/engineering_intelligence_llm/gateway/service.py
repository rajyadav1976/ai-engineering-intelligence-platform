from __future__ import annotations

from collections.abc import AsyncIterator
from engineering_intelligence_llm.domain.models import LLMRequest, LLMResponse
from engineering_intelligence_llm.routing.protocols import LLMRouter

class LLMGatewayService:
    """Default implementation of the platform LLM Gateway."""

    def __init__(self, router: LLMRouter) -> None:
        self._router = router

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a complete LLM response."""
        provider = self._router.select(request)  
        return await provider.generate(request)

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        """Generate complete LLM response as a streaming."""
        provider = self._router.select(request)
        async for response in provider.stream(request):
            yield response

