"""Agent execution only: context selection and evaluation live outside Cortex."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .context import FullContextPolicy
from .contracts import Message
from .models import ModelGateway
from .storage import RunBundle
from .tools import FixtureTools


@dataclass(frozen=True)
class CortexResult:
    answer: str
    model_calls: int
    tool_calls: int


@dataclass
class Cortex:
    model: ModelGateway
    tools: FixtureTools
    policy: FullContextPolicy
    max_steps: int = 8
    budget_tokens: int = 2048

    def execute(self, initial_messages: Sequence[Message], bundle: RunBundle) -> CortexResult:
        """A fixed model/tool loop; no benchmark-label access or scorer semantics."""
        if self.max_steps < 1:
            raise ValueError("max_steps must be positive")
        messages = list(initial_messages)
        tool_count = 0
        for step in range(1, self.max_steps + 1):
            call_id = f"call-{step:03d}"
            bundle.event("context_candidates_built", call_id=call_id, count=len(messages))
            projection = self.policy.build(messages, call_id=call_id, budget_tokens=self.budget_tokens)
            bundle.event("context_selection_completed", call_id=call_id,
                         selected_count=len(projection.ordered_messages), policy="full-context-v1")
            bundle.append("projections.jsonl", {"call_id": call_id, **projection.to_dict()})
            bundle.event("context_projection_built", call_id=call_id,
                         request_hash=projection.request_hash,
                         estimated_input_tokens=projection.estimated_input_tokens)
            bundle.event("model_call_started", call_id=call_id, model_id=self.model.model_id)
            try:
                response = self.model.complete(projection.ordered_messages)
            except Exception as exc:
                bundle.event("model_call_failed", call_id=call_id,
                             error_type=type(exc).__name__)
                raise
            bundle.append("model_calls.jsonl", {
                "call_id": call_id, "projection_id": projection.projection_id,
                "request_hash": projection.request_hash, "model_id": self.model.model_id,
                "response": asdict(response),
            })
            bundle.event("model_call_finished", call_id=call_id,
                         finish_reason=response.finish_reason, usage=asdict(response.usage))
            if response.tool_calls:
                message = Message(f"assistant-{step}", "assistant", response.text,
                                  tool_calls=response.tool_calls)
                messages.append(message)
                for index, call in enumerate(response.tool_calls):
                    bundle.event("tool_call_started", call_id=call_id, tool_call_id=call.call_id,
                                 tool_name=call.name)
                    try:
                        observation = self.tools.invoke(call)
                    except Exception as exc:
                        bundle.event("tool_call_failed", call_id=call_id,
                                     tool_call_id=call.call_id, error_type=type(exc).__name__)
                        raise
                    messages.append(Message(f"tool-{step}-{index}", "tool", observation,
                                            tool_call_id=call.call_id))
                    tool_count += 1
                    bundle.event("tool_call_finished", call_id=call_id,
                                 tool_call_id=call.call_id)
            else:
                return CortexResult(response.text, step, tool_count)
        raise RuntimeError(f"Cortex exceeded max_steps={self.max_steps}")
