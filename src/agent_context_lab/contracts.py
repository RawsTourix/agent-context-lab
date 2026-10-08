"""Provider-neutral, immutable request and response value objects."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Role = Literal["system", "user", "assistant", "tool"]


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Message:
    message_id: str
    role: Role
    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    tool_call_id: str | None = None

    def __post_init__(self) -> None:
        if self.tool_calls and self.role != "assistant":
            raise ValueError("Only assistant messages can contain tool calls")
        if self.tool_call_id and self.role != "tool":
            raise ValueError("Only tool messages can have tool_call_id")
        if self.role == "tool" and not self.tool_call_id:
            raise ValueError("Tool observations require tool_call_id")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Usage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    source: str = "unavailable"


@dataclass(frozen=True)
class ModelResponse:
    text: str = ""
    tool_calls: tuple[ToolCall, ...] = ()
    usage: Usage = field(default_factory=Usage)
    finish_reason: str = "stop"

    def __post_init__(self) -> None:
        if self.tool_calls and self.finish_reason != "tool_calls":
            raise ValueError("tool_calls responses need finish_reason='tool_calls'")
        if not self.tool_calls and self.finish_reason == "tool_calls":
            raise ValueError("tool_calls finish reason requires at least one tool call")
