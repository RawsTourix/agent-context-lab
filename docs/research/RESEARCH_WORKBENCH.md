# Research Workbench

## 1. Intent

The workbench should feel like an experimental control room rather than a chat application.

The researcher should be able to:

- launch controlled experiments;
- watch an agent run live;
- inspect each model call;
- compare policies/scorers/budgets;
- see plots update from stored results;
- mark anomalies/interesting runs;
- export the same data to CSV/XLSX/Parquet/JSON;
- reproduce a previous run configuration.

## 2. Initial implementation direction

Fast research-first stack:

- **Python** — experiment/runtime language;
- **DuckDB** — local analytical database;
- **Parquet** — portable tabular results;
- **JSON/JSONL** — manifests and event streams;
- **Streamlit** — first researcher UI;
- **Plotly** — interactive research plots.

This stack is provisional. The data contracts matter more than the UI framework.

## 3. Main screens

### Overview

Shows:

- number of experiments/runs;
- success rate;
- recent regressions;
- aggregate token/cost/latency;
- current benchmark version.

### Experiments

Create/select an immutable experiment manifest:

```text
benchmark dataset/version
cases
model
model parameters
scorer
selection policy
budgets
seeds/repetitions
tool set
```

### Live

For a currently running experiment:

```text
iteration/model call
available tokens
selected tokens
selected/available element count
last tool
elapsed time
current status
```

### Runs

Filterable table:

- run id;
- case;
- model;
- scorer;
- policy;
- budget;
- quality;
- selected/input tokens;
- latency;
- status.

### Context Inspector

For one model call, show available vs selected context.

Example columns:

```text
element id
source type/ref
token cost
utility
mandatory?
selected?
selection reason
representation
```

Later add residency states:

```text
PIN / preferred
RELEASED
EVICTED
RECALLED
COMPACTED
```

### Compare

Compare selected runs/experiment groups while holding known controls fixed.

Primary views:

- policy vs quality;
- policy vs tokens;
- budget vs quality;
- budget vs tokens;
- scorer vs evaluator quality;
- token savings vs quality loss;
- Pareto frontier;
- optimization solve time vs N.

### Benchmarks

Browse benchmark cases and their evaluation rules without exposing private raw traces.

### Exports

Export exactly the filtered/selected research data to:

- CSV;
- XLSX;
- Parquet;
- JSON.

Exports should include metadata identifying schema and experiment versions.

## 4. Automatic plots

Plots are views over stored data, not manually curated screenshots.

Initial plot library:

1. input tokens by model call;
2. available vs selected context tokens;
3. task quality by policy;
4. quality vs budget;
5. quality vs selected tokens;
6. token reduction vs quality loss;
7. solver time vs number of variables;
8. scorer prediction vs ground-truth relevance where available;
9. critical omission rate;
10. latency breakdown.

## 5. Research notebook principle

The UI is not the only analysis surface.

All metrics must remain accessible through:

- SQL in DuckDB;
- Python/pandas/polars;
- exported Parquet/CSV.

A graph in the UI should be reproducible from stored data.

## 6. Experiment manifests

An experiment configuration must be versioned and preserved.

Example:

```yaml
experiment_id: exp-0042

benchmark:
  dataset: context-bench-v1
  cases: all

model:
  provider: ...
  id: ...
  temperature: 0
  seed: 42

scorer:
  id: llm-scorer-v2

selector:
  id: ilp-v1

budgets:
  - 4000
  - 8000
  - 12000

repetitions: 5
```

After execution begins, the manifest is immutable. A changed configuration becomes another experiment.

## 7. Scientific ergonomics

The workbench should help answer questions, not merely display telemetry.

Examples:

- "Show all cases where ILP used fewer tokens than full context but quality dropped."
- "Which context elements are most often selected by OracleScorer but missed by LLMScorer?"
- "At which budget does quality start to collapse?"
- "Which cases cause greedy and ILP to diverge most?"
- "Show solver runtime distribution for N >= 5000."
- "Open the exact projection for this anomalous point."

That is the intended research workflow.
