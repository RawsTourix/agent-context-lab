# Agent instructions

## Project mode

This repository is a research harness first and an agent product second.

Before implementing or changing architecture, read:

1. `docs/design/CONCEPT.md`
2. `docs/design/ARCHITECTURE.md`
3. `docs/design/DEVELOPMENT_BASELINE.md`
4. the relevant file under `docs/research/`
5. `docs/references/SOURCES.md` when reusing external/project-local code.

## Non-negotiable boundaries

- Cortex is the controlled runtime boundary and must not own scorer/selector/evaluator semantics.
- Scorer and Evaluator are distinct responsibilities.
- Context reduction is not success unless task quality remains acceptable.
- ILP optimality is only with respect to the declared surrogate scores/constraints.
- Elementization, representation and ordering are experiment-affecting factors; do not change them silently.
- Selection operates on provider-neutral research elements; Context Engine materialization must preserve provider/tool structural validity.
- Eligibility/security/disclosure constraints are hard constraints and must not be converted into utility preferences.
- Every model call must be reconstructable from structured observability/manifests to the extent permitted by local privacy settings.
- Canonical run evidence is append-only; analytical databases are derived/rebuildable.
- Do not rely on parsing free-form logs for research metrics.
- Do not persist or expose hidden chain-of-thought.
- Do not commit secrets or raw private traces.
- Provider-specific context features may optimize execution but must not redefine project semantics.
- Keep v0 a modular monolith; do not introduce distributed services without evidence.

## Architecture changes

If code requires changing a documented responsibility or contract:

1. update the design document first;
2. explain the reason/evidence;
3. update schemas/tests with the same change.

Do not create a second undocumented source of truth in code comments.

## Experimental integrity

When comparing two treatments, change only the declared factor(s).

Unless explicitly part of the experiment, hold fixed:

- Cortex version;
- model configuration;
- benchmark case/version;
- tool fixtures;
- ElementizationPolicy;
- RepresentationPolicy;
- OrderingPolicy;
- evaluator;
- serializer/tokenizer basis.

Do not call a silently truncated baseline `FullContextPolicy`.

If all eligible context cannot fit the hard model input capacity, mark that baseline infeasible for that case/model.

## Benchmark leakage

Production-like scorers/policies must not read:

- expected answers;
- hidden relevance labels;
- evaluator-only metadata;
- final-test labels.

OracleScorer/GroundTruthSelector are benchmark-only tools.

If a scorer prompt/threshold/policy is tuned on a case, that case becomes development/tuning data for that configuration.

## Research reproducibility

Any benchmark-affecting change must preserve/version:

- benchmark case definitions/hashes;
- scorer id/version;
- policy id/version;
- evaluator id/version;
- Cortex/Context Engine version;
- elementizer/representation/ordering policy versions;
- model configuration;
- dataset/tool fixture revision;
- tokenizer/serializer version;
- event/schema version;
- code/dependency revision.

A changed experiment configuration creates a new experiment identity; do not silently overwrite historical results.

Remote-provider output may not be bitwise reproducible. The minimum requirement is replayable experiment configuration and model-facing input evidence.

## Failure handling

Do not silently discard failed runs.

Classify failures such as:

- task failure;
- budget infeasible;
- model/provider error;
- tool error;
- evaluation error;
- cancellation/internal error.

Retries create new attempt records or explicit nested provider attempts; they do not erase the original failure evidence.

## Research data

Local raw Run Bundles may contain sensitive content and must be gitignored by default.

Public export must be whitelist/sanitization based.

Annotations and researcher notes are overlays; they must not mutate historical run evidence.

## Reuse from other repositories

Do not copy a subsystem just because it exists in `internet-search-bot`, 5R-AXIS, or another framework.

For reused code:

- verify license compatibility;
- record exact source path + commit;
- adapt only what the lab needs;
- preserve required attribution;
- add local tests.

`internet-search-bot` is MIT-licensed.

5R-AXIS research documents are design input, not an implementation dependency; do not copy private/unlicensed implementation into this public repository without an explicit licensing decision.

## Implementation restraint

Not required for v0 unless a concrete benchmark proves the need:

- vector database;
- general long-term memory;
- multi-agent orchestration;
- full MCP discovery layer;
- public chat UI;
- distributed runtime;
- provider-specific agent framework lock-in;
- learned context compression;
- autonomous context-policy evolution.

Start with a deterministic ScriptedModel/FakeModel plus fixture-backed tools and a simple, inspectable runtime. A live provider is the second vertical slice, not a prerequisite for proving the research apparatus.
