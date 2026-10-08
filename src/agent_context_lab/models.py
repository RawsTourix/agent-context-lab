"""Scripted test-model adapter behind the future provider gateway boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence

from .contracts import Message, ModelResponse


class ModelGateway(Protocol):
    model_id: str

    def complete(self, messages: Sequence[Message]) -> ModelResponse: ...


@dataclass
class ScriptedModel:
    """Deterministic scripted turns. Not a real LLM or an evaluation baseline."""

    responses: tuple[ModelResponse, ...]
    model_id: str = "scripted-model-v1"
    calls: list[tuple[Message, ...]] = field(default_factory=list, init=False)

    def complete(self, messages: Sequence[Message]) -> ModelResponse:
        index = len(self.calls)
        if index >= len(self.responses):
            raise RuntimeError("ScriptedModel exhausted: unexpected extra model call")
        if not messages:
            raise ValueError("Model input may not be empty")
        self.calls.append(tuple(messages))
        return self.responses[index]
