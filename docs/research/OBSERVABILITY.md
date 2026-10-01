# Observability and research data

## 1. Goal

Observability is part of the experiment apparatus, not just debugging.

A result is scientifically useful only if we can reconstruct:

- what configuration was run;
- what context was available;
- what the selector chose;
- what the model actually received;
- what tools ran;
- what outcome was produced;
- how the evaluator scored it.

## 2. Observable events

Initial event taxonomy:

```text
run_started
run_finished
run_failed

model_call_started
context_candidates_built
context_scoring_completed
context_selection_completed
context_projection_built
model_call_finished

tool_call_started
tool_call_finished
tool_call_failed

evaluation_started
evaluation_finished
```

Later residency events:

```text
context_pin_requested
context_release_requested
context_evicted
context_recalled
context_compacted
```

## 3. Event envelope

Every event should have a common envelope:

```text
event_id
event_type
timestamp
experiment_id
run_id
call_id? / tool_call_id?
sequence_number
schema_version
payload
```

Sequence numbers make ordering explicit even when timestamps are close.

## 4. ContextProjection manifest

Every model call should create a manifest that answers:

> What did this exact invocation actually see, and why?

Minimum fields:

```text
projection_id
run_id
call_id
budget_tokens

available_element_ids
mandatory_element_ids
selected_optional_element_ids
excluded/unselected element ids

per-element:
  source_ref
  representation
  token estimate/count
  utility score
  scorer id/version
  selection reason

selection policy id/version
projection token total
projection hash
build latency
```

The manifest may store references/hashes instead of raw sensitive content.

## 5. Usage measurement

For every model call distinguish:

- provider-reported prompt/input tokens;
- local tokenizer estimate;
- estimator name/version;
- difference between estimate and actual where both exist.

Do not silently mix estimated and actual values in one column.

## 6. Runtime logs vs research events

Human-readable application logs and research records are different.

### Logs

For debugging:

- messages;
- warnings;
- stack traces.

### Research events

Stable structured schema:

- machine-readable;
- versioned;
- queryable;
- used to generate figures/tables.

Research analysis should not depend on parsing free-form log text.

## 7. Data retention in this public project

Never commit:

- API keys/tokens;
- private user messages;
- raw session identifiers when unnecessary;
- private tool payloads;
- hidden model reasoning/chain-of-thought;
- provider secrets.

Real traces imported from other projects must be sanitized or transformed into derived benchmark/reference data.

## 8. Run layout

Suggested filesystem layout:

```text
runs/
└── <experiment_id>/
    └── <run_id>/
        ├── manifest.json
        ├── events.jsonl
        ├── projections.jsonl
        ├── evaluation.json
        └── artifacts/
```

Queryable derived data:

```text
research.duckdb
datasets/
exports/
```

Raw run files should remain sufficient to rebuild the analytical database.

## 9. Interesting-run annotation

The Research Workbench should allow a researcher to mark an unusual point/run for later investigation without mutating the raw result.

Example annotation:

```text
annotation_id
run_id / call_id
label: interesting | anomaly | regression | inspect
note
created_at
```

This is the software equivalent of marking the "red star" on an experimental plot: a measured point remains immutable, while the researcher can flag it for deeper analysis.
