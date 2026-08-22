from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from engineering_intelligence_llm.domain.models import (
    LLMRequest, 
    LLMResponse
)


class LLMGateway(Protocol):
    """Platform level contract for LLM interface."""

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        '''Generate a complete LLM response'''
        ...

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        '''Generate complete LLM response as a streaming'''
        ...