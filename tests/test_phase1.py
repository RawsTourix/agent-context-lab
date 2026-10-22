import json
from pathlib import Path

import pytest

from agent_context_lab.cli import main
from agent_context_lab.context import BudgetInfeasible, FullContextPolicy, canonical_json
from agent_context_lab.contracts import Message, ToolCall
from agent_context_lab.experiment import run_demo
from agent_context_lab.storage import load_bundle


def test_demo_produces_replayable_run(tmp_path: Path):
    directory = run_demo(tmp_path, attempt_id="attempt-001")
    record = load_bundle(directory)
    assert record["result"]["status"] == "success"
    assert record["result"]["evaluation"]["success"] is True
    assert record["result"]["cortex"]["model_calls"] == 2
    assert record["result"]["cortex"]["tool_calls"] == 1
    assert len(record["projections"]) == 2
    assert len(record["model_calls"]) == 2
    assert all(x["schema_version"] == 1 for x in record["events"])
    events = record["events"]
    assert [e["sequence_number"] for e in events] == list(range(1, len(events) + 1))
    assert events[-1]["event_type"] == "run_finished"
    assert record["projections"][1]["ordered_message_ids"] == [
        "system-001", "user-001", "assistant-1", "tool-1-0"
    ]
    assert record["projections"][1]["ordered_messages"][3]["tool_call_id"] == "tool-001"


def test_append_only_run_never_overwrites(tmp_path: Path):
    run_demo(tmp_path, attempt_id="same-id")
    with pytest.raises(FileExistsError):
        run_demo(tmp_path, attempt_id="same-id")


def test_budget_failure_is_persisted(tmp_path: Path):
    with pytest.raises(BudgetInfeasible):
        run_demo(tmp_path, budget_tokens=1, attempt_id="small-budget")
    record = load_bundle(tmp_path / "demo-v1" / "case-001-full-v1" / "small-budget")
    assert record["result"]["status"] == "budget_infeasible"
    assert record["events"][-1]["event_type"] == "run_failed"


def test_cli_invocation_and_list(tmp_path: Path, capsys):
    assert main(["--runs-dir", str(tmp_path), "demo"]) == 0
    assert main(["--runs-dir", str(tmp_path), "list"]) == 0
    assert "success" in capsys.readouterr().out


def test_projection_does_not_truncate_or_reorder():
    messages = [Message("z", "user", "first"), Message("a", "assistant", "second")]
    p = FullContextPolicy().build(messages, call_id="c", budget_tokens=200)
    assert tuple(m.message_id for m in p.ordered_messages) == ("z", "a")
    with pytest.raises(BudgetInfeasible):
        FullContextPolicy().build(messages, call_id="c", budget_tokens=1)


def test_message_structural_invariants():
    with pytest.raises(ValueError):
        Message("x", "user", "", tool_calls=(ToolCall("id", "foo", {}),))
    with pytest.raises(ValueError):
        Message("x", "tool", "foo")


def test_schema_rejection(tmp_path: Path):
    directory = run_demo(tmp_path, attempt_id="schema")
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["schema_version"] = 999
    manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported schema_version"):
        load_bundle(directory)


def test_identifier_traversal_rejected(tmp_path: Path):
    from agent_context_lab.storage import RunBundle
    with pytest.raises(ValueError):
        RunBundle.create(tmp_path, {"experiment_id": "../other", "trial_id": "t", "attempt_id": "a"})


def test_verify_bundle_and_detect_tamper(tmp_path: Path):
    from agent_context_lab.storage import verify_bundle
    directory = run_demo(tmp_path, attempt_id="verified")
    assert verify_bundle(directory) == {"verified": True, "events": 16,
                                       "projections": 2, "model_calls": 2, "complete": True}
    projections = directory / "projections.jsonl"
    lines = projections.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["ordered_messages"][0]["content"] = "modified"
    lines[0] = canonical_json(first)
    projections.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_bundle(directory)
