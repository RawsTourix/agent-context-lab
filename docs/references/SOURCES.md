# Sources and reusable inputs

This registry distinguishes **code to inspect/reuse**, **architecture/research input**, **benchmark/evaluation prior art**, and **scientific evidence**.

A link here does not mean the project copies that source's architecture or accepts every claim in it.

## 1. RawsTourix / internet-search-bot

Repository:

- https://github.com/RawsTourix/internet-search-bot

License:

- MIT.

Role:

> Generation-1 practical reference: working agent/tool integration, operational traces and lessons from context growth.

### Components worth inspecting

#### Gateway

- https://github.com/RawsTourix/internet-search-bot/blob/main/src/gateway.py

Useful ideas:

- explicit transport/gateway boundary;
- FastAPI lifecycle/health patterns;
- adapter separation.

Do not copy as-is: Agent Context Lab does not need Telegram or a multi-protocol public gateway for v0.

#### Message processor and unified models

- https://github.com/RawsTourix/internet-search-bot/blob/main/src/core/message_processor.py
- https://github.com/RawsTourix/internet-search-bot/blob/main/src/core/models.py

Useful ideas:

- normalized request/response envelope;
- separation between client transport and agent processing.

#### LLM/tool loop and MCP client

- https://github.com/RawsTourix/internet-search-bot/blob/main/src/bots/main_bot/mcp_client.py
- https://github.com/RawsTourix/internet-search-bot/blob/main/src/api/api.py

Useful ideas:

- iterative model/tool execution;
- tool result handling;
- provider/tool error paths;
- existing practical code to mine rather than redesign basic mechanics from zero.

Do not copy wholesale: the lab runtime should have a much smaller tool abstraction and stronger experiment instrumentation.

When code is actually adapted, record the exact source commit/path in a third-party/provenance note.

### Empirical traces

Sanitized research excerpts currently live in the optimization-course repository:

- https://github.com/rosbiotech-studies/optimization-and-system-modeling/tree/main/lab_context/traces

Role:

- reference workloads;
- context growth/compaction examples;
- seed for benchmark-case design.

Raw private exports must not be copied into this public repository.

## 2. 5R-AXIS Agent

Repository:

- https://github.com/5r-axis/agent

Primary research input:

- https://github.com/5r-axis/agent/blob/research/context-residency-management/docs/research/context-residency-management-research-v1.md

Useful concepts:

- model-facing context is distinct from conversation/state/memory;
- bounded immutable ContextProjection per model call;
- source ownership and provenance;
- ContextUnitRef-like addressing;
- ContextProjectionManifest;
- PIN / RELEASE / EVICT / RECALL distinction;
- `evict != delete`;
- provider-neutral context construction;
- dynamic context residency as a later research layer.

Boundary:

- Agent Context Lab is an independent experimental harness.
- 5R-AXIS research is design input, not a runtime dependency.
- The private 5R-AXIS repository currently has no repository license declared; do not copy its implementation into this public repository unless reuse/licensing is explicitly resolved.

## 3. Optimization and System Modeling coursework

Repository:

- https://github.com/rosbiotech-studies/optimization-and-system-modeling

Laboratory context:

- https://github.com/rosbiotech-studies/optimization-and-system-modeling/tree/main/lab_context

Role:

- academic problem statement;
- static binary selection model;
- terminology/evidence relevant to laboratory works;
- real-trace reference material.

The research harness should be useful beyond the course; coursework files are not runtime dependencies.

---

# Context-management research

## 4. MemGPT

Paper:

- https://arxiv.org/abs/2310.08560

Key input:

- virtual context management;
- main context vs external context;
- paging analogy;
- retrieval of out-of-context information when needed.

Use as conceptual prior art, not an architecture template.

## 5. Letta

Project/docs:

- https://github.com/letta-ai/letta
- https://docs.letta.com/

Relevant concepts:

- structured memory/context blocks;
- attaching/detaching information from model-visible context;
- persistent information outside a single immediate prompt;
- context/memory tooling.

Useful comparison target for later residency experiments.

## 6. Letta Context-Bench

Research/leaderboard:

- https://leaderboard.letta.com/
- https://www.letta.com/blog/context-bench/
- https://www.letta.com/blog/context-bench-skills/

Relevant methodology:

- agentic filesystem/context retrieval;
- multi-step entity/fact tracing;
- synthetic/fictional entities to reduce contamination;
- known ground-truth answers;
- evaluation of loading useful context without polluting the window.

