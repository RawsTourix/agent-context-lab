# Phase 1 — Cortex + evidence skeleton

This implementation is the **first deterministic vertical slice**, not an LLM benchmark or an optimization result.

## Run

```bash
uv sync --extra dev
uv run acl demo
uv run acl list
uv run acl verify runs/demo-v1/case-001-full-v1/<attempt-id>
uv run acl show runs/demo-v1/case-001-full-v1/<attempt-id>
uv run pytest
```

Optional research UI:

```bash
uv sync --extra dev --extra workbench
uv run --extra workbench streamlit run src/agent_context_lab/workbench.py
```

The `ScriptedModel` deterministically requests a `read_fixture` tool, receives `42`, then provides the expected answer. Cortex controls only model/tool execution; `ExactAnswerEvaluator` lives outside it.

## Evidence

Each run creates a **new**, non-overwriting directory:

```text
runs/demo-v1/case-001-full-v1/<attempt-id>/
  manifest.json
  events.jsonl
  projections.jsonl
  model_calls.jsonl
  result.json
```

These files are the canonical evidence. They are excluded from Git by `.gitignore`; do not publish them without a separate whitelist-based export review.

`schema_version: 1` is present on every persisted record. The projection manifest includes ordered exact messages, a SHA-256 hash of their canonical JSON representation, and an explicitly rough token estimate (`utf8-bytes-div4-ceil-v1`). **This is not actual model token usage.** The scripted model's usage is marked `scripted_fixture`, not provider-reported.

## Boundaries and current limitations

- No production LLM integration, MCP, scorer, ILP or dynamic context residency in Phase 1.
- `FullContextPolicy` raises if its estimated full input exceeds the declared experimental budget; it never truncates silently.
- The fake provider does not validate full third-party API semantics.
- No promise of bitwise replay with future remote LLM providers.
- The demo stores exact model-facing messages **locally** for debugging/replay; real/private data should remain under ignored `runs/`.
- DuckDB/Parquet are deferred because there is no substantial dataset yet; the Streamlit viewer reads immutable run files directly.

Run `uv run acl verify <run-path>` to check event sequencing, message order and per-call SHA-256 hashes. This validates stored evidence consistency, not the truth or quality of any LLM answer.

**Lockfile status:** GitHub Actions generated `uv.lock` as [phase1-uv-lock artifact](https://github.com/RawsTourix/agent-context-lab/actions/runs/37762753540). The extracted file passed `uv lock --check --offline` locally. It still needs to be committed at the repository root; until then the checked-in tree is not fully dependency-reproducible. No fabricated lockfile is included.
