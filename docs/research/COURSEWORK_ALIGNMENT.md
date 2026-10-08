# Coursework alignment

**Status:** working research-to-course map, not a replacement for the teacher's official assignment.

Agent Context Lab is intentionally broader than the laboratory reports. The course should consume reproducible results from the lab rather than dictate the whole software architecture.

## Laboratory work 1 — subject domain and optimization problem

Project contribution:

- defines the multi-step LLM-agent context problem;
- distinguishes available information from model-facing context;
- establishes that context reduction is not useful if task quality collapses.

No implementation is required to justify the subject domain.

## Laboratory work 2 — mathematical formulation

Static one-call selection becomes the first formal model.

For optional context elements:

```text
x_i in {0, 1}
s_i = estimated token/resource cost under the declared elementization/tokenizer basis
v_i = estimated utility proxy
B   = optional-context budget
```

Base formulation:

```text
maximize sum(v_i * x_i)
subject to sum(s_i * x_i) <= B
```

Mandatory context is preferably reserved before optional selection in the simplest model.

The classroom example can use a small N while the formulation remains valid for arbitrary N.

Important interpretation:

- (s_i) is a controlled additive estimate for the mathematical model; actual serialized input is measured separately;
- (v_i) is a surrogate utility estimate, not measured final task quality;
- the additive objective is a base assumption, not a claim that real context elements never interact.

These limitations belong in the project methodology even if the classroom write-up keeps the base model compact.

## Laboratory work 3 — method and computational applicability

Project contribution:

- ILPPolicy implementation;
- comparison with simple baselines;
- separate large-N deterministic generator;
- solver status/time/objective/gap diagnostics;
- hardware/solver version capture for performance claims.

This allows testing scalability without paying for LLM calls.

## Laboratory work 4 — experimental data

Project contribution:

- benchmark cases;
- trace-derived workload design;
- ContextProjection manifests;
- token/latency/tool-event measurements;
- append-only Run Bundles;
- reproducible ExperimentSpec/TrialSpec/RunAttempt hierarchy.

Real `internet-search-bot` traces are empirical references, not automatically benchmark ground truth.

## Laboratory work 5 — parameter identification

Central question:

> How is utility (v_i) obtained?

Project contribution:

- OracleScorer for controlled cases;
- deterministic heuristic scorer;
- embedding scorer;
- LLM scorer;
- comparison/calibration against known relevance where available;
- explicit measurement of scorer overhead.

This stage must preserve the distinction between estimated utility and final task quality.

If scorer prompts/thresholds are tuned, development and final-test cases must be separated.

## Laboratory work 6 — software implementation

Project contribution:

- Cortex;
- Context Engine;
- Model Gateway;
- deterministic tool runtime;
- scorers;
- selection policies;
- Experiment Runner;
- append-only observability;
- Research Store;
- Research Workbench.

The implementation should remain minimal enough that the experiment stays understandable.

## Laboratory work 7 — experiment and results

Project contribution:

- controlled policy/scorer/budget comparisons;
- task-quality evaluation;
- target-model and context-management overhead;
- token/cost/latency metrics;
- Pareto analysis;
- failure/critical-omission analysis;
- confidence intervals/effect sizes where appropriate;
- automatic plots/tables/exports.

The main empirical question is not "how many tokens were removed?" but:

> How much context/system cost can be reduced before task quality degrades beyond a predeclared acceptable threshold?

Position/order and element granularity are controlled factors so they do not silently invalidate the comparison.

## Beyond the laboratory sequence

If static selection results are solid, Agent Context Lab can extend to dynamic context residency:

- PIN / prefer;
- RELEASE;
- EVICT;
- RECALL;
- COMPACT;
- residency/churn/recall metrics;
- representation/lineage experiments.

This extension connects naturally to 5R-AXIS Context Residency Management research without making 5R-AXIS implementation a prerequisite for completing the course.
