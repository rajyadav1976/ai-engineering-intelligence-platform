import pytest

from engineering_intelligence_llm.domain import (
    LLMRequest,
    Message,
    MessageRole,   
)

from engineering_intelligence_llm.providers import OllamaProvider

@pytest.mark.asyncio
async def test_ollama_provider_generates_response() -> None:
    provider = OllamaProvider(base_url="http://localhost:11434")
    request = LLMRequest(
        model="qwen3:latest",  # Specify the model name if required
        messages=(
            Message(role=MessageRole.USER, content="What is 2 + 2?"),
        )
    )
    response = await provider.generate(request)

    assert response is not None
    assert response.provider == "Ollama"
    assert response.model == "qwen3:latest"
    assert response.content
    
