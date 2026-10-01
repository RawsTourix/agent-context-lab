# Agent Context Lab

**Modular AI agent and research workbench for benchmarking context selection, utility scoring, token budgets, and context-management policies.**

> **Status:** design/research baseline. Implementation has not started yet.

Agent Context Lab is a small, controlled agent environment built for **reproducible experiments with LLM context management**.

The immediate academic use is the optimization-and-system-modeling laboratory sequence, but the repository is deliberately structured so that the benchmark, observability and research tooling remain useful for future agent development.

## Core question

A long-running agent may have much more information available than should be sent to the model on every call.

This project asks:

> **Which information should the model see now, under a limited context/token budget, without causing an unacceptable loss in task quality?**

The first stage studies static selection for one model invocation. Later stages may extend this to dynamic residency with reversible eviction and recall.

## Architecture at a glance

```text
                 Experiment Runner
                        |
                        v
                    Cortex
                        |
              +---------+---------+
              |                   |
              v                   v
        Context Engine        Tool Runtime
              |
       scorer + selector
              |
              v
       ContextProjection
              |
              v
          Model Gateway
              |
              v
              LLM

events / manifests / metrics
              |
              v
          Research Store
              |
              v
      Research Workbench
```

### Cortex

**Cortex** is the stable execution kernel of the experimental agent.

It runs the model/tool loop but intentionally does **not** decide:

- how context usefulness is scored;
- which selection algorithm is used;
- how benchmark quality is evaluated.

That separation lets experiments change one independent variable without silently changing the agent itself.

## Research principles

1. **Quality first.** Fewer tokens are not an improvement if the task result becomes unacceptably worse.
2. **Scorer ≠ selector ≠ evaluator.** Utility estimation, subset optimization and final task evaluation are separate.
3. **Reproducibility.** Every run records model configuration, policy/scorer versions, benchmark case, code/data revision and actual model-facing context.
4. **Provider neutrality.** Provider-native context features may optimize execution but do not define project semantics.
5. **Observable context.** Each model call should have a ContextProjection manifest describing what was available, selected and sent.
6. **Research data are first-class.** Plots and tables are generated from stored experiment data, not assembled manually after the fact.

## Planned research path

Initial static experiment:

```text
available context
→ utility scoring
→ selection under budget
→ model call
→ task result
→ independent evaluation
```

Later temporal extension:

```text
P1 → model call
   → release / evict

P2 → model call
   → missing information
   → recall

P3 → model call
```

Candidate operations for future experiments:

`PIN / RELEASE / EVICT / RECALL / COMPACT`.

The important invariant is:

```text
not resident in the current context != deleted
```

## Documentation

Start here:

- [Documentation map](docs/README.md)
- [Concept baseline](docs/design/CONCEPT.md)
- [Architecture](docs/design/ARCHITECTURE.md)
- [Benchmark protocol](docs/research/BENCHMARK.md)
- [Observability](docs/research/OBSERVABILITY.md)
- [Research Workbench](docs/research/RESEARCH_WORKBENCH.md)
- [Sources and reusable inputs](docs/references/SOURCES.md)
- [Roadmap](docs/roadmap/ROADMAP.md)

For coding agents and contributors:

- [AGENTS.md](AGENTS.md)

## Existing inputs

This project is intentionally informed by — but independent from — three existing workstreams:

- [RawsTourix/internet-search-bot](https://github.com/RawsTourix/internet-search-bot) — practical Gen1 agent/tool loop and real operational traces.
- [5R-AXIS/agent](https://github.com/5r-axis/agent) — architectural research around bounded ContextProjection, source ownership, provenance and dynamic context residency.
- [optimization-and-system-modeling/lab_context](https://github.com/rosbiotech-studies/optimization-and-system-modeling/tree/main/lab_context) — academic problem framing and sanitized real-trace reference material.

External prior art is tracked in [SOURCES.md](docs/references/SOURCES.md).

## Current implementation direction

The first implementation should stay deliberately small:

- Python;
- modular monolith;
- provider-neutral Model Gateway;
- minimal deterministic tool interface;
- DuckDB + Parquet + JSON/JSONL research storage;
- Streamlit + Plotly first Research Workbench;
- full/sliding/greedy/ILP context-selection policies;
- OracleScorer before more complex learned/LLM scorers.

These technology choices are provisional. The experiment semantics and data contracts are more important than any UI or framework.

## Non-goals for v0

Not required:

- production-grade general agent platform;
- vector database;
- autonomous long-term memory;
- multi-agent orchestration;
- distributed runtime;
- full MCP discovery stack;
- consumer chat product;
- hidden chain-of-thought logging.

## License

No project license has been selected yet. Before reusing code from external repositories, verify source-license compatibility and attribution requirements.
