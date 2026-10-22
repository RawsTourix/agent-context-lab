"""Phase-1 full-context projection, with explicit approximate accounting."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Sequence

from .contracts import Message

ESTIMATOR_ID = "utf8-bytes-div4-ceil-v1"
SERIALIZER_ID = "canonical-json-v1"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def estimated_tokens(payload: str) -> int:
    """Explicitly rough estimator. Never a provider-reported or exact token count."""
    return (len(payload.encode("utf-8")) + 3) // 4


class BudgetInfeasible(Exception):
    """Full input cannot fit the declared experimental *estimated* budget."""


@dataclass(frozen=True)
class ContextProjection:
    projection_id: str
    ordered_messages: tuple[Message, ...]
    request_hash: str
    estimated_input_tokens: int
    budget_tokens: int

    def to_dict(self) -> dict:
        return {
            "projection_id": self.projection_id,
            "ordered_message_ids": [m.message_id for m in self.ordered_messages],
            "ordered_messages": [m.to_dict() for m in self.ordered_messages],
            "request_hash": self.request_hash,
            "estimated_input_tokens": self.estimated_input_tokens,
            "token_estimator": ESTIMATOR_ID,
            "serializer": SERIALIZER_ID,
            "budget_tokens": self.budget_tokens,
            "selection_policy": "full-context-v1",
        }


@dataclass(frozen=True)
class FullContextPolicy:
    """Includes everything; no implicit truncation or reordering."""

    def build(self, messages: Sequence[Message], *, call_id: str, budget_tokens: int) -> ContextProjection:
        if budget_tokens <= 0:
            raise ValueError("budget_tokens must be positive")
        ordered = tuple(messages)
        payload = canonical_json([asdict(m) for m in ordered])
        count = estimated_tokens(payload)
        if count > budget_tokens:
            raise BudgetInfeasible(f"Full context estimate {count} exceeds budget {budget_tokens}")
        return ContextProjection(
            projection_id=f"{call_id}-projection",
            ordered_messages=ordered,
            request_hash=sha256(payload.encode("utf-8")).hexdigest(),
            estimated_input_tokens=count,
            budget_tokens=budget_tokens,
        )
