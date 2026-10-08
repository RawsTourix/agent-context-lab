"""Canonical append-only on-disk evidence, separate from analytical indexes."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any
from uuid import uuid4

from . import SCHEMA_VERSION


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass
class RunBundle:
    """Files are created once; event and projection streams are only appended."""

    directory: Path
    experiment_id: str
    trial_id: str
    attempt_id: str
    sequence: int = field(default=0, init=False)
    started_ns: int = field(default_factory=time.monotonic_ns, init=False)

    @classmethod
    def create(cls, root: Path, manifest: dict[str, Any]) -> RunBundle:
        experiment_id = str(manifest["experiment_id"])
        trial_id = str(manifest["trial_id"])
        attempt_id = str(manifest["attempt_id"])
        for identifier in (experiment_id, trial_id, attempt_id):
            if not identifier or not all(c.isalnum() or c in "-_" for c in identifier):
                raise ValueError("Run identifiers must be nonempty, safe path segments")
        directory = root / experiment_id / trial_id / attempt_id
        directory.mkdir(parents=True, exist_ok=False)
        bundle = cls(directory, experiment_id, trial_id, attempt_id)
        bundle._create_json("manifest.json", dict(manifest))
        for name in ("events.jsonl", "projections.jsonl", "model_calls.jsonl"):
            (directory / name).touch(exist_ok=False)
        return bundle

    def _create_json(self, filename: str, data: dict[str, Any]) -> None:
        with (self.directory / filename).open("x", encoding="utf-8") as f:
            f.write(_json({"schema_version": SCHEMA_VERSION, **data}) + "\n")

    def append(self, filename: str, data: dict[str, Any]) -> None:
        if filename not in {"events.jsonl", "projections.jsonl", "model_calls.jsonl"}:
            raise ValueError("Unknown evidence stream")
        with (self.directory / filename).open("a", encoding="utf-8") as f:
            f.write(_json({"schema_version": SCHEMA_VERSION, **data}) + "\n")

    def event(self, event_type: str, **payload: Any) -> None:
        self.sequence += 1
        self.append("events.jsonl", {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp_utc": _utc_now(),
            "monotonic_offset_ns": time.monotonic_ns() - self.started_ns,
            "experiment_id": self.experiment_id,
            "trial_id": self.trial_id,
            "attempt_id": self.attempt_id,
            "sequence_number": self.sequence,
            "payload": payload,
        })

    def finish(self, result: dict[str, Any]) -> None:
        self._create_json("result.json", result)


def load_bundle(directory: Path) -> dict[str, Any]:
    def read_json(path: Path) -> dict[str, Any]:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"Unsupported schema_version in {path.name}")
        return data

    def read_stream(name: str) -> list[dict[str, Any]]:
        records = []
        for line in (directory / name).read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                if record.get("schema_version") != SCHEMA_VERSION:
                    raise ValueError(f"Unsupported schema_version in {name}")
                records.append(record)
        return records

    return {
        "manifest": read_json(directory / "manifest.json"),
        "events": read_stream("events.jsonl"),
        "projections": read_stream("projections.jsonl"),
        "model_calls": read_stream("model_calls.jsonl"),
        "result": read_json(directory / "result.json") if (directory / "result.json").exists() else None,
    }


def verify_bundle(directory: Path) -> dict[str, Any]:
    """Verify the stored projection hashes and the event ordering; never mutate evidence."""
    from .context import canonical_json

    data = load_bundle(directory)
    sequence = [e["sequence_number"] for e in data["events"]]
    if sequence != list(range(1, len(sequence) + 1)):
        raise ValueError("Event sequence is missing, duplicated or out of order")
    seen = set()
    for projection in data["projections"]:
        call_id = projection["call_id"]
        if call_id in seen:
            raise ValueError("Duplicate projection call_id")
        seen.add(call_id)
        payload = canonical_json(projection["ordered_messages"])
        actual_hash = sha256(payload.encode("utf-8")).hexdigest()
        if actual_hash != projection["request_hash"]:
            raise ValueError(f"Projection hash mismatch for {call_id}")
        expected_ids = [m["message_id"] for m in projection["ordered_messages"]]
        if expected_ids != projection["ordered_message_ids"]:
            raise ValueError(f"Projection ordering mismatch for {call_id}")
    for model_call in data["model_calls"]:
        if model_call["call_id"] not in seen:
            raise ValueError("Model call without a recorded projection")
        matching = next(x for x in data["projections"] if x["call_id"] == model_call["call_id"])
        if matching["request_hash"] != model_call["request_hash"]:
            raise ValueError("Model call request hash differs from projection")
    return {"verified": True, "events": len(sequence), "projections": len(seen),
            "model_calls": len(data["model_calls"]), "complete": data["result"] is not None}