Useful input for benchmark-case design, especially controlled filesystem scenarios.

Do not assume its rubric/task generator is directly suitable for our scorer-vs-selector causal questions.

## 7. ACON — Agent Context Optimization

Paper:

- https://proceedings.mlr.press/v306/kang26b.html

Code:

- https://github.com/microsoft/acon

Why highly relevant:

- peer-reviewed ICML 2026 work specifically on context compression for long-horizon agents;
- evaluates task success together with peak-token reduction;
- uses success/failure trajectory contrast to improve compression guidelines;
- separates context-management machinery from the underlying task agent.

Difference from our initial research question:

- ACON focuses on learned/natural-language compression policies;
- Agent Context Lab starts with explicit context elements, utility scoring and constrained subset selection.

Potential later use:

- representation/compression baseline;
- compare selection-only vs compression/summary strategies;
- study context-policy adaptation from failure trajectories.

## 8. Scroll — Context as an Environment

Paper/preprint:

- https://arxiv.org/abs/2608.21690

Relevant concepts:

- append-only event log as durable history;
- small model-visible working projection;
- off-context information remains queryable/recoverable;
- exact addressability of evicted history;
- programmatic materialization rather than always serializing history.

Status note:

- recent preprint; useful design evidence, not a settled standard.

Strong conceptual overlap with later Agent Context Lab residency/replay work.

## 9. Context-Folding

Paper:

- https://arxiv.org/abs/2510.11967

Key input:

- branch into a sub-trajectory;
- complete a subtask;
- fold intermediate trajectory into a smaller retained result;
- evaluate long-horizon agents under much smaller active context.

Useful as a later comparison for representation/compaction strategies.

## 10. LLMLingua / LongLLMLingua

Papers:

- https://aclanthology.org/2023.emnlp-main.825/
- https://aclanthology.org/2024.acl-long.91/

Relevant concepts:

- explicit compression budget;
- token-level/coarse-to-fine prompt compression;
- long-context key-information density;
- compression can affect both cost and quality.

Role here:

- future RepresentationPolicy/compression baselines;
- evidence that "selection" and "representation compression" are distinct research dimensions.

Do not import token-level compression into v0 static subset selection.

## 11. RECOMP

Paper:

- https://proceedings.iclr.cc/paper_files/paper/2024/hash/bda88ed2892f5e61c9a9bf215c566913-Abstract-Conference.html

Code:

- https://github.com/carriex/recomp

Relevant concepts:

- extractive vs abstractive context compression;
- selective augmentation (including returning no context when irrelevant);
- task-quality-aware compression.

Useful future comparison for retrieved/document context.

---

# Evidence about long-context behavior

## 12. Lost in the Middle

Paper:

- https://aclanthology.org/2024.tacl-1.9/

Key evidence:

- long-context performance can depend strongly on where relevant information appears;
- beginning/end positions can outperform the middle;
- having a longer nominal context window does not imply robust use of all positions.

Project impact:

- ordering must be fixed/versioned in selection experiments;
- add position-stress benchmarks rather than treating context as an unordered set.

## 13. RULER

Paper/repository:

- https://arxiv.org/abs/2404.06654
- https://github.com/NVIDIA/RULER

Relevant methodology:

- configurable synthetic context lengths;
- multiple retrieval/aggregation/multi-hop task families;
- distinguishes nominal from effective usable context.

Useful for synthetic scale/position benchmark inspiration.

## 14. LongBench / LongBench v2

Papers:

- https://aclanthology.org/2024.acl-long.172/
- https://aclanthology.org/2025.acl-long.183/

Relevant methodology:

- diverse long-context task families;
- document, dialogue, code repository and structured-data understanding;
- realistic tasks complement synthetic retrieval tests.

Potential use:

- later external validation or case-design inspiration.

Before importing any dataset, review license, evaluation format and whether it isolates the variable we actually want to test.

---

# Agent runtime / evaluation / observability prior art

## 15. AxisAgentic

Repository:

- https://github.com/XYZ-AI-Lab/AxisAgentic

Relevant 2026 architecture:

- extensible long-horizon agent runtime;
- append-only traces;
- reconstruction of model-visible state;
- replaceable model/tools/orchestrators/evaluators/policies;
- context budgets/compaction/recovery;
- trajectory metrics/provenance and replay.

Why useful:

