# Benchmark and experiment protocol

## 1. Purpose

The benchmark exists to answer two separate questions:

1. How well do we estimate the usefulness of context elements?
2. Given those estimates and a budget, how well do we select the subset shown to the model?

These must not be collapsed into one score.

The benchmark also exists to detect when a context policy saves resources by silently damaging task quality.

## 2. Benchmark case

A benchmark case should contain:

```text
case_id
case_version/content hash
split: development | test
task/request
available source material
elementization policy/version
mandatory context
tool environment/fixtures
expected outcome / evaluation rules
optional ground-truth relevance or sufficient-subset annotations
difficulty/category metadata
```

Cases should be immutable once published. Fixes create a new version.

If scorer prompts/thresholds/policies are tuned against a case, that case cannot remain an untouched final-test case for that tuned configuration.

## 3. Initial workload families

### A. Controlled synthetic selection

Purpose: isolate scorer/selector mechanics.

Characteristics:

- small to medium number of elements;
- known relevant/irrelevant elements;
- deterministic expected answer;
- exact relevance labels or known sufficient subsets;
- fictional/randomized entities where practical.

Useful for OracleScorer and regression tests.

The simplest cases should intentionally satisfy the additive-utility assumptions of the laboratory model so implementation correctness can be tested independently of real-world interactions.

Later synthetic cases should deliberately violate those assumptions through redundancy, prerequisites and complementary facts.

### B. File/package analysis

Purpose: represent real agent work where several files contain overlapping, outdated and conflicting facts.

A case may require:

- reading multiple files;
- selecting current facts;
- obeying source-priority rules;
- producing structured outputs.

This family is directly motivated by real internet-search-bot traces where one request processed a package of files over multiple model/tool iterations.

### C. Multi-step tool task

Purpose: model realistic agent trajectories with intermediate tool results that are useful for different lengths of time.

Prefer fixture-backed deterministic tools for controlled comparisons.

### D. Long-horizon repository analysis

Future case family aligned with 5R-AXIS Context Residency Management:

- read source region;
- persist finding + provenance;
- evict raw source from later projections;
- recall exact region when a late dependency requires it.

### E. Position/order stress cases

Keep the selected information semantically identical while moving critical elements across different context positions.

Purpose:

- measure position sensitivity;
- ensure one selection policy is not accidentally favored by a hidden ordering change.

### F. Structural-dependency cases

Controlled cases where provider-neutral information has explicit dependencies or grouping requirements.

Examples:

- a fact requires its provenance/source label;
- a tool observation must retain the structural call/result linkage needed by the serializer;
- two complementary elements are jointly necessary.

Purpose:

- prove that Context Engine materialization stays provider-valid;
- test extended dependency/group constraints separately from the base one-budget model.

Structural protocol overhead should not be mislabeled as semantic utility.

## 4. Selection baselines

Every serious comparison should include simple baselines.

Initial policies:

1. **FullContextPolicy** — include every eligible element **only when the complete eligible projection fits the hard model-input capacity**.
2. **SlidingWindowPolicy** — recent/canonical-tail items up to the experiment budget.
3. **GreedyUtilityPolicy** — highest utility first.
4. **GreedyDensityPolicy** — highest utility per estimated token first.
5. **ILPPolicy** — solve the binary selection problem under the same scores/budget.
6. **GroundTruth/OracleSelector** — only where a controlled case defines a meaningful sufficient or optimal subset.

Important:

> FullContextPolicy must not silently truncate and still call itself "full context".

If the full projection does not fit, the baseline is `infeasible` for that case/model capacity. SlidingWindowPolicy is the explicit truncation baseline.

## 5. Scorer baselines

Initial scorer family:

- **OracleScorer** — benchmark-only per-element labels/scores on controlled cases;
- **HeuristicScorer** — deterministic rules;
- **EmbeddingScorer** — task/context semantic similarity;
- **LLMScorer** — model-based utility estimate.

The scorer configuration is part of the experiment manifest.

Production-like scorers may see only information available to the agent at that point. Expected answers, evaluator internals and hidden relevance labels are forbidden inputs.

### Oracle limitation

Per-element ground-truth relevance is not a universal oracle.

If two elements are jointly necessary, mutually redundant or contradictory, independent labels do not fully define the best subset.

For those cases use explicit:

- sufficient-subset annotations;
- dependency/group constraints;
- or a dedicated GroundTruthSelector.

Do not claim an "oracle upper bound" unless the benchmark semantics justify it.

## 6. Utility score semantics

The first ILP model treats utility as a scalar surrogate (v_i).

Recommended v0 rule:

- the selector receives finite numeric scores;
- scorer id/version and scale semantics are recorded;
- objective values from different scorers are not compared as if they shared the same scale.

When ground-truth relevance is binary/graded, scorer quality can be evaluated using ranking/classification metrics in addition to downstream task quality.

## 7. Primary metrics

### Outcome quality

At least one task-quality measure is mandatory.

Possible metrics:

