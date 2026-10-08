"""Benchmark runner and evaluator are independent of the Cortex runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import uuid

from . import __version__
from .context import BudgetInfeasible, FullContextPolicy, canonical_json
from .contracts import Message, ModelResponse, ToolCall, Usage
from .cortex import Cortex
from .models import ScriptedModel
from .storage import RunBundle
from .tools import FixtureTools


@dataclass(frozen=True)
class ExactAnswerEvaluator:
    evaluator_id: str = "exact-answer-v1"

    def evaluate(self, actual: str, expected: str) -> dict:
        return {"success": actual == expected, "expected": expected,
                "actual": actual, "evaluator_id": self.evaluator_id}


def demo_script() -> ScriptedModel:
    return ScriptedModel(responses=(
        ModelResponse(tool_calls=(ToolCall("tool-001", "read_fixture", {"key": "answer"}),),
                      usage=Usage(40, 6, "scripted_fixture"), finish_reason="tool_calls"),
        ModelResponse(text="The reference answer is 42.",
                      usage=Usage(56, 8, "scripted_fixture")),
    ))


def run_demo(root: Path, *, budget_tokens: int = 2048,
             attempt_id: str | None = None) -> Path:
    """A deterministic two-turn smoke benchmark with a fresh append-only bundle."""
    experiment_id, trial_id = "demo-v1", "case-001-full-v1"
    attempt_id = attempt_id or f"attempt-{uuid.uuid4().hex[:12]}"
    model = demo_script()
    tools = FixtureTools({"answer": "42"})
    evaluator = ExactAnswerEvaluator()
    bundle = RunBundle.create(root, {
        "experiment_id": experiment_id, "trial_id": trial_id,
        "attempt_id": attempt_id, "benchmark_case_id": "demo-001",
        "dataset_version": "demo-v1", "model_id": model.model_id,
        "policy_id": "full-context-v1", "toolset_version": tools.version,
        "evaluator_id": evaluator.evaluator_id, "budget_tokens": budget_tokens,
        "max_steps": 4, "package_version": __version__,
        "model_configuration": {"type": "scripted", "temperature": None, "seed": None},
        "fixture_ids": ["answer"],
        "fixture_hash": sha256(canonical_json(tools.records).encode("utf-8")).hexdigest(),
        "script_id": "demo-script-v1",
    })
    bundle.event("run_started")
    try:
        initial = (Message("system-001", "system", "Use available tools as needed."),
                   Message("user-001", "user", "What is the reference answer?"))
        outcome = Cortex(model=model, tools=tools, policy=FullContextPolicy(),
                         max_steps=4, budget_tokens=budget_tokens).execute(initial, bundle)
        bundle.event("evaluation_started", evaluator_id=evaluator.evaluator_id)
        evaluation = evaluator.evaluate(outcome.answer, "The reference answer is 42.")
        bundle.event("evaluation_finished", success=evaluation["success"])
        result = {"status": "success" if evaluation["success"] else "task_failure",
                  "evaluation": evaluation, "cortex": asdict(outcome)}
    except Exception as exc:
        status = "budget_infeasible" if isinstance(exc, BudgetInfeasible) else "internal_error"
        result = {"status": status, "error_type": type(exc).__name__, "error": str(exc)}
        bundle.event("run_failed", status=status, error_type=type(exc).__name__)
        bundle.finish(result)
        raise
    bundle.event("run_finished", status=result["status"])
    bundle.finish(result)
    return bundle.directory
