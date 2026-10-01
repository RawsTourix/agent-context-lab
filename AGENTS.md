# Agent instructions

## Project mode

This repository is a research harness first and an agent product second.

Before implementing or changing architecture, read:

1. `docs/design/CONCEPT.md`
2. `docs/design/ARCHITECTURE.md`
3. the relevant file under `docs/research/`
4. `docs/references/SOURCES.md` when reusing external/project-local code.

## Non-negotiable boundaries

- Cortex is the stable agent runtime and must not own scorer/selector/evaluator semantics.
- Scorer and Evaluator are distinct responsibilities.
- Context reduction is not success unless task quality remains acceptable.
- Every model call must be reconstructable from structured observability/manifests.
- Do not rely on parsing free-form logs for research metrics.
- Do not persist or expose hidden chain-of-thought.
- Do not commit secrets or raw private traces.
- Provider-specific context features may optimize execution but must not redefine project semantics.
- Keep v0 a modular monolith; do not introduce distributed services without evidence.

## Architecture changes

If code requires changing a documented responsibility or contract:

1. update the design document first;
2. explain the reason/evidence;
3. update tests and schemas with the same change.

Do not create a second undocumented source of truth in code comments.

## Reuse from other repositories

Do not copy a subsystem just because it exists in `internet-search-bot` or 5R-AXIS.

For reused code:

- verify license compatibility;
- record source path and commit;
- adapt only what the lab needs;
- add local tests.

5R-AXIS research documents are design input, not an implementation dependency.

## Research reproducibility

Any benchmark-affecting change must preserve/version:

- benchmark case definitions;
- scorer id/version;
- policy id/version;
- evaluator id/version;
- model configuration;
- dataset revision;
- event/schema version.

A changed experiment configuration creates a new experiment identity; do not silently overwrite historical results.

## Implementation restraint

Not required for v0 unless a concrete benchmark proves the need:

- vector database;
- general long-term memory;
- multi-agent orchestration;
- full MCP discovery layer;
- public chat UI;
- distributed runtime;
- provider-specific agent framework lock-in.
