# Coursework alignment

**Status:** working source-grounded map, not a substitute for the teacher's assignment.
**Academic source index and uncertainty rules:** [TEACHER_REQUIREMENTS.md](TEACHER_REQUIREMENTS.md).
**Method and scaling argument for Lab 3:** [METHOD_SELECTION.md](METHOD_SELECTION.md).

Agent Context Lab is broader than the seven laboratory reports. The course receives **specific, inspectable deliverables** from the harness; research infrastructure must not change what the teacher asked for. A minimal stand-alone implementation must support completion even if 5R-AXIS never becomes runnable.

## Semester 1: establish the model

### Laboratory work 1 — subject domain and problem

- Describe the information available to a multi-step AI agent and the smaller actual context sent for one model call.
- Explain the quality-versus-resource problem and why naive maximal truncation is not acceptable.
- No running agent, solver, scorer or benchmark is needed to justify the problem.

### Laboratory work 2 — mathematical formulation

For eligible optional context elements:

```text
x_i ∈ {0,1}             binary decision to include item i
s_i > 0                 estimated item token cost
v_i >= 0                estimated item usefulness for current task
B >= 0                  remaining optional-token budget
N                       number of optional candidates

maximize Σ(v_i x_i)
subject to Σ(s_i x_i) <= B
```

Mandatory instructions and current-task constraints are included/reserved outside optional selection. In the base static formulation: **N binary decision variables, one functional budget constraint**, with variable domains stated separately. Neither the academic fixture size nor the presence of just one constraint limits N in the general model.

Interpretation:

- `s_i` is a controlled additive cost *estimate*; account separately for serialized overhead and actual input tokens.
- `v_i` is a surrogate utility estimate, **not** observed final task quality.
- The additive objective ignores real dependencies/redundancy unless an explicitly extended model accounts for them.
- Changing tokenization, representation, elementization or order changes the experiment and must be versioned.

Seven-item teaching fixture and exact expected objective: [METHOD_SELECTION.md](METHOD_SELECTION.md). The fixture is synthetic, not measured agent telemetry.

### Laboratory work 3 — choice and applicability of solution method

**Teacher-side deliverable:** classify the formulated problem, compare applicable methods, explicitly quantify mathematical dimension and argue a method's computational suitability. A report should emphasize **why** a method is applicable and what limits it, rather than reproducing a long manual algorithm.

**Lab contribution:**

- the base problem is 0–1 knapsack / binary integer linear optimization;
- compare greedy heuristics, dynamic programming and integer programming with branch-and-bound / branch-and-cut;
- `ILPPolicy` with a versioned MILP solver is the proposed extensible default, not a claim that it is always fastest;
- classic DP over integer capacity can be exact in `O(NB)` time, and B/state-space size matters;
- avoid claiming that merely increasing N makes continuous LP NP-complete or that any method is universally optimal for speed.

**Research extension, not an established teacher requirement:** build a no-LLM deterministic large-N/B generator, record status/gap/time/solver version/hardware, and empirically compare implementations. This supports the method justification and later work but must not be described as a mandatory live-provider experiment for Lab 3.

## Semester 2: turn the model into a demonstrable process

The four roles below follow the lecturer's description in Lecture 002 (see [primary transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-002/sources/raw-transcript--RawsTourix.txt)). Update them if a newer official assignment provides different requirements.

### Laboratory work 4 — object / business-process description

**Educational deliverable:** a clear model of the *process being optimized*, not merely a dataset.

Project contribution:

- describe one agent iteration as an observable process: task + allowed sources → mandatory/optional classification → parameterization/scoring → selection → valid model-facing serialization → model/tool execution → outcome;
- identify actors/owners, incoming data, outgoing artifacts, decision points, exceptions and feedback/measurement;
- provide a process diagram and accompanying narrative; it may use fixture tools and a ScriptedModel, with no production agent dependency.

Benchmark datasets and trace-derived scenarios are supporting material, **not a replacement** for the required process description.

### Laboratory work 5 — parameter identification

**Educational deliverable:** defensible numeric coefficients and how they are obtained.

Project contribution:

- `s_i`: specify tokenizer/serializer basis, units, actual measurement or estimated value, and uncertainty;
- `B`: define how mandatory/fixed content, protocol/tool schemas and usable capacity are accounted for;
- `v_i`: define a repeatable estimation protocol and its limitations; consider deterministic heuristic, oracle-labeled *development/test* fixture, embedding or LLM scorer as separate research variants;
- record scoring scale, source of labels, provenance, version, error/calibration where measurable and scorer overhead.

Do not infer `v_i` from hidden evaluation labels in ordinary policies. Synthetic classroom values are not automatically measurements. Parameter identification is distinct from “solver returns optimum”.

### Laboratory work 6 — interface for input and output

**Educational deliverable:** a **usable input/output interface** for the optimization task. Merely shipping a library API or a read-only dashboard is not equivalent unless the teacher accepts it.

Minimum interaction: enter/import candidate elements, sizes, usefulness estimates, mandatory context/budget and select a policy; validate data, execute a solve and display selection `x_i`, objective, token consumption, spare budget, feasibility/solver status and understandable validation errors.

Project contribution: a small CLI or local UI backed by the *same* schemas/solver/fixtures, optionally integrated into the Research Workbench. Keep source-of-truth contracts and model-independent semantics; avoid prematurely building a general user chat interface.

### Laboratory work 7 — solve the optimization problem

**Educational deliverable:** run a completed instance and show the actual optimization solution, explaining its result, feasibility and boundary conditions.

Project contribution:

- take specified input → invoke a documented method → show selected elements and totals;
- verify constraints, distinguish optimum vs feasible incumbent vs infeasible/failed run;
- preserve the model/parameter/solver versions used;
- optionally accompany the solution with research benchmark and comparative task-quality measurements.

The full policy/scorer benchmark is valuable for the course project and later research, **but it supplements rather than replaces** the teacher's requested solution.

## Research beyond the minimum academic requirements

The harness separately supports:

- deterministic and real-provider model/tool cases;
- trace-derived (sanitized) workloads;
- versioned ContextProjection manifests, append-only runs and replayable comparisons;
- scorer vs selector error separation and quality floors;
- provider usage/cost/latency plus selector/scorer overhead;
- development/test split and repetition where appropriate;
- optional dynamic residency `PIN / RELEASE / EVICT / RECALL` with exact source references and provenance.

Do not make an external agent, expensive LLM calls, long-term memory, vector database or 5R-AXIS integration a blocker for *any* of the seven lab deliverables.

The central empirical research question remains:

> How much context/system cost can be reduced **without unacceptable downstream task-quality loss**?

ILP solution optimality is relative to specified surrogate values/constraints, not a guarantee of task success. See [Benchmark](BENCHMARK.md), [Experiment design](EXPERIMENT_DESIGN.md), and [Observability](OBSERVABILITY.md).
