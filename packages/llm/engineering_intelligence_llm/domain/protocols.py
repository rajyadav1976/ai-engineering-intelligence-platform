from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from .models import LLMRequest, LLMResponse


class LLMProvider(Protocol):
    """Provider-independent contract for LLM providers."""

    @property
    def name(self) -> str:
        """Return the provider identifier."""
        ...

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a complete LLM response."""
        ...

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        """Generate an LLM response as a stream of response chunks."""
        ...