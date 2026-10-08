# Roadmap

The order is intentionally research-first.

## Phase 0 — documentation and development baseline

Deliverables:

- project concept;
- explicit mathematical-model assumptions;
- component ownership;
- benchmark protocol;
- experiment/statistical protocol;
- observability schema;
- workbench concept;
- source registry;
- development baseline.

Accepted for Phase 1:

- MIT;
- Python 3.11+ and `uv`;
- scripted deterministic model adapter first;
- ignored `runs/` for local raw evidence;
- persisted JSON records carry `schema_version: 1`.

Exit criterion:

> A developer can explain what changes between experiments, what must remain fixed, what evidence is persisted, and what the base mathematical model assumes without reading chat history.

## Phase 1 — Cortex + evidence skeleton

Build:

- package scaffold;
- minimal run lifecycle;
- provider-neutral Model Gateway;
- deterministic ScriptedModel/FakeModel adapter;
- tiny deterministic fixture-backed tool interface;
- ExperimentSpec / TrialSpec / RunAttempt ids;
- append-only structured events;
- RunManifest / Run Bundle;
- no context optimization yet.

Policy:

- FullContextPolicy only on cases where it is feasible.

Also build a **minimal read-only Workbench** early:

- runs table;
- trajectory/timeline;
- model-call detail;
- raw token/latency charts.

Exit criterion:

> One fully deterministic scripted-model benchmark case runs end-to-end, produces an append-only replayable trace, and can be inspected in the Workbench without any external model API.

## Phase 2 — static context-selection harness

Build:

- ContextElement representation;
- versioned ElementizationPolicy;
- token estimation + serializer accounting;
- mandatory/optional classification;
- fixed OrderingPolicy;
- SelectionPolicy interface;
- OracleScorer;
- synthetic controlled benchmark cases.

Policies:

- full (when feasible);
- sliding;
- greedy utility;
- greedy utility/token;
- ILP.

Exit criterion:

> The same case can be replayed across policies while Cortex, model, tools, elementization, representation, ordering and evaluator are fixed.

## Phase 3 — optimization/scalability experiments

Build:

- deterministic large-N generator;
- ILP solver integration;
- solver diagnostics;
- version/hardware capture;
- plots for N / constraints / solve time.

Add synthetic cases that test:

- simple additive relevance;
- redundancy;
- prerequisites/complementarity;
- additional constraints.

Exit criterion:

> The base mathematical model is tested well beyond the small classroom example, and its simplifying assumptions are empirically visible rather than hidden.

## Phase 4 — scorer research

Add:

- heuristic scorer;
- embedding scorer;
- LLM scorer;
- scorer cost/latency accounting;
- calibration/comparison against oracle labels;
- development/test split enforcement.

Exit criterion:

> Scorer error can be distinguished from selector error and scorer overhead is included in total system cost.

## Phase 5 — Workbench expansion + experiment analysis

Expand the researcher UI:

- experiment launch/sweep expansion;
- Context Inspector;
- Invocation Inspector;
- paired comparison views;
- confidence intervals/effect sizes;
- Pareto plots;
- automatic tables/plots;
- CSV/XLSX/Parquet/JSON exports;
- append-only interesting-run annotations;
- sanitized public export flow.

Exit criterion:

> A researcher can inspect an anomalous point back to the exact projection/trajectory and reproduce every plot from stored run data without manually assembling spreadsheets.

## Phase 6 — realistic workloads

Add:

- sanitized/imported trace-derived scenarios;
- file/package analysis;
- multi-step fixture-backed tool tasks;
- structured output evaluation;
- position/order stress cases;
- optional external benchmark adapters after license/method review.

Exit criterion:

> Static selection is tested on workloads that resemble real agent activity, not only synthetic relevance puzzles.

## Phase 7 — representation/compression research

Before full temporal residency, compare selection with alternative representations:

- raw;
- extractive;
- summary/digest;
- structured extraction;
- selective no-context where appropriate.

Possible external comparison ideas:

- LLMLingua / LongLLMLingua;
- RECOMP;
- ACON-style compression.

Exit criterion:

> Selection and representation compression are measured as distinct treatment factors.

## Phase 8 — dynamic residency research

Add experimentally:

- stable source refs;
- RELEASE / EVICT / RECALL;
- optional PIN/prefer;
- residency/churn/recall metrics;
- exact-source recall;
- derived representation lineage;
- fault/thrashing analysis.

Exit criterion:

> The system can keep context bounded across a multi-call task while recovering information that is no longer resident and preserving exact provenance.

## Phase 9 — 5R-AXIS feedback

Only after reproducible evidence exists:

- compare Agent Context Lab findings with 5R-AXIS Context Engine research;
- export benchmark methodology/results;
- propose design changes upstream as evidence, not assumptions.

The lab is allowed to remain simpler than 5R-AXIS indefinitely.

## Parallel watch tracks

These may be researched without blocking the main path:

- cache-aware context economics;
- ordering/position optimization;
- tool-schema selection;
- provider-native context editing;
- external eval-harness adapters (Inspect AI, MLflow/OpenTelemetry export);
- self-evolving context policies.

A watch track enters the implementation roadmap only when a concrete benchmark question justifies it.
