from __future__ import annotations

from engineering_intelligence_infrastructure.configuration import get_settings
from engineering_intelligence_llm.gateway import (
    LLMGateway,
    LLMGatewayService,
)
from engineering_intelligence_llm.providers import OllamaProvider
from engineering_intelligence_llm.routing import (
    DefaultLLMRouter,
    ProviderRegistry,
)


def create_default_llm_gateway() -> LLMGateway:
    """Create the default platform LLM Gateway from application configuration."""

    ollama_provider = OllamaProvider(
        base_url=get_settings().ollama_host,
    )

    registry = ProviderRegistry()

    registry.register(ollama_provider)

    router = DefaultLLMRouter(
        provider_registry=registry,
    )

    return LLMGatewayService(
        router=router,
    )
