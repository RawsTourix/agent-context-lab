# Documentation map

This repository is documentation-first: architecture, experiment semantics and reproducibility rules are fixed before the implementation becomes large enough to hide design mistakes.

## Design

- [CONCEPT.md](design/CONCEPT.md) — research problem, hypotheses, terminology, mathematical assumptions and project boundaries.
- [ARCHITECTURE.md](design/ARCHITECTURE.md) — component ownership, Cortex, Context Engine, experiment identity and evidence flow.
- [DEVELOPMENT_BASELINE.md](design/DEVELOPMENT_BASELINE.md) — proposed Python/tooling/storage/solver baseline before Phase 1 code.

## Research

- [BENCHMARK.md](research/BENCHMARK.md) — benchmark cases, baselines, scorers, selection policies, metrics and workload families.
- [EXPERIMENT_DESIGN.md](research/EXPERIMENT_DESIGN.md) — paired comparisons, repetitions, dev/test separation, quality floors and uncertainty reporting.
- [OBSERVABILITY.md](research/OBSERVABILITY.md) — append-only run evidence, event model, ContextProjection manifests and replay/privacy rules.
- [RESEARCH_WORKBENCH.md](research/RESEARCH_WORKBENCH.md) — researcher-facing UI, trajectory/context inspection, plots, tables, annotations and exports.
- [COURSEWORK_ALIGNMENT.md](research/COURSEWORK_ALIGNMENT.md) — how the same research harness supports laboratory works 1–7 without becoming course-specific runtime code.

## References

- [SOURCES.md](references/SOURCES.md) — project-local and external sources, evidence strength, reuse notes and scientific prior art.

## Planning

- [ROADMAP.md](roadmap/ROADMAP.md) — implementation sequence and acceptance criteria.

## Source-of-truth rule

The documents above describe the intended research harness. Code must not silently redefine their semantics.

If implementation evidence shows that a documented assumption is wrong, update the relevant document explicitly and record the reason rather than adding an undocumented workaround.
