# Architecture baseline

## 1. Design goal

Keep the **agent under test** stable while context-management strategies are exchanged around it.

The architecture is split into three planes.

```text
EXPERIMENT PLANE

Benchmark Case
      |
Experiment Runner
      |
      v
=================================

AGENT PLANE

    Cortex
      |
      +------> Tool Runtime
      |
      v
Context Engine
      |
      +--> Scorer
      +--> SelectionPolicy
      |
      v
ContextProjection
      |
      v
Model Gateway
      |
      v
Provider / model

=================================

RESEARCH PLANE

events + manifests + metrics
            |
            v
        Run Store
            |
   +--------+---------+
   |        |         |
 tables    plots   evaluator
   |        |         |
   +--------+---------+
            |
            v
   Research Workbench
```

## 2. Component ownership

### Cortex

Stable execution kernel.

Owns:

- run lifecycle;
- model/tool turn loop;
- generic runtime state;
- stop/error transitions;
- requests for a ContextProjection.

Does not own scoring, selection or evaluation.

### Context Engine

Owns construction of the model-facing projection for one call.

Conceptual pipeline:

```text
available sources
→ normalize/address context elements
→ classify mandatory vs optional
→ score optional elements
→ apply selection policy under budget
→ materialize representation
→ ContextProjection + manifest
```

For v0, this can remain a simple in-process module.

### Scorer

Interface:

```text
score(task, call_state, context_element) -> utility estimate
```

Candidate implementations:

- OracleScorer;
- deterministic heuristic scorer;
- embedding/retrieval scorer;
- LLM scorer.

A scorer must be versioned because changing its prompt/model/weights changes the experiment.

### SelectionPolicy

Interface:

```text
select(candidates, scores, budget, constraints) -> selected element ids
```

Candidate policies:

- FullContextPolicy;
- SlidingWindowPolicy;
- GreedyUtilityPolicy;
- GreedyDensityPolicy;
- ILPPolicy;
- later residency-aware policies.

The policy receives already computed scores. It must not silently call another scorer.

### Model Gateway

Provider-neutral boundary for model invocation.

Owns:

- provider request/response conversion;
- model parameters;
- usage metadata;
- provider errors;
- optional provider-specific optimizations that do not change canonical experiment semantics.

It must expose actual usage when the provider supplies it and estimated usage otherwise, with the source of the measurement recorded.

### Tool Runtime

Minimal tool interface needed by benchmark workloads.

The first prototype should use a very small deterministic tool set (for example file read/search/lookup) rather than rebuild the whole MCP ecosystem.

MCP support can be added later behind the same tool abstraction.

### Experiment Runner

Owns experiment configuration and repeated execution.

It varies declared independent variables while keeping the rest fixed.

Examples:

- policy;
- scorer;
- budget;
- model;
- seed;
- benchmark case.

### Evaluator

Post-run measurement.

The evaluator must be independent from the scorer whenever possible.

Examples:

- exact expected answer fields;
- programmatic assertions;
- structured artifact validation;
- reference facts;
- LLM judge as a secondary measure when deterministic evaluation is impossible.

### Run Store

Research data source of truth for experiment outputs.

Initial direction:

- DuckDB for analysis/query;
- Parquet for tabular durable exports;
- JSON/JSONL for manifests/events;
- filesystem artifacts for generated files.

This is an implementation baseline, not an architectural requirement.

### Research Workbench

Human-facing research environment.

It reads Run Store data; it should not become an authority over runtime semantics.

## 3. Core data contracts

Exact Python classes are intentionally deferred, but implementation should preserve these conceptual contracts.

### ContextElement

Minimum fields:

```text
element_id
source_type
source_ref
representation_type
content/reference
token_count or estimate
mandatory flag
metadata
```

Optional later fields:

```text
derived_from
revision/hash
recallable
residency state
```

### ScoreRecord

```text
run_id
call_id
element_id
scorer_id
scorer_version
utility
confidence? / diagnostics?
created_at
```

### ContextProjection

```text
projection_id
run_id
call_id
budget_tokens
mandatory_element_ids
selected_optional_element_ids
actual/estimated input tokens
content hash
```

### RunManifest

Must contain enough information to reproduce a run:

```text
run_id
experiment_id
benchmark_case_id + version
model id/provider
model parameters
seed when supported
scorer id/version
selection policy id/version
budget
tool-set version
code revision
dataset revision
timestamps
```

### EvaluationResult

```text
run_id
evaluator id/version
success
quality metrics
failure reason
critical omission flag
diagnostics
```

## 4. Mandatory vs optional context

The simplest optimization experiment should avoid unnecessary model complexity.

Recommended v0 rule:

```text
total model budget
- reserved mandatory context
= optional selection budget
```

Then only optional elements receive binary decision variables.

This keeps the initial optimization model clear while allowing richer constraints later.

## 5. Static selection first, dynamic residency later

### Phase A — static

For each model call:

```text
available candidates
→ score
→ select subset under budget
→ model call
```

### Phase B — temporal residency

Across adjacent calls:

```text
P1 → call
   → release/evict

P2 → call
   → missing information
   → recall

P3 → call
```

Future semantics may include:

- PIN / prefer;
- RELEASE;
- EVICT;
- RECALL;
- COMPACT.

Invariant:

```text
not resident now != deleted
```

## 6. Control principle

The runtime should be deliberately boring.

A benchmark should be able to replace:

```text
Scorer A → Scorer B
```

or:

```text
Greedy → ILP
```

without changing Cortex.

That separation is the basis for causal interpretation of experiment results.
