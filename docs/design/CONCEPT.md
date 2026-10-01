# Agent Context Lab — concept baseline

**Status:** design/research baseline  
**Implementation:** not started  
**Primary use:** laboratory work in optimization and system modeling, with a deliberate path toward reusable agent research infrastructure.

## 1. Problem

A multi-step LLM agent can accumulate more potentially useful information than should be placed into every model invocation.

Available information may include:

- current user request and constraints;
- conversation messages;
- tool calls and tool results;
- file/document/code fragments;
- task state and intermediate findings;
- derived summaries or structured extractions;
- externally stored information that can be recalled.

The project studies how to decide **what the model should see now** without treating context reduction as a goal by itself.

Core principle:

> Context optimization is successful only when resource savings do not cause an unacceptable loss in task quality.

## 2. Research question

For a model call with a finite context/token budget:

> Which available context elements should be included so that the agent preserves the information most useful for the current task while avoiding unnecessary context cost?

The first formal problem is static selection for one model call.

Later work may extend this to a temporal residency problem across many calls:

- retain/prefer useful information;
- release information that no longer needs preferred residency;
- evict optional material from later projections without deleting the source;
- recall exact source material when needed again.

## 3. Research hypotheses

The initial project should make these hypotheses testable rather than assume they are true.

### H1 — bounded selection can reduce context cost without unacceptable quality loss

A well-chosen subset of available context can use fewer input tokens than a full-context baseline while preserving comparable task outcome quality.

### H2 — scoring quality and selection quality are separable

Two different sources of error must be measured separately:

1. **Scorer error:** wrong estimate of a context element's usefulness.
2. **Selector error:** suboptimal subset selection given the scores and constraints.

This is why the benchmark includes an oracle/ground-truth scorer for controlled cases.

### H3 — the best policy depends on workload and budget

No single policy should be assumed universally optimal. Full-history, sliding-window, greedy, optimization-based and later dynamic-residency policies must be compared under the same agent runtime.

### H4 — dynamic residency may outperform one-shot reduction on long tasks

For long-horizon workloads, reversible eviction and recall may allow a smaller working set while preserving access to exact source information.

This is a future extension, not a requirement for the first prototype.

## 4. Cortex

**Cortex** is a project-local name for the stable agent execution kernel.

Cortex owns only the generic runtime loop:

- receive task/run input;
- request a model-facing context;
- call the model;
- dispatch tool calls;
- feed tool outcomes back into the run;
- maintain the minimal runtime state required to continue;
- terminate with a result/status.

Cortex must **not** own:

- utility scoring;
- context selection policy;
- benchmark definitions;
- evaluation criteria;
- research dashboards;
- durable long-term memory;
- 5R-AXIS canonical semantics.

Reason: in a controlled experiment, the agent runtime should stay fixed while the independent variable changes.

## 5. Context terminology

### Context element

A separately addressable candidate that may be included in a model call.

Examples: message, tool result, file region, structured state item, summary, finding.

The implementation may later call this type `ContextUnit`, but the exact code name is not yet canonical.

### Available context

All information the runtime is allowed to consider for the current call.

### Mandatory context

Information that must be included for correctness/policy/runtime reasons. It is not competing with optional candidates in the simplest optimization model; its token cost can be reserved before optional selection.

### ContextProjection

The immutable model-facing context assembled for one particular model invocation.

This term is intentionally compatible with 5R-AXIS research, but Agent Context Lab remains an independent experimental project.

### Utility score

A pre-selection estimate of how useful an optional context element is for the current task/call.

It is **not** the same thing as measured final task quality.

## 6. Quality-first objective

The project must never report "fewer tokens" as sufficient evidence of improvement.

At minimum, every benchmark comparison should pair resource metrics with outcome metrics:

- task success / quality;
- critical omission rate;
- input tokens;
- total tokens/cost where available;
- latency.

The important research surface is the trade-off between quality and resource use.

## 7. Scope

### In scope

- minimal modular LLM agent runtime;
- provider-neutral model gateway;
- deterministic/reproducible benchmark cases;
- context element extraction and token accounting;
- utility scorers;
- full/sliding/greedy/ILP selection policies;
- evaluator independent from scorer;
- traces and ContextProjection manifests;
- research data store;
- automatic tables/plots/comparisons/exports;
- later: PIN / RELEASE / EVICT / RECALL experiments.

### Out of scope for v0

- general-purpose production agent platform;
- autonomous long-term learning;
- full durable memory subsystem;
- vector database unless justified by a concrete scorer;
- distributed execution;
- complex multi-agent orchestration;
- consumer chat UI;
- hidden chain-of-thought collection;
- provider-specific context semantics as project truth.

## 8. Relationship to other projects

Agent Context Lab is intentionally between two existing code/research bases:

- **internet-search-bot** provides real-world agent-loop and tool-use experience plus empirical traces.
- **5R-AXIS** provides stronger architectural ideas around bounded model-facing projections, source ownership, reversible residency and provenance.

The lab must reuse ideas and selected implementation patterns, not copy either architecture wholesale.
