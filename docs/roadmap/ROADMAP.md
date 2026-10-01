# Roadmap

The order is intentionally research-first.

## Phase 0 — documentation baseline

Deliverables:

- project concept;
- component ownership;
- benchmark protocol;
- observability schema;
- workbench concept;
- source registry.

Exit criterion:

> A developer can explain what changes between experiments and what must remain fixed without reading chat history.

## Phase 1 — Cortex skeleton

Build:

- minimal run lifecycle;
- provider-neutral Model Gateway;
- tiny deterministic tool interface;
- structured events;
- run manifest;
- no context optimization yet.

Policy:

- FullContextPolicy only.

Exit criterion:

> One benchmark case runs end-to-end and produces a complete reproducible trace.

## Phase 2 — static context-selection harness

Build:

- ContextElement representation;
- token counting;
- mandatory/optional classification;
- SelectionPolicy interface;
- OracleScorer;
- synthetic controlled benchmark cases.

Policies:

- full;
- sliding;
- greedy utility;
- greedy utility/token;
- ILP.

Exit criterion:

> The same case can be replayed across policies while Cortex/model/tool configuration is fixed.

## Phase 3 — optimization/scalability experiments

Build:

- deterministic large-N generator;
- ILP solver integration;
- solver diagnostics;
- plots for N / constraints / solve time.

Exit criterion:

> The mathematical model is tested well beyond the small classroom example without requiring LLM calls.

## Phase 4 — scorer research

Add:

- heuristic scorer;
- embedding scorer;
- LLM scorer;
- calibration/comparison against oracle labels.

Exit criterion:

> Scorer error can be distinguished from selector error.

## Phase 5 — Research Workbench

Build first usable researcher UI:

- experiment launch;
- live telemetry;
- runs table;
- Context Inspector;
- policy/scorer comparisons;
- automatic plots;
- CSV/XLSX/Parquet/JSON exports;
- interesting-run annotations.

Exit criterion:

> A researcher can reproduce a plot from stored run data without manually assembling spreadsheets.

## Phase 6 — realistic workloads

Add:

- sanitized/imported trace-derived scenarios;
- file-package analysis;
- multi-step tool tasks;
- structured output evaluation.

Exit criterion:

> Static selection is tested on workloads that resemble real agent activity, not only synthetic relevance puzzles.

## Phase 7 — dynamic residency research

Add experimentally:

- stable source refs;
- RELEASE / EVICT / RECALL;
- optional PIN/prefer;
- residency/churn/recall metrics;
- exact-source recall;
- derived representation lineage.

Exit criterion:

> The system can keep context bounded across a multi-call task while recovering information that is no longer resident.

## Phase 8 — 5R-AXIS feedback

Only after reproducible evidence exists:

- compare Agent Context Lab findings with 5R-AXIS Context Engine research;
- export benchmark methodology/results;
- propose design changes upstream as evidence, not assumptions.

The lab is allowed to remain simpler than 5R-AXIS indefinitely.
