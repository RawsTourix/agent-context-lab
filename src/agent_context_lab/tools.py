"""Tiny fixture-backed tool runtime: no file-system or network side effects."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import ToolCall


@dataclass(frozen=True)
class FixtureTools:
    records: dict[str, str]
    version: str = "fixture-tools-v1"

    def invoke(self, call: ToolCall) -> str:
        if call.name != "read_fixture":
            raise ValueError(f"Unsupported tool: {call.name}")
        key = call.arguments.get("key")
        if not isinstance(key, str) or key not in self.records:
            raise ValueError("Fixture key does not exist")
        return self.records[key]
