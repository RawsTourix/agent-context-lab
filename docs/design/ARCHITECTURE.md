# Architecture baseline

## 1. Design goal

Keep the **agent runtime under test** fixed within a controlled comparison while context-management strategies are exchanged around it.

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
      +--> ElementizationPolicy
      +--> Scorer
      +--> SelectionPolicy
      +--> RepresentationPolicy
      +--> OrderingPolicy
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

append-only events + manifests + artifacts
            |
            v
        Run Bundle
            |
            v
   Derived Research Store
      (DuckDB/Parquet)
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

Not every policy in this diagram needs a separate class in v0. The diagram names responsibilities that must be versioned or held fixed when they can affect an experiment.

## 2. Component ownership

### Cortex

Stable experimental execution kernel.

Owns:

- run lifecycle;
- model/tool turn loop;
- generic runtime state;
- stop/error transitions;
- requests for a ContextProjection.

Does not own scoring, selection, benchmark or evaluation semantics.

A Cortex implementation may evolve between project versions. Its exact version is fixed within a controlled comparison and recorded in every RunManifest.

### Context Engine

Owns construction of the model-facing projection for one call.

Conceptual pipeline:

```text
available sources
→ normalize/address provider-neutral context elements
→ apply eligibility / hard constraints
→ classify fixed/mandatory vs optional
→ score optional elements
→ select optional elements under budget
→ close structural dependencies if required
→ choose/materialize representation
→ apply deterministic ordering
→ serialize a provider-valid projection
→ ContextProjection + manifest
```

For v0 this remains an in-process module.

### ElementizationPolicy

Defines how source material becomes selectable elements.

Examples:

- one message = one element;
- one tool result = one element;
- file split by paragraph/region;
- structured state items.

Elementization is fixed in ordinary policy comparisons because granularity changes both optimization and scoring workload.

### Eligibility / hard constraints

Before utility scoring, the Context Engine determines which source material is allowed and structurally eligible for the target invocation.

Examples:

- disclosure/security eligibility;
- benchmark/runtime scope restrictions;
- mandatory current-task constraints;
- provider/tool structural requirements.

These rules are not utility scores. A selector cannot override them.

### Scorer

Interface:

```text
score(task, call_state, context_element) -> utility estimate
```

Candidate implementations:

- OracleScorer for controlled cases;
- deterministic heuristic scorer;
- embedding/retrieval scorer;
- LLM scorer.

A scorer must be versioned because changing its prompt/model/weights changes the experiment.

Production-like scorers must not read benchmark expected answers or hidden ground-truth relevance labels.

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

### Structural closure and materialization

Selection operates on provider-neutral research elements rather than blindly deleting raw provider messages.

The materialization stage must preserve request validity.

Examples:

- a selected tool observation may need a corresponding call identifier/structural envelope;
- provider role sequences must remain valid;
- fixed tool schemas/system instructions remain accounted for even when they are not decision variables.

If a dependency itself should compete for budget as meaningful content, represent it explicitly as a dependency/group constraint in an extended model. Otherwise structural envelope cost is fixed/materialization overhead.

### RepresentationPolicy

Defines the model-facing representation of a selected source.

v0 direction:

- raw/exact candidate representation only.

Later candidates:

- extractive representation;
- structured extraction;
- summary/digest;
- metadata-only reference.

Representation changes must preserve provenance/lineage.

### OrderingPolicy

Defines the order of selected items inside the model-facing context.

v0 direction:

- deterministic canonical ordering;
- preserve benchmark/source order for optional elements after selection.

Ordering is kept fixed because long-context performance can be position-sensitive.

### Model Gateway

Provider-neutral boundary for model invocation.

Owns:

- provider request/response conversion;
- model parameters;
- usage metadata;
- provider errors and retry attempts;
- optional provider-specific optimizations that do not change project semantics.

It must expose actual usage when the provider supplies it and estimated usage otherwise, with measurement source recorded.

### Tool Runtime

Minimal tool interface needed by benchmark workloads.

The first prototype should use a small deterministic fixture-backed tool set rather than rebuild the whole MCP ecosystem.

MCP can be added later behind the same abstraction.

### Experiment Runner

Owns experiment configuration, factor expansion and repeated execution.

It varies declared independent variables while holding controls fixed.

### Evaluator

Post-run measurement.

The evaluator must be independent from the scorer whenever possible.

Examples:

- exact expected answer fields;
- programmatic assertions;
- structured artifact validation;
- reference facts;
- LLM judge as a secondary measure when deterministic evaluation is impossible.

### Run Bundle

Canonical append-only evidence for one RunAttempt.

Contains:

- resolved run manifest;
- structured event stream;
- model-call/projection manifests;
- evaluation result;
- generated artifacts or immutable refs.

