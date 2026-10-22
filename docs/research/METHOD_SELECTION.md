# Method selection for the static context problem (Lab 3)

**Status:** method-comparison and implementation guidance; selection of the primary policy is provisional pending evidence.

## Problem being solved

For eligible optional elements with given nonnegative utility estimates `v_i`, integer token costs `s_i > 0`, optional budget `B >= 0`, and binary choices `x_i`:

```text
maximize    sum_i(v_i * x_i)
subject to  sum_i(s_i * x_i) <= B
            x_i in {0,1}, i=1..N
```

Mandatory instructions, policy and current-task constraints are reserved before optional selection. Eligibility/security filtering precedes scoring and selection. This is a **static 0–1 knapsack instance**, a special case of binary integer linear programming (ILP / MILP), not unconstrained optimization or a multi-step Markov decision process.

Base dimension: **N binary decision variables; one functional budget constraint** (plus separately stated variable domains). A small illustrative fixture never limits N for the general formulation.

The optimizer does **not** choose the estimates `v_i`; their identification is a separate stage. It can certify an optimum **given** the selected surrogate scores, token estimates and declared restrictions; it cannot certify maximum downstream model quality.

## Methods worth explaining

| Method | Applicability | Advantages | Limitations / correctness |
| --- | --- | --- | --- |
| Exhaustive enumeration | Finite N | Exact reference on tiny instances; regression oracle | `2^N` combinations; not a scalable production method |
| Greedy by utility / utility per token | Same base input | Transparent fast baseline | Does not generally find the 0–1 optimum |
| Dynamic programming over token capacity | Integer weights and B | Exact for the one-budget knapsack; straightforward comparison | `O(NB)` time, typical `O(B)` value memory (solution reconstruction may require more); pseudo-polynomial in numeric B; more constraints complicate state |
| Branch-and-bound | Binary knapsack/ILP | Exact when completed; can prune using bounds | Worst-case exponential; speed depends on instance and bounds |
| Branch-and-cut in an ILP/MILP solver | Generalized linear constraints | Handles extended integer-linear models; solver diagnostics/status, gap/time limits | More machinery and solver overhead; not uniformly faster than specialized DP |
| Continuous LP relaxation alone | Relaxed `0<=x_i<=1` | Gives a bound and aids ILP techniques | Fractional solutions may be invalid as final context selection |

**No unsupported blanket claim:** “many variables imply cut generation is always better” is false as a general method rule. Evaluate the declared instance family, its budget, possible additional constraints and runtime limits.

## Defensible baseline decision

Use an `ILPPolicy` adapter (initial candidate: `scipy.optimize.milp` / HiGHS) as the **general extensible exact-method baseline**, retaining solver status and gap. Describe the underlying family as branch-and-bound / branch-and-cut as supported by actual solver documentation/version; do not claim a specific internal search path without evidence.

Add a **knapsack DP research comparison** if justified, without making it a mandatory dependency for the Lab 3 write-up or changing the accepted design. For a pure one-constraint integer-weight instance, DP can be competitive or superior; the benchmark determines the practical trade-off.

Greedy is a baseline, not evidence that optimizing the surrogate always improves downstream quality. Exact/DP methods should be compared against brute force on small fixtures before testing larger instances.

## Known reproducible fixture from Lab 2

The seven **synthetic, illustrative** items of the approved mathematical formulation:

| i | size `s_i` (tokens) | utility `v_i` (points) |
| ---: | ---: | ---: |
| 1 | 720 | 9 |
| 2 | 640 | 8 |
| 3 | 450 | 7 |
| 4 | 900 | 2 |
| 5 | 780 | 9 |
| 6 | 950 | 1 |
| 7 | 380 | 6 |

Optional budget: `B = 2400` tokens; mandatory payload is already reserved.

- Exact optimum: choose **1, 3, 5, 7**, total **2330 tokens**, surrogate utility **31**.
- Greedy by descending `v_i/s_i`, with original-index tie break (1 before 2): choose **1, 2, 3, 7**, total **2190 tokens**, surrogate utility **30**.
- Enumerating `2^7 = 128` subsets is a simple independent regression check. Do **not** mistake this textbook example for empirical agent quality or a claim about actual token counts.

Required test expectation: a valid exact solver returns utility 31 and weight <= 2400 for this fixture, or a clearly classified time-limit/gap status if artificially constrained. Reject results that cannot satisfy hard constraints.

## Scaling and benchmark discipline

Separate two experiments:

1. **Pure optimization scaling (no LLM needed).** Deterministically generate integer `s_i` and fixed-scale `v_i` for controlled sweeps over N and B. Record seed, generator, distribution, number of constraints, solver/algorithm and options, hardware, wall time, memory (where measurable), objective, bound/gap, feasibility and status. Vary one factor at a time; compare DP and ILP only when assumptions match. Synthetic data here are **not identified coefficients** for a real agent.
2. **Actual agent outcome experiment.** Hold the runtime/model/tools/evaluator/representation/order/elementization and case fixed while changing policy/scorer as declared. Evaluate task result quality and input/total system tokens, including scoring and solving overhead. Repeated stochastic runs and provider drift controls belong here.

Never fabricate scale ceilings (“N >= 1000 is impossible”) or solver timings; those must come from executed runs.

## Critical implementation invariants

- `B` is the optional selection budget *after* capacity reservation for protocol/tool-schema/fixed and mandatory content, and (where appropriate) output space. If fixed/mandatory exceeds capacity, emit an infeasibility classification; do not drop protected content.
- Additive `s_i` is an estimate, not guaranteed actual serialized prompt cost. Count final provider-facing request with the declared tokenizer/serializer; if it exceeds capacity, emit `budget_infeasible_after_serialization` (or a separately versioned repair treatment), not silent truncation.
- Tool-call/result linkage, role ordering and other provider structural constraints must be satisfied in materialization. A mathematically feasible set is not necessarily an admissible provider request.
- Utility additivity and item independence are **assumptions**. Redundancy, complementarity, prerequisite relations and privacy/eligibility may require extended models or experiments; do not sneak them into the base 0–1 equation.
- Handle solver statuses correctly: feasible incumbent with a nonzero gap is **not** a proven optimum; time limit != infeasibility; provider error != task failure.
- Changing the tokenizer, scorer, item granularity, generator, dependencies or model serialization creates a **new experiment version**; prior results remain immutable.

## Not part of the initial method decision

- A specific LLM-scoring prompt or learned utility predictor;
- an end-to-end commercial agent;
- provider-native compaction as if equivalent to the same selector;
- dynamic source eviction/recall;
- a global claim that one policy maximizes real-world task success.

See [Teaching requirements](TEACHER_REQUIREMENTS.md), [Coursework alignment](COURSEWORK_ALIGNMENT.md), [Benchmark](BENCHMARK.md) and [Experiment design](EXPERIMENT_DESIGN.md).
