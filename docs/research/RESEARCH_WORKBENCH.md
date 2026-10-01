# Research Workbench

## 1. Intent

The workbench should feel like an experimental control room rather than a chat application.

The researcher should be able to:

- launch controlled experiments;
- watch an agent run live;
- inspect each model call and trajectory step;
- compare policies/scorers/budgets;
- see plots update from stored results;
- mark anomalies/interesting runs;
- export the same data to CSV/XLSX/Parquet/JSON;
- reproduce a previous run configuration;
- distinguish raw evidence from later annotations.

## 2. Initial implementation direction

Fast research-first stack:

- **Python** — experiment/runtime language;
- **DuckDB** — local analytical database;
- **Parquet** — portable tabular results;
- **JSON/JSONL** — canonical manifests/events;
- **Streamlit** — first researcher UI;
- **Plotly** — interactive research plots.

This stack is provisional. The data contracts matter more than the UI framework.

The first read-only Workbench should appear early in development, not after all scorer research is finished.

## 3. Main screens

### Overview

Shows:

- number of experiments/trials/attempts;
- task success rate;
- infrastructure failure rate;
- recent regressions;
- aggregate tokens/cost/latency;
- benchmark/dataset version;
- code revision.

### Experiments

Create/select an immutable ExperimentSpec:

```text
benchmark dataset/version
case split
model
model parameters
scorer
selection policy
elementization/representation/ordering
budgets
seeds/repetitions
tool fixtures
primary metrics
quality floor/margin
```

The UI expands the sweep into concrete TrialSpecs.

### Live

For a currently running experiment:

```text
trial / attempt
iteration/model call
available tokens
selected tokens
selected/available element count
scoring latency/cost
last tool
elapsed time
current status
```

### Runs

Filterable table:

- experiment/trial/run ids;
- case;
- model;
- scorer;
- policy;
- budget;
- quality;
- selected/input tokens;
- total system tokens/cost;
- latency;
- failure class/status.

### Trajectory

Chronological view of:

```text
task start
→ context build
→ model call
→ tool call
→ observation
→ next projection
→ ...
→ evaluation
```

Clicking a step opens the exact event/projection/model-call evidence.

### Context Inspector

For one model call, show available vs selected context.

Example columns:

```text
position
element id
source type/ref
representation
estimated token cost
utility
mandatory?
selected?
selection reason
```

The Inspector should make ordering visible because position is itself experimentally relevant.

Later add residency states:

```text
PIN / preferred
RELEASED
EVICTED
RECALLED
COMPACTED
```

### Invocation Inspector

Show the complete logical model input basis:

- fixed instructions refs/hashes;
- tool schemas;
- ordered ContextProjection;
- model parameters;
- tokenizer/serializer;
- estimated and provider-reported token usage;
- request/retry ids.

Local raw content visibility is controlled by privacy mode.

### Compare

Compare selected TrialSpec groups while holding known controls fixed.

Primary views:

- policy vs quality;
- policy vs tokens;
- budget vs quality;
- budget vs tokens;
- scorer quality vs downstream evaluator quality;
- token savings vs quality loss;
- total system cost per successful run;
- Pareto frontier;
- optimization solve time vs N;
- position sensitivity;
- scorer/selector overhead decomposition.

Paired comparisons should clearly show the common case set and number of repetitions.

### Benchmarks

Browse benchmark cases, splits and evaluation rules without exposing private raw traces.

Show whether a case has been used for tuning/development so accidental test leakage is visible.

### Exports

Export exactly the filtered/selected research data to:

- CSV;
- XLSX;
- Parquet;
- JSON.

Exports should include metadata identifying schema, code, dataset and experiment versions.

Public export is a separate sanitized/whitelisted operation from local raw Run Bundles.

## 4. Automatic plots

Plots are views over stored data, not manually curated screenshots.

Initial plot library:

1. input tokens by model call;
2. available vs selected context tokens;
3. task quality by policy;
4. quality vs budget;
5. quality vs selected tokens;
6. token/resource reduction vs quality loss;
7. total system cost per successful run;
8. solver time vs number of variables;
9. scorer prediction vs ground-truth relevance where available;
10. critical omission rate;
11. latency/cost breakdown;
12. quality by critical-information position;
13. selected-element count/granularity distribution.

Plot tooltips should expose experiment/trial/run ids so an interesting point can be opened immediately.

## 5. Research notebook principle

The UI is not the only analysis surface.

All metrics must remain accessible through:

- SQL in DuckDB;
- Python/pandas/polars;
- exported Parquet/CSV.

A graph in the UI should be reproducible from stored data.

## 6. Experiment and trial manifests

ExperimentSpec is an immutable sweep definition.

Example:

```yaml
experiment_id: exp-0042

benchmark:
  dataset: context-bench-v1
  split: test
  cases: all

model:
  provider: ...
  id: ...
  temperature: 0

scorer:
  id: llm-scorer-v2

selector:
  id: ilp-v1

budgets:
  - 4000
  - 8000
  - 12000

repetitions: 5

primary_metrics:
  quality: exact_success
  efficiency: total_input_tokens_per_success

quality_floor:
  relative_to_full_context: 0.95
```

The runner resolves this into TrialSpecs where each trial has one case, one budget, one treatment and one replicate identity.

After execution begins, ExperimentSpec is immutable. A changed sweep becomes another experiment.

## 7. Statistical views

The Workbench should not imply precision that the experiment does not support.

Comparison views should show, where applicable:

- number of paired cases;
- number of attempts/repetitions;
- mean/median as appropriate;
- confidence interval/dispersion;
- absolute effect size;
- missing/failed attempts.

Default research direction: paired bootstrap confidence intervals over cases for aggregate policy comparisons when sample size is sufficient.

## 8. Annotation workflow

Interesting/anomalous points can be tagged after a run.

Annotations are overlays and never mutate canonical run evidence.

Useful labels:

```text
interesting
anomaly
regression
inspect
possible-scorer-failure
possible-selector-failure
possible-position-effect
infrastructure-noise
```

This supports the "red star on the plot" research workflow.

## 9. Scientific ergonomics

The workbench should help answer questions, not merely display telemetry.

Examples:

- "Show all cases where ILP used fewer tokens than full context but quality dropped."
- "Which context elements are most often selected by OracleScorer but missed by LLMScorer?"
- "At which budget does quality start to collapse?"
- "Which cases cause greedy and ILP to diverge most?"
- "Does the result change when the same critical fact moves to the middle of the context?"
- "Did LLMScorer save downstream tokens after including its own scoring cost?"
- "Show solver runtime distribution for N >= 5000."
- "Open the exact projection and trajectory for this anomalous point."

That is the intended research workflow.

## 10. Prior-art note

Inspect AI, MLflow and recent long-horizon agent runtimes provide useful patterns for:

- experiments/runs;
- structured logs;
- live evaluation views;
- post-run metadata/annotations;
- replay and provenance.

Agent Context Lab should borrow proven ideas but keep a smaller domain-specific workbench because model-visible context selection is itself the object of study.