A Run Bundle must be sufficient to rebuild the analytical database.

### Derived Research Store

Queryable analytical layer derived from Run Bundles.

Initial direction:

- DuckDB for analysis/query;
- Parquet for durable tabular exports;
- JSON/JSONL for canonical manifests/events.

DuckDB is rebuildable and is **not** the only copy/source of experiment evidence.

### Research Workbench

Human-facing research environment.

It reads canonical/derived research data and writes only separate annotations/experiment definitions.

It must not mutate historical raw run evidence.

## 3. Experiment identity hierarchy

Use distinct identities:

```text
ExperimentSpec
  └── TrialSpec
       └── RunAttempt
            ├── ModelCall
            └── ToolCall
```

### ExperimentSpec

Immutable sweep definition: dataset, treatments, budgets, repetitions and primary metrics.

### TrialSpec

One fully resolved case + treatment + replicate configuration.

### RunAttempt

One execution attempt. Infrastructure retries create new attempts rather than overwriting a failure.

This hierarchy prevents ambiguous manifests such as one "run" that still contains multiple unresolved budgets.

## 4. Budget accounting

Do not conflate the provider context window with the selector budget.

Conceptually:

```text
provider context capacity
- reserved output allowance
= maximum model input capacity

maximum model input capacity
- fixed protocol/system/tool-schema overhead
- mandatory dynamic context
= available optional capacity

selection budget
= min(experiment optional budget, available optional capacity)
```

If fixed + mandatory context already exceeds capacity, the call is `budget_infeasible`.

The Context Engine must not silently drop mandatory content to make a run fit.

## 5. Token cost semantics

The base mathematical model uses additive per-element costs (s_i), but real model serialization adds overhead.

Therefore store at least:

- element-local token estimate;
- tokenizer id/version;
- serializer id/version;
- estimated full projection tokens after materialization;
- provider-reported input tokens when available.

If the selected subset fits the additive estimate but the serialized projection exceeds the hard input capacity, v0 must use a deterministic, logged overflow policy rather than hidden truncation.

Preferred v0 behavior: fail the projection as `budget_infeasible_after_serialization` so estimator error remains visible.

A later explicit repair policy may be benchmarked separately.

## 6. Core data contracts

Exact Python classes are intentionally deferred, but implementation should preserve these conceptual contracts.

### ContextElement

Minimum fields:

```text
element_id
source_type
source_ref
source_revision/hash when applicable
representation_type
content/reference
estimated_tokens
tokenizer_id/version
mandatory flag + mandatory reason
eligibility/hard-constraint metadata
structural dependency/group refs when applicable
metadata
```

Optional later fields:

```text
derived_from
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
raw scorer output/diagnostics reference?
scoring tokens/cost/latency
created_at
```

Utility values from different scorer scales are not automatically comparable.

### ContextProjection

```text
projection_id
run_id
call_id
budget_tokens
ordered model-facing element ids
mandatory element ids
selected optional element ids
unselected element ids
elementizer id/version
representation policy id/version
ordering policy id/version
tokenizer id/version
serializer id/version
estimated projection tokens
content/request hash
build latency
```

The exact provider request may additionally include fixed instructions/tool schemas represented by immutable refs/hashes in the invocation manifest.

### RunManifest

Must contain enough information to replay the experiment input/configuration:

```text
run_id / attempt_id
trial_id
experiment_id
benchmark case id + version/hash
benchmark split
Cortex version
Context Engine version
model provider/id
resolved model revision/fingerprint when exposed
model parameters
seed when supported
scorer id/version
selection policy id/version
elementizer id/version
representation policy id/version
ordering policy id/version
tokenizer/serializer versions
budget
tool-set/fixture version
evaluator id/version
code revision
dataset revision
runtime/dependency version info
timestamps
```

Remote providers may not guarantee identical outputs. The project guarantees replayable configuration/model-facing input when sufficient evidence is available, not bitwise-identical future inference.

### EvaluationResult

```text
run_id
evaluator id/version
success
quality metrics
failure reason/class
critical omission flag
diagnostics
```

## 7. Mandatory vs optional context

Recommended v0 rule:

```text
available optional capacity
→ only optional elements receive binary decision variables
```

Mandatory material is accounted for before selection.

This keeps the first laboratory optimization model clear while allowing richer constraints later.

## 8. Static selection first, dynamic residency later

### Phase A — static

For each model call:

```text
available candidates
→ score
→ select subset under budget
→ fixed representation/order
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

## 9. Control principle

The runtime should be deliberately boring.

A benchmark should be able to replace:

```text
Scorer A → Scorer B
```

or:

```text
Greedy → ILP
```

without changing Cortex, elementization, ordering, representation, tool fixtures or evaluator unless those are explicitly declared treatment factors.

That separation is the basis for causal interpretation of experiment results.
