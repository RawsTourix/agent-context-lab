# Benchmark and experiment protocol

## 1. Purpose

The benchmark exists to answer two separate questions:

1. How well do we estimate the usefulness of context elements?
2. Given those estimates and a budget, how well do we select the subset shown to the model?

These must not be collapsed into one score.

## 2. Benchmark case

A benchmark case should contain:

```text
case_id
case_version
task/request
available context elements
mandatory context
tool environment
expected outcome / evaluation rules
optional ground-truth relevance labels
difficulty/category metadata
```

Cases should be immutable once published. Fixes create a new version.

## 3. Initial workload families

### A. Controlled synthetic selection

Purpose: isolate scorer/selector mechanics.

Characteristics:

- small to medium number of elements;
- known relevant/irrelevant elements;
- deterministic expected answer;
- exact ground-truth relevance available.

Useful for OracleScorer and regression tests.

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

### D. Long-horizon repository analysis

Future case family aligned with 5R-AXIS Context Residency Management:

- read source region;
- persist finding + provenance;
- evict raw source from later projections;
- recall exact region when a late dependency requires it.

## 4. Selection baselines

Every serious comparison should include simple baselines.

Initial policies:

1. **FullContextPolicy** — all eligible context, subject only to hard model limits.
2. **SlidingWindowPolicy** — recent items up to budget.
3. **GreedyUtilityPolicy** — highest utility first.
4. **GreedyDensityPolicy** — utility per token first.
5. **ILPPolicy** — solve the binary selection problem under the same scores/budget.
6. **Oracle upper bound** — where ground-truth relevance permits a meaningful oracle.

Later:

7. summary-capped;
8. state-centric;
9. heuristic working set + recall;
10. dynamic optimization/residency.

## 5. Scorer baselines

Initial scorer family:

- **OracleScorer** — benchmark-only ground truth;
- **HeuristicScorer** — deterministic rules;
- **EmbeddingScorer** — task/context semantic similarity;
- **LLMScorer** — model-based utility estimate.

The scorer configuration is part of the experiment manifest.

## 6. Primary metrics

### Outcome quality

At least one task-quality measure is mandatory.

Possible metrics:

- exact success/failure;
- field-level accuracy;
- constraint satisfaction;
- generated artifact validity;
- reference fact recall;
- critical omission rate.

### Context/resource use

- available context tokens;
- selected context tokens;
- mandatory vs optional token count;
- input tokens reported by provider;
- output tokens;
- total/cached tokens where available;
- estimated monetary cost when pricing metadata is available;
- context-build latency;
- model latency;
- total run latency.

### Optimization diagnostics

- number of candidates N;
- number selected;
- number of constraints;
- solver status;
- solver wall time;
- objective value;
- optimality gap where applicable.

These are especially important for the optimization-course work because a toy demonstration may use small N while the same formulation is tested for hundreds/thousands of variables.

## 7. Quality-resource analysis

Token reduction alone is not improvement.

Comparisons should make the trade-off visible:

```text
quality
  ^
  |  full
  |     A
  |        B
  |             C
  +------------------> context cost
```

Useful derived analysis:

- percentage token reduction at fixed minimum quality;
- quality loss at fixed token budget;
- Pareto frontier of quality vs resource use;
- failure threshold under aggressive compression.

## 8. Experiment controls

To compare policies fairly:

- same benchmark case/version;
- same model/version;
- same system instructions;
- same tool set;
- same model parameters;
- fixed seed when the provider/model supports it;
- temperature kept fixed;
- repeat stochastic runs rather than pretending determinism;
- record code revision and dataset revision.

If provider seed does not guarantee deterministic output, record that limitation.

## 9. Scorer vs selector experiment

A central experiment matrix:

```text
             Full  Greedy  Density  ILP
Oracle
Heuristic
Embedding
LLM
```

Interpretation examples:

- Oracle + ILP strong, LLMScorer + ILP weak → scoring problem.
- Oracle + ILP and Oracle + Greedy similar → exact optimization adds little for that workload.
- all reduced-context policies fail → budget/case requires information that selection cannot safely remove.

## 10. Scale experiment

The formal model should be tested independently of expensive LLM calls.

Generate deterministic candidate sets for:

```text
N = 10, 100, 500, 1k, 5k, 10k, ...
```

Measure:

- solve time;
- memory if practical;
- objective value;
- solver status;
- effect of additional constraints.

This separates optimization-algorithm scalability from agent/provider cost.

## 11. Evaluation independence

Do not use the same LLM prompt/model output both to define utility and to prove final quality unless explicitly labeled as a weak/secondary evaluation.

Prefer deterministic evaluators where possible.

LLM-as-judge may be used for open-ended cases only with:

- fixed rubric;
- versioned judge prompt/model;
- blind comparison where practical;
- deterministic checks alongside it.

## 12. Real traces

Real internet-search-bot traces are **empirical reference workloads**, not ground-truth benchmark cases.

Use them to:

- identify realistic context element types;
- observe context growth/compaction patterns;
- construct realistic synthetic cases;
- test trace import/parsing later.

Do not put raw private/session exports into this public repository.
