# Experiment design and statistical protocol

**Status:** baseline protocol for controlled comparisons.

The benchmark tells us *what* to run. This document defines *how* comparisons should be run so that the result can be interpreted.

## 1. Experimental hierarchy

Use four distinct levels:

```text
ExperimentSpec
  └── TrialSpec
       └── RunAttempt
            └── model/tool calls
```

### ExperimentSpec

Immutable sweep definition.

Examples of declared factors:

- benchmark dataset/version;
- cases/split;
- model/provider configuration;
- scorer family;
- selection policies;
- budgets;
- repetitions;
- evaluation protocol;
- primary metrics.

### TrialSpec

One fully resolved treatment combination for one benchmark case and one replicate.

A trial must not contain unresolved lists such as `budgets: [4000, 8000]`; it contains one concrete budget.

### RunAttempt

One execution attempt of a TrialSpec.

Infrastructure retry must create a new attempt identity rather than silently replacing the failed attempt.

This separates agent-quality failures from provider/tool/infrastructure failures.

## 2. Unit of comparison

For policy/scorer comparisons, prefer a **paired design**:

```text
same case
same model configuration
same tool fixtures
same elementization
same ordering
same representation
same evaluator
different declared treatment
```

The case is the natural blocking unit.

For stochastic models, repeated attempts are needed. A provider seed may be recorded and reused when supported, but it must not be treated as a guarantee of identical output.

## 3. Development, tuning and final evaluation

Benchmark cases should support explicit splits when any scorer/prompt/threshold/policy is tuned:

```text
development / tuning
test
```

Optional larger datasets may use:

```text
train
development
test
```

Rules:

- Oracle labels/expected answers are never visible to production-like scorers.
- A scorer prompt tuned against a test case makes that test case contaminated for the tuned scorer.
- Final headline results must come from cases not used to tune scorer prompts, thresholds or policy hyperparameters.
- Synthetic cases should use fictional/randomized entities when practical to reduce training-data leakage.

## 4. Predeclared quality criterion

"Acceptable quality loss" must not be chosen after looking at results.

Before a headline experiment, declare one of:

- exact task success;
- a minimum task-quality floor;
- an equivalence/non-inferiority margin relative to baseline;
- a task-specific rubric threshold.

Example:

```text
primary quality metric: exact task success
minimum acceptable rate: 0.95 of FullContext baseline
primary resource metric: total input tokens per successful run
```

A different threshold is a different experiment specification.

## 5. Primary and secondary metrics

Every experiment should declare primary metrics before execution.

Recommended default framing:

### Primary quality

Task-specific success/quality.

### Primary efficiency

A system-level measure such as:

```text
total tokens/cost/latency per successful run
```

not only selected context tokens.

### Secondary diagnostics

- target-model input tokens;
- scorer tokens/cost/latency;
- embedding/retrieval cost;
- solver time;
- context-build time;
- critical omission rate;
- failure class.

This prevents an expensive LLM scorer from appearing efficient merely because it shortens the downstream prompt.

## 6. Repetitions and uncertainty

For deterministic synthetic optimization tests, repeated solver runs may be used for timing stability but are not needed to estimate task success.

For stochastic LLM experiments:

- run multiple repetitions per case/treatment;
- keep repetitions balanced across compared treatments;
- report the number of cases and attempts;
- report dispersion/uncertainty, not only a single mean.

Default aggregate reporting direction:

- paired difference per case when comparing two treatments;
- 95% bootstrap confidence interval over benchmark cases when the sample size supports it;
- effect size / absolute difference alongside any significance test.

Do not claim a meaningful difference solely from a small change in a noisy point estimate.

## 7. Run order and provider drift

External model services can change over time.

To reduce temporal confounding:

- run compared treatments in the same time window when practical;
- randomize/interleave treatment order across cases;
- record timestamps and provider/model identifiers;
- record resolved model revision/fingerprint when the provider exposes one;
- record SDK/provider adapter versions.

"Reproducible" therefore has two levels:

1. **input/configuration replayability** — the exact experiment configuration and model-facing input can be reconstructed;
2. **output reproducibility** — identical model output, which may not be guaranteed for remote/stochastic providers.

The project promises the first. It records evidence relevant to the second.

## 8. Tool determinism

Controlled benchmark tools should be fixture-backed or otherwise deterministic.

If a benchmark deliberately uses live web/API tools:

- record retrieval time;
- preserve the returned observation when allowed;
- classify the run as environment-dependent;
- do not compare it directly with fixture-backed deterministic runs without saying so.

## 9. Position and ordering as confounders

Long-context model performance can depend on where relevant information appears.

Therefore v0 selection experiments must use a fixed, versioned `OrderingPolicy`.

Suggested v0 behavior:

- mandatory segments use a fixed canonical order;
- selected optional elements preserve a deterministic source/case order.

Later experiments may vary ordering explicitly.

A useful stress test is to keep the selected set constant while permuting the position of critical elements.

## 10. Elementization as a confounder

Selection quality depends on how source material is divided into elements.

Therefore `ElementizationPolicy` is fixed and versioned within an experiment.

Changing:

```text
whole message
→ paragraph
→ sentence
→ token span
```

changes both the optimization problem and scorer workload.

Granularity can become an independent variable only in a dedicated experiment.

## 11. Analysis integrity

Do not silently drop failed runs.

Every RunAttempt must end in a classified state such as:

```text
success
task_failure
budget_infeasible
model_error
tool_error
provider_error
evaluation_error
cancelled
```

Headline task-quality metrics should state which failure classes are included/excluded and why.

Infrastructure failures should remain visible even when retried.
