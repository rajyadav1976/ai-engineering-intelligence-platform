from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from engineering_intelligence_llm.domain.models import (
    LLMRequest,
    LLMResponse,
    Message,
    TokenUsage,
)


class OllamaProvider:
    """Ollama implementation of the platform LLM provider contract."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @property
    def name(self) -> str:
        return "ollama"

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        payload = self._build_chat_payload(request)

        async with httpx.AsyncClient(
            timeout=self._timeout,
        ) as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json=payload,
            )

            response.raise_for_status()

            data: dict[str, Any] = response.json()

        return self._build_response(
            request=request,
            data=data,
        )

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[LLMResponse]:
        payload = self._build_chat_payload(request)
        payload["stream"] = True

        async with httpx.AsyncClient(
            timeout=self._timeout,
        ) as client:
            async with client.stream(
                "POST",
                f"{self._base_url}/api/chat",
                json=payload,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    chunk: dict[str, Any] = json.loads(line)

                    yield self._build_stream_response(
                        request=request,
                        data=chunk,
                    )

    def _build_chat_payload(
        self,
        request: LLMRequest,
    ) -> dict[str, Any]:
        if not request.model:
            raise ValueError(
                "OllamaProvider requires a model in LLMRequest.model"
            )

        return {
            "model": request.model,
            "messages": [
                self._convert_message(message)
                for message in request.messages
            ],
            "stream": False,
            "options": self._build_generation_options(request),
        }

    @staticmethod
    def _convert_message(
        message: Message,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "role": message.role.value,
            "content": message.content,
        }

        if message.name:
            payload["name"] = message.name

        if message.tool_call_id:
            payload["tool_call_id"] = message.tool_call_id

        return payload

    @staticmethod
    def _build_generation_options(
        request: LLMRequest,
    ) -> dict[str, Any]:
        generation = request.generation

        options: dict[str, Any] = {}

        if generation.temperature is not None:
            options["temperature"] = generation.temperature

        if generation.top_p is not None:
            options["top_p"] = generation.top_p

        if generation.max_tokens is not None:
            options["num_predict"] = generation.max_tokens

        if generation.stop:
            options["stop"] = list(generation.stop)

        return options

    def _build_response(
        self,
        request: LLMRequest,
        data: dict[str, Any],
    ) -> LLMResponse:
        message_data = data.get("message", {})

        content = message_data.get("content", "")

        assistant_message = Message(
            role="assistant",
            content=content,
        )

        usage = TokenUsage(
            prompt_tokens=data.get(
                "prompt_eval_count",
                0,
            ),
            completion_tokens=data.get(
                "eval_count",
                0,
            ),
            total_tokens=(
                data.get("prompt_eval_count", 0)
                + data.get("eval_count", 0)
            ),
        )

        return LLMResponse(
            content=content,
            model=data.get(
                "model",
                request.model or "",
            ),
            messages=(assistant_message,),
            finish_reason=self._map_finish_reason(data),
            usage=usage,
            request_id=request.request_id,
            provider=self.name,
            metadata={
                "done": data.get("done"),
                "total_duration_ns": data.get(
                    "total_duration"
                ),
                "load_duration_ns": data.get(
                    "load_duration"
                ),
                "prompt_eval_duration_ns": data.get(
                    "prompt_eval_duration"
                ),
                "eval_duration_ns": data.get(
                    "eval_duration"
                ),
            },
        )

    def _build_stream_response(
        self,
        request: LLMRequest,
        data: dict[str, Any],
    ) -> LLMResponse:
        message_data = data.get("message", {})

        content = message_data.get("content", "")

        assistant_message = Message(
            role="assistant",
            content=content,
        )

        return LLMResponse(
            content=content,
            model=data.get(
                "model",
                request.model or "",
            ),
            messages=(assistant_message,),
            finish_reason=self._map_finish_reason(data),
            request_id=request.request_id,
            provider=self.name,
            metadata={
                "done": data.get("done"),
            },
        )

    @staticmethod
    def _map_finish_reason(
        data: dict[str, Any],
    ) -> str | None:
        if data.get("done"):
            return "stop"

        return None