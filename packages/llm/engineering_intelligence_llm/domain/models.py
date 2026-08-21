from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass(frozen=True, slots=True)    
class Message:
    role: MessageRole
    content: str
    name: str | None = None
    tool_call_id: str | None = None

@dataclass(frozen=True, slots=True)
class GenerationParameters:
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    stop: tuple[str, ...] | None = ()

@dataclass(frozen=True, slots=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]

@dataclass(frozen=True, slots=True)
class LLMRequest:
    messages: tuple[Message, ...]
    model: str | None = None
    generation: GenerationParameters = field(default_factory=GenerationParameters)
    tools: tuple[ToolDefinition, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: str | None = None

@dataclass(frozen=True, slots=True)
class TokenUsage:
    prompt_tokens: int=0
    completion_tokens: int=0
    total_tokens: int=0

@dataclass(frozen=True, slots=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]

@dataclass(frozen=True, slots=True)
class LLMResponse:
    content: str
    model: str
    messages: tuple[Message, ...]
    finish_reason: str | None = None
    usage: TokenUsage | None = None
    tool_calls: tuple[ToolCall, ...] = ()
    request_id: str | None = None
    provider: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

        


