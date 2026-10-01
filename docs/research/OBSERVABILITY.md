# Observability and research data

## 1. Goal

Observability is part of the experiment apparatus, not just debugging.

A result is scientifically useful only if we can reconstruct:

- what configuration was run;
- what context was available;
- what the selector chose;
- in what order/representation it was materialized;
- what the model actually received;
- what tools ran;
- what outcome was produced;
- how the evaluator scored it;
- which attempts/retries/errors occurred.

## 2. Canonical evidence model

The **append-only Run Bundle** is the canonical experiment record.

DuckDB/Parquet tables are derived analytical views and must be rebuildable from Run Bundles.

A Run Bundle must never be silently rewritten to "clean up" an old result.

Post-run annotations are stored as separate overlay records with provenance.

This follows a useful research principle:

> raw measurement remains immutable; interpretation may evolve separately.

## 3. Observable events

Initial event taxonomy:

```text
run_started
run_finished
run_failed

model_call_started
context_candidates_built
context_scoring_started
context_scoring_completed
context_selection_started
context_selection_completed
context_projection_built
model_request_started
model_request_finished
model_call_finished

tool_call_started
tool_call_finished
tool_call_failed

evaluation_started
evaluation_finished
```

Budget/error events:

```text
context_budget_infeasible
context_serialization_overflow
provider_retry
```

Later residency events:

```text
context_pin_requested
context_release_requested
context_evicted
context_recalled
context_compacted
```

## 4. Event envelope

Every event should have a common envelope:

```text
event_id
event_type
timestamp_utc
monotonic_offset_ns? / duration_ns?
experiment_id
trial_id
run_id
attempt_id
call_id? / tool_call_id?
parent_event_id? / span_id?
sequence_number
schema_version
payload
```

### Ordering

- `sequence_number` is monotonic within a RunAttempt.
- timestamps are for human/cross-system correlation;
- monotonic durations are preferred for latency measurement where possible.

### Causality

Parent/span identifiers are useful for:

- nested model/scorer/tool calls;
- retries;
- future parallel tools;
- mapping to OpenTelemetry-style traces.

The project does not need to adopt OpenTelemetry as a runtime dependency in v0, but should avoid an event schema that makes later mapping impossible.

## 5. ContextProjection manifest

Every model call should create a manifest that answers:

> What did this exact invocation actually see, in what order, and why?

Minimum fields:

```text
projection_id
run_id
call_id
selection_budget_tokens

available_element_ids
mandatory_element_ids
selected_optional_element_ids
unselected element ids

ordered_model_facing_items:
  item/element ref
  role/segment kind
  source ref/revision
  representation kind
  estimated token cost
  utility score
  scorer id/version
  inclusion reason

elementizer id/version
representation policy id/version
ordering policy id/version
selection policy id/version

tokenizer id/version
serializer id/version
estimated projection tokens
projection/content hash
build latency
```

The manifest may store immutable refs/hashes instead of raw sensitive content.

## 6. Model invocation evidence

A ContextProjection is only part of the full request.

The model invocation record must also identify fixed inputs that affect model behavior/token count:

- system/developer instructions;
- provider protocol framing where observable;
- tool/function schemas;
- model parameters;
- model/provider identifier;
- serialized request hash or canonical request snapshot;
- provider request id when exposed.

Goal:

> reconstruct the logical model-facing input exactly enough to replay the request even if the provider wire format changes.

The project does **not** promise future identical model output from a remote provider.

## 7. Usage measurement

For every model/scorer call distinguish:

- provider-reported prompt/input tokens;
- provider-reported output tokens;
- cached/read/write tokens where exposed;
- local tokenizer estimate;
- estimator/tokenizer name/version;
- difference between estimate and actual where both exist.

Do not silently mix estimated and actual values in one column.

For selection/scoring overhead, record the same kinds of usage separately from the target model call.

## 8. Retry and attempt semantics

Retries must remain observable.

A logical model operation may contain multiple provider attempts.

Record:

```text
logical_call_id
attempt_index
provider_request_id
started/finished
status
error class
usage/cost if billed/known
```

Do not hide rate-limit/network retries inside one latency number if they materially affect total run cost.

## 9. Runtime logs vs research events

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

Research analysis must not depend on parsing free-form log text.

## 10. Failure taxonomy

Every RunAttempt ends with a classified state.

Initial classes:

```text
success
task_failure
budget_infeasible
budget_infeasible_after_serialization
model_error
provider_error
tool_error
evaluation_error
cancelled
internal_error
```

Keep:

- runtime status;
- task-quality result;
- infrastructure failure class

as separate fields.

A provider outage is not the same scientific outcome as an agent choosing the wrong answer.

## 11. Data retention and privacy

This is a public repository, but experiments may contain sensitive local data.

### Local raw mode

A local ignored Run Bundle may contain model-visible content when needed for scientific inspection/replay.

It must not contain hidden chain-of-thought that was never exposed by the provider/runtime.

### Public/export mode

Public artifacts must use a **whitelist export schema**.

Only explicitly approved fields/content leave local research storage.

Do not rely on "copy everything, then regex-redact known secrets" as the publication model.

Never commit:

- API keys/tokens;
- private user messages without explicit sanitization;
- raw session identifiers when unnecessary;
- private tool payloads;
- hidden model reasoning/chain-of-thought;
- provider secrets.

Real traces imported from other projects must be sanitized or transformed into derived benchmark/reference data.

## 12. Suggested Run Bundle layout

```text
runs/
└── <experiment_id>/
    └── <trial_id>/
        └── <attempt_id>/
            ├── manifest.json
            ├── events.jsonl
            ├── projections.jsonl
            ├── model_calls.jsonl
            ├── evaluation.json
            └── artifacts/
```

Derived/queryable data:

```text
research.duckdb
datasets/
exports/
```

Raw run files must remain sufficient to rebuild the analytical database.

## 13. Interesting-run annotation

The Research Workbench should allow a researcher to mark an unusual point/run for later investigation without mutating raw evidence.

Example annotation:

```text
annotation_id
target_type: run | call | projection | event
target_id
label: interesting | anomaly | regression | inspect
note
created_at
author
source/provenance
```

Annotations live in a separate append-only overlay.

This is the software equivalent of marking the "red star" on an experimental plot: the measured point remains immutable while the researcher flags it for deeper analysis.

## 14. External observability compatibility

Two useful reference families:

- OpenTelemetry GenAI semantic conventions;
- OpenInference semantic conventions.

Both can inform naming/span structure.

Agent Context Lab should keep its research schema provider-neutral and stable even if external conventions evolve.