- exact success/failure;
- field-level accuracy;
- constraint satisfaction;
- generated artifact validity;
- reference fact recall;
- critical omission rate.

The primary quality metric and acceptable threshold/margin must be declared before the headline experiment.

### Context/resource use

Target-model metrics:

- available context tokens;
- selected context tokens;
- fixed/mandatory vs optional token count;
- provider-reported input tokens;
- output tokens;
- cached tokens where available;
- model-call monetary cost when pricing metadata is available;
- model latency.

Context-management overhead:

- scorer input/output tokens;
- scorer monetary cost;
- scorer latency;
- embedding/retrieval latency/cost;
- context-build latency;
- optimizer/solver time.

System-level metrics:

- total run tokens/cost;
- total run latency;
- total resource use **per successful run**.

This is necessary because an expensive scorer can reduce the target-model prompt while making the complete system more expensive.

### Optimization diagnostics

- number of candidates N;
- number selected;
- number of constraints;
- solver status;
- solver wall time;
- objective value;
- optimality gap where applicable;
- node count where available.

These are especially important for the optimization-course work because a classroom demonstration may use small N while the same formulation is tested for hundreds/thousands of variables.

## 8. Quality-resource analysis

Token reduction alone is not improvement.

Comparisons should make the trade-off visible:

```text
quality
  ^
  |  full
  |     A
  |        B
  |             C
  +------------------> total context/system cost
```

Useful derived analysis:

- percentage resource reduction at a predeclared minimum quality;
- quality loss at fixed budget;
- Pareto frontier of quality vs resource use;
- failure threshold under aggressive reduction;
- total cost per successful run.

## 9. Experiment controls

To compare policies fairly, hold constant unless explicitly declared as a treatment:

- benchmark case/version;
- model/version;
- Cortex version;
- system instructions;
- tool fixtures;
- elementization policy;
- representation policy;
- ordering policy;
- evaluator;
- model parameters.

Also:

- record seed when the provider/model supports it;
- keep temperature and sampling settings fixed;
- repeat stochastic runs rather than pretending determinism;
- record code, dependency and dataset revisions.

Detailed rules live in [EXPERIMENT_DESIGN.md](EXPERIMENT_DESIGN.md).

## 10. Scorer vs selector experiment

A central experiment matrix:

```text
                Sliding  Greedy  Density  ILP
Oracle
Heuristic
Embedding
LLM
```

FullContextPolicy is scorer-independent and should be treated as a separate reference baseline when feasible.

Interpretation examples:

- Oracle + ILP strong, LLMScorer + ILP weak → likely scoring problem.
- Oracle + ILP and Oracle + Greedy similar → exact optimization adds little for that workload.
- all reduced-context policies fail → budget/case may require information that the selector cannot safely remove.
- ILP objective improves but task quality does not → surrogate utility/model assumptions are inadequate.

## 11. Scale experiment

The formal optimization model should be tested independently of expensive LLM calls.

Generate deterministic candidate sets for:

```text
N = 10, 100, 500, 1k, 5k, 10k, ...
```

Measure:

- solve time;
- memory if practical;
- objective value;
- solver status;
- optimality gap;
- effect of additional constraints.

Record hardware, solver version/options and relevant thread settings for performance claims.

This separates optimization-algorithm scalability from agent/provider cost.

## 12. Position sensitivity experiment

Selection and ordering are separate factors.

At least one controlled experiment should:

1. choose a fixed set of context elements;
2. hold content and token count constant;
3. move critical elements between beginning/middle/end positions;
4. measure task quality.

This prevents context-selection results from silently depending on a lucky layout.

## 13. Element granularity experiment

Later, after the static baseline works, test elementization separately:

```text
whole message
paragraph/region
sentence
structured fact
```

Measure both:

- downstream quality/selection flexibility;
- scorer and serialization overhead.

Smaller elements are not automatically better.

## 14. Evaluation independence

Do not use the same LLM prompt/model output both to define utility and to prove final quality unless explicitly labeled as a weak/secondary evaluation.

Prefer deterministic evaluators where possible.

LLM-as-judge may be used for open-ended cases only with:

- fixed rubric;
- versioned judge prompt/model;
- blind comparison where practical;
- deterministic checks alongside it;
- judge tokens/cost tracked separately.

## 15. Real traces

Real internet-search-bot traces are **empirical reference workloads**, not ground-truth benchmark cases.

Use them to:

- identify realistic context element types;
- observe context growth/compaction patterns;
- construct realistic synthetic cases;
- test trace import/parsing later.

Do not put raw private/session exports into this public repository.

## 16. External benchmark inspiration

The project may borrow **methodology**, not necessarily datasets, from long-context and agent-evaluation work such as:

- RULER — configurable synthetic long-context tasks;
- LongBench / LongBench v2 — diverse realistic long-context tasks;
- Letta Context-Bench — agentic filesystem/context retrieval with controlled ground truth;
- Inspect AI — composable evaluation tasks/tools/scorers and structured logs.

Any imported dataset must be reviewed for license, contamination risk and fit with this project's causal questions before use.
