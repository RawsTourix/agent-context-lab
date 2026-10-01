# Documentation map

This repository is documentation-first: architecture, experiment semantics and reproducibility rules are fixed before the implementation becomes large enough to hide design mistakes.

## Design

- [CONCEPT.md](design/CONCEPT.md) — research problem, hypotheses, terminology and project boundaries.
- [ARCHITECTURE.md](design/ARCHITECTURE.md) — component ownership, Cortex, Context Engine and the three-plane architecture.

## Research

- [BENCHMARK.md](research/BENCHMARK.md) — benchmark cases, baselines, scorers, selection policies, metrics and experiment protocol.
- [OBSERVABILITY.md](research/OBSERVABILITY.md) — trace/event model, ContextProjection manifests and reproducibility data.
- [RESEARCH_WORKBENCH.md](research/RESEARCH_WORKBENCH.md) — researcher-facing UI, plots, tables, exports and data storage.

## References

- [SOURCES.md](references/SOURCES.md) — project-local and external sources, with notes on what is reusable and what is only conceptual input.

## Planning

- [ROADMAP.md](roadmap/ROADMAP.md) — implementation sequence and acceptance criteria.

## Source-of-truth rule

The documents above describe the intended research harness. Code must not silently redefine their semantics.

If implementation evidence shows that a documented assumption is wrong, update the relevant document explicitly and record the reason rather than adding an undocumented workaround.