> It independently validates the value of treating trajectory evidence and model-visible reconstruction as first-class runtime data.

Agent Context Lab remains smaller and focuses specifically on controlled context-management experiments.

## 16. Inspect AI

Project/docs:

- https://github.com/UKGovernmentBEIS/inspect_ai
- https://inspect.aisi.org.uk/

Relevant patterns:

- composable datasets, agents/tools and scorers;
- repeated evaluation/epochs;
- structured evaluation logs;
- live Inspect View;
- explicit cost/sample limits;
- post-run annotations/metadata with provenance.

Use as evaluation-harness prior art.

Do not automatically make Inspect a runtime dependency; first determine whether its abstractions fit the ContextProjection-specific experiment model.

## 17. MLflow Tracking

Docs:

- https://mlflow.org/docs/latest/ml/tracking/

Relevant patterns:

- experiment → run hierarchy;
- parameters/metrics/artifacts;
- searchable historical runs;
- visualization.

Use as experiment-tracking prior art.

Agent Context Lab still needs domain-specific call/projection/trajectory evidence that generic ML tracking does not define.

## 18. OpenTelemetry GenAI semantic conventions

Reference:

- https://github.com/open-telemetry/semantic-conventions-genai

Relevant patterns:

- inference/tool/agent spans;
- common semantic attributes;
- retry/logical-operation tracing.

Status:

- GenAI conventions are evolving/developmental.

Use as compatibility/reference input, not as the canonical research schema.

## 19. OpenInference semantic conventions

Reference:

- https://github.com/Arize-ai/openinference

Relevant patterns:

- LLM/embedding/retrieval/tool span kinds;
- tracing vocabulary for AI applications.

Same rule: useful mapping target, not project source of truth.

---

# Provider/framework context hooks

## 20. OpenAI Agents SDK

Repository/docs:

- https://github.com/openai/openai-agents-python
- https://openai.github.io/openai-agents-python/running_agents/

Relevant mechanism:

- `call_model_input_filter` edits fully prepared model input immediately before a model call;
- session/history callbacks provide another explicit context boundary.

Useful evidence for keeping model-input shaping as a separable hook.

Do not make the SDK the Cortex.

## 21. Anthropic / Claude context editing

Docs:

- https://platform.claude.com/docs/en/build-with-claude/context-editing

Relevant mechanisms:

- context editing/clearing;
- tool-result clearing for agentic workloads;
- compaction/context management.

Treat provider-native features as optional execution optimizations or future comparison policies, never as Agent Context Lab canonical semantics.

## 22. Model Context Protocol

Docs:

- https://modelcontextprotocol.io/
- https://docs.anthropic.com/en/docs/mcp

Role:

- optional standardized tool/data-source integration layer.

MCP is not required for v0. A minimal deterministic tool interface should be implemented first; MCP can be an adapter later.

---

# Optimization implementation references

## 23. SciPy MILP / HiGHS

Docs:

- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
- https://highs.dev/

Why useful for v0:

- direct mixed-integer linear programming API;
- SciPy `milp` uses HiGHS;
- exposes MIP diagnostics such as node count/gap;
- small implementation surface for the laboratory binary-selection model.

The solver remains replaceable behind ILPPolicy.

Solver/runtime performance claims must record versions/options/hardware.

---

# Adoption and evidence rules

## 24. Code adoption rule

Before reusing code from another repository:

1. verify its license;
2. record the exact source file and commit;
3. prefer adapting a small component over copying a subsystem;
4. preserve attribution/license terms where required;
5. add tests around changed semantics.

## 25. Architectural adoption rule

Before adopting an architectural idea:

1. state the problem it solves here;
2. distinguish observed source behavior from our inference;
3. benchmark the idea when feasible;
4. do not promote it to a project invariant merely because another framework uses it.

## 26. Scientific evidence rule

Distinguish:

- peer-reviewed research;
- preprints;
- vendor/project documentation;
- project blog/benchmark claims;
- our own empirical traces.

A useful idea may come from any of these, but its evidence strength must not be silently upgraded.

## 27. Watchlist

Recent work can be tracked without immediately influencing canonical design.

Candidate watch topics:

- self-evolving context-management policies from trajectories;
- cache-aware context policies;
- tool-schema selection/retrieval;
- learned residency/fault-driven policies;
- context-policy transfer across models/tasks.

Move a watch item into the main registry only when it materially affects a planned experiment or design decision.
