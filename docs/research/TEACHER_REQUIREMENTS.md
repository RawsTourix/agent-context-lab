# Teaching requirements and research-harness implications

**Status:** source-grounded academic guidance; not a replacement for an official assignment or a verbatim transcript.
**Scope:** optimization and system modeling laboratory sequence, with coursework as the downstream deliverable.

## Evidence and interpretation policy

Keep three layers separate:

1. **Teacher guidance from raw lecture transcripts.** Use it to identify the required educational result; oral wording may be informal and automatic transcription may be wrong.
2. **Coursework mapping.** A working interpretation of what each laboratory report must deliver. Reconcile it with any later assignment from the teacher.
3. **Agent Context Lab engineering decisions.** Reproducibility, traces, provider abstraction, benchmarks and implementation choices are *our research protocol*, not teacher mandates.

Do not quote uncertain transcribed fragments as exact words. Do not present a summary note as a primary source.

### Primary-source index (as available on 2026-10-22)

- [Lecture 002 — original transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-002/sources/raw-transcript--RawsTourix.txt) — mathematical problem formulation, identification of coefficients and the subsequent sequence of lab tasks.
- [Lecture 004 — original transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-004/sources/raw-transcript--RawsTourix.txt) — dimension, functional constraints and method applicability.
- [Lecture 005 — original transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-005/sources/raw-transcript--RawsTourix.txt) — Bellman-style dynamic programming, states and dimensionality.
- [Lecture 006 — original transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-006/sources/raw-transcript--RawsTourix.txt) — justifying the method of finding an optimum, without substituting a lengthy manual algorithm derivation for the task argument.
- [Lecture 007 — original transcript](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-007/sources/raw-transcript--RawsTourix.txt) — aggregation/dimension reduction and caveats of subjective importance coefficients.
- [Lecture 002 — teacher-guidance notes](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/lecture-002/sources/teacher-guidance--RawsTourix.md) — secondary summary.
- [Lab-context guidance](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/other-001-lab-context/work/teacher-guidance.md) — secondary, interpretive synthesis, not literal speech.
- [Base research problem](https://github.com/rosbiotech-studies/optimization-and-system-modeling/blob/main/other-001-lab-context/work/problem-v1.md) and [sanitized traces](https://github.com/rosbiotech-studies/optimization-and-system-modeling/tree/main/other-001-lab-context/work/traces) — project context and empirical *orientation*, not grading criteria or ground truth.

The full context of the original utterances takes precedence over paraphrased excerpts. If official laboratory assignment instructions disagree with this map, review and update the map before claiming compliance.

## What matters for laboratories 1–3

- **Lab 1: subject domain and optimization problem.** Describe where the problem arises and why excess context and excessive exclusion are both undesirable. Do not promise a particular implementation.
- **Lab 2: mathematical formulation.** Distinguish indices, available data/parameters, decision variables, their domains, objective function, functional constraints and output. The minimal static model can be a one-budget 0–1 knapsack over optional context elements. Mandatory information is reserved outside optional selection.
- **Lab 3: choice and reasoned applicability of the optimization method.** Classify the problem, count actual decision variables and functional constraints after expanding indexed families, compare *applicable* methods, consider computational cost/limitations, and justify a method for this particular model. Understand why/when it works rather than manually coding or solving a large algorithm.

Lecture guidance emphasizes that a compact classroom example is compatible with an arbitrary-size general model: the example's seven elements do **not** imply seven is the production limit.

**Do not overstate the assignment:** a timing/scalability experiment is valuable research evidence, but the available transcripts do not establish that a complete live-provider benchmark or hand-coded optimization algorithm is *mandatory* for Lab 3. The method argument can be completed before such experiments, with empirical verification recorded as a distinct planned research task.

## Lecturer's later-semester sequence (working interpretation)

Lecture 002 explains a continuation along these functional lines:

| Laboratory | Educational deliverable | Research-harness support, without replacing the deliverable |
| --- | --- | --- |
| 4 | **Description of the object / business process** | Reproducible diagram and narrative of agent context formation, actors, data flows, decision points, inputs and outputs |
| 5 | **Identification of mathematical-model coefficients** | Account for optional element sizes `s_i`, budget `B`, and utility estimates `v_i`: origin, units, estimation method, validity and error |
| 6 | **Interface for data input and output** | A minimal usable interface that accepts/validates problem parameters and presents selected elements, objective, budget and solver status |
| 7 | **Solving the optimization task** | Connect input → solver → result with a verifiable working example, infeasibility/error handling and evidence |

The broader Agent Context Lab benchmark, replay viewer and comparative research are supplementary and reusable. They must **not displace** the business-process description (Lab 4) or the input/output interface (Lab 6).

## Cross-cutting teacher emphasis

- Count the **number of decision variables** and **number of functional constraints**, not just constraint *types*. In the base model: `N` binary variables and one budget constraint; domains `x_i ∈ {0,1}` are stated separately. An extended indexed constraint family must be counted after expansion.
- Computational applicability depends on **method and instance structure**, not a magical variable threshold. State limitations, do not claim one solver is universally fastest.
- If considering dynamic programming, estimate **state-space size**. For integer token weights and integer `B`, a classic weight-indexed DP can require `O(NB)` time: this is pseudo-polynomial, not polynomial in the bit length of `B`.
- Coefficients have meanings, units, sources and measurement errors. For the present model `s_i` is a token cost estimate and `v_i` is a *surrogate* of usefulness; actual task quality is measured separately. Unsupported or inconsistent coefficients can invalidate the practical result despite a mathematically correct optimum.
- Keep formula/parameter provenance and references from the beginning. Cite original technical sources and observed data; synthetic example coefficients are labeled synthetic, never passed off as measurements.
- Distinguish model applicability from empirical performance. A solver optimality certificate refers to the formulated surrogate objective, **not guaranteed agent success**.

## Guardrails for developers

- Treat the static selection task as an intentionally restricted first case. Do not require full 5R-AXIS, an external agent framework, an LLM-based scorer, live network tools or a paid model to complete coursework.
- Build a deterministic path first; include tests for a known optimal seven-element fixture, an infeasible mandatory-context case and serializer-budget overflow.
- Do not silently mutate the model to make a demonstration work (e.g. changing weight granularity, making required task constraints optional, or discarding protocol dependencies).
- Keep teacher deliverables mapped to distinct produced artifacts, while preserving the ability to extend experiments independently.
- Dynamic `PIN / RELEASE / EVICT / RECALL` and 5R-AXIS integration remain subsequent *research options*, not prerequisites for Lab 3 or Lab 7.

See [Coursework alignment](COURSEWORK_ALIGNMENT.md), [Method selection](METHOD_SELECTION.md), [Architecture](../design/ARCHITECTURE.md) and [Benchmark](BENCHMARK.md).
