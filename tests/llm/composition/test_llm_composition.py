from __future__ import annotations

from engineering_intelligence_infrastructure.configuration import (
    get_settings,
)   

from engineering_intelligence_llm.composition import (
    create_default_llm_gateway,
)
from engineering_intelligence_llm.gateway import LLMGatewayService
from engineering_intelligence_llm.routing import DefaultLLMRouter


def test_default_gateway_is_wired_with_default_router() -> None:
    gateway = create_default_llm_gateway()

    assert isinstance(gateway, LLMGatewayService)
    assert isinstance(gateway._router, DefaultLLMRouter)

def test_default_gateway_uses_application_configuration() -> None:
    settings = get_settings()

    gateway = create_default_llm_gateway()

    assert isinstance(gateway, LLMGatewayService)
    assert gateway._router is not None    