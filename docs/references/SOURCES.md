# Sources and reusable inputs

This registry distinguishes **code to inspect/reuse**, **architecture/research input**, and **external prior art**.

A link here does not mean the project copies that source's architecture.

## 1. RawsTourix / internet-search-bot

Repository:

- https://github.com/RawsTourix/internet-search-bot

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
- "evict != delete";
- provider-neutral context construction;
- dynamic context residency as a later research layer.

Boundary:

Agent Context Lab is an independent experimental harness. It must not silently make research-only 5R concepts canonical for 5R-AXIS.

## 3. Optimization and System Modeling coursework

Repository:

- https://github.com/rosbiotech-studies/optimization-and-system-modeling

Laboratory context:

- https://github.com/rosbiotech-studies/optimization-and-system-modeling/tree/main/lab_context

Role:

- academic problem statement;
- static selection model;
- terminology and evidence relevant to laboratory works;
- real-trace reference material.

The research harness should be useful beyond the course; coursework files are not runtime dependencies.

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

- structured memory blocks;
- attaching/detaching blocks from model-visible context;
- persistent memory outside a single immediate prompt;
- context/memory tooling.

Useful comparison target for later residency experiments.

## 6. OpenAI Agents SDK

Repository/docs:

- https://github.com/openai/openai-agents-python
- https://openai.github.io/openai-agents-python/running_agents/

Relevant mechanism:

- `call_model_input_filter` edits the prepared model input immediately before a model call;
- session input callbacks allow explicit history handling.

This is a useful example of keeping model-input shaping as a separable hook.

## 7. Anthropic / Claude context management

Docs:

- https://docs.anthropic.com/

Relevant ideas:

- long-horizon context management;
- compaction/state-saving workflows;
- tool results as a major contributor to context;
- server-side/dynamic filtering in selected tool flows.

Treat provider-native features as implementation optimizations, never as Agent Context Lab's canonical context semantics.

## 8. Context-Folding

Paper:

- https://arxiv.org/abs/2510.11967

Key input:

- branch into a sub-trajectory;
- complete a subtask;
- fold intermediate trajectory into a smaller retained result;
- evaluate long-horizon agents under much smaller active context.

Useful as a later comparison for representation/compaction strategies.

## 9. Model Context Protocol

Docs:

- https://modelcontextprotocol.io/
- https://docs.anthropic.com/en/docs/mcp

Role:

- optional standardized tool/data-source integration layer.

MCP is not required for v0. A minimal tool interface should be implemented first; MCP can be an adapter later.

## 10. Source adoption rule

Before reusing code from another repository:

1. verify its license;
2. record the exact source file/commit;
3. prefer adapting a small component over copying a subsystem;
4. preserve attribution where required;
5. add tests around changed semantics.

Before adopting an architectural idea:

1. state the problem it solves here;
2. distinguish observed source behavior from our inference;
3. benchmark the idea when feasible;
4. do not promote it to a project invariant merely because another framework uses it.
