# Development baseline

**Status:** approved environment baseline (MIT, Python 3.11+, uv). Other choices are implementation proposals.

This document narrows the first implementation enough that development can start without turning provisional technology choices into project semantics.

## 1. Runtime

Accepted baseline:

- MIT license;
- Python 3.11+;
- `pyproject.toml` as package/project definition;
- `uv` for environment resolution and a committed lockfile;
- `pytest` for tests;
- `ruff` for lint/format;
- static typing with `mypy` or an equivalent checker.

Python 3.11 keeps compatibility with the existing development/VPS environment and current research dependencies while avoiding a needless 3.12-only requirement.

## 2. Suggested package layout

```text
src/agent_context_lab/
├── cortex/
├── context/
│   ├── elements/
│   ├── scoring/
│   ├── selection/
│   └── projection/
├── models/
├── tools/
├── benchmark/
├── evaluation/
├── observability/
├── storage/
└── workbench/
```

This is a starting layout, not a domain model.

The architectural ownership in `ARCHITECTURE.md` matters more than the exact folder names.

## 3. Schema/data layer

Recommended:

- Pydantic v2 for versioned external/config/event schemas;
- immutable/frozen value objects where practical;
- explicit `schema_version` on persisted records;
- UUID/ULID-like stable ids for experiment/run/call/event identities;
- SHA-256 content hashes for immutable dataset/source revisions where useful.

Avoid using Python object serialization/pickle as the durable research format.

## 4. Research storage

Initial implementation:

```text
append-only local RunBundle
        |
        +--> JSON / JSONL manifests and events
        +--> artifacts
        |
        v
derived loader/index
        |
        +--> DuckDB
        +--> Parquet
        |
        v
Research Workbench / notebooks / exports
```

The append-only RunBundle is canonical experiment evidence.

DuckDB is a rebuildable analytical index/cache, not the only copy of the result.

## 5. Workbench

Initial UI direction:

- Streamlit;
- Plotly;
- DuckDB queries;
- read-only views first.

The first UI should exist early enough to inspect Phase-1 traces. It does not need experiment editing or polished dashboards immediately.

First useful views:

- run list;
- trajectory/timeline;
- model-call detail;
- ContextProjection inspector;
- basic token/latency plot.

## 6. Optimization solver

Preferred v0 candidate for the laboratory ILP implementation:

- `scipy.optimize.milp`, backed by HiGHS.

Reasons:

- small dependency surface;
- direct mixed-integer linear programming interface;
- exposes MIP diagnostics such as node count/gap;
- HiGHS is open-source;
- easy to use for deterministic large-N synthetic experiments.

The solver remains behind `ILPPolicy`.

Persist:

- SciPy version;
- HiGHS/solver version when available;
- solver options;
- time limit/gap settings;
- thread settings where configurable.

Do not encode SciPy-specific objects into benchmark contracts.

## 7. Model/provider access

Use a project-owned `ModelGateway` protocol.

### Deterministic adapter first

Phase 1 should start with a `ScriptedModel` / `FakeModel` adapter that returns a predefined sequence such as:

```text
model turn 1 → deterministic tool request
tool fixture  → deterministic observation
model turn 2 → deterministic final answer
```

Purpose:

- test Cortex/model-tool control flow without network/provider noise;
- validate event ordering and Run Bundle replay;
- make the first regression suite free and deterministic;
- verify the Workbench before any real API cost exists.

This adapter is test infrastructure, not a benchmark policy.

### Real provider adapter second

After the deterministic vertical slice works, add one real provider adapter behind the same interface.

An OpenAI-compatible transport is a reasonable first interoperability target, but the exact provider is **not a Phase-1 architecture blocker**.

Provider SDKs may sit behind adapters.

Do not make a third-party agent framework the Cortex.

The minimum response contract should preserve:

- model output;
- tool requests;
- finish/status reason;
- usage metadata;
- provider request id if available;
- model identifier/revision metadata when available;
- retry/error information.

## 8. Tools

Start with deterministic local tools.

Candidate v0 set:

- read a known text/file artifact;
- search within a fixture corpus;
- retrieve a named fixture record.

MCP is a later adapter.

This keeps early benchmark outcomes reproducible and avoids debugging network variability while testing context selection.

## 9. Privacy and local data

Default repository behavior:

- `runs/`, local databases and provider payload captures are gitignored;
- committed benchmark fixtures contain only public/synthetic/sanitized data;
- secrets come from environment/local config, never committed files;
- public export is whitelist-based rather than "copy raw run and redact a few fields".

A local research mode may retain model-visible content for inspection, but public exports must be a separate sanitized artifact.

## 10. Reuse policy

`internet-search-bot` is MIT-licensed and may be reused with attribution/license compliance.

Prefer reimplementing the small generic contracts first; only copy/adapt code when it clearly saves work.

5R-AXIS currently serves as conceptual/design input. Do not copy private/unlicensed implementation into the public repository unless an explicit licensing decision makes that reuse valid.

## 11. Phase 1 implementation defaults

Decisions accepted by the project owner: **MIT**, **Python 3.11+**, **uv**.

Defaults for the first implementation PR:

- start with ScriptedModel; real model provider selection is deferred;
- store local evidence under `runs/` (gitignored), keep exported databases/artifacts out of Git;
- include explicit `schema_version: 1` in persisted JSON/JSONL records; reject unknown major schema versions rather than guessing;
- create `pyproject.toml` and a lockfile using `uv` when the toolchain is available.

Any later schema migration should be explicit and tested. No further architecture decision blocks starting Phase 1.
