# Review feedback on laboratory works 1–2 (October 2026)

**Status:** actionable review notes; **source is a screenshot of comments by Dmitry Ivliev dated 2026-10-08 and 2026-10-29, supplied by the student.** This is *not* a raw Novitsky lecture transcript and must not be represented as the instructor's verbatim requirements. Source screenshot was supplied in a conversation and is not committed here.

## Reviewer points and disposition

| Lab | Feedback | Accepted response |
| --- | --- | --- |
| 1 | Utility is mentioned without explaining what determines it, hence the comparison criterion is vague. | Define estimated *task-conditional usefulness*: expected contribution to completing the **current step**. Candidate evidence factors include relevance to task, reliability, recency, necessity for next steps. State that any numerical score requires a common, explicit scheme and later coefficient identification. Do not equate proxy `v_i` with downstream measured quality. |
| 1 | The selected portion's token budget must be clearly separate from the model context-window limit. | Define full model capacity and a deliberately chosen *optional* budget separately, including reservations for fixed and mandatory content (and output capacity when relevant). |
| 1 | Is mandatory information included in the optional budget? | **No in the accepted base model.** Mandatory content is included separately; `B` refers only to optional candidates. |
| 2 | `X*` is introduced but not formally defined as the optimizer. | State `X* ∈ argmax_{X ∈ D} F(X)`, with `D={X ∈ {0,1}^N: Σs_i x_i ≤ B}`. Multiple optimal vectors may exist. The optimizer returns a subset of optional candidates, not mandatory information. |
| 2 | The claim that `N` is not bounded by the seven-item example is unclear. | Replace with: “The mathematical formulation is defined for any positive integer `N`; `N=7` is used only to illustrate one numerical instance.” This is *mathematical generality*, not a guarantee of feasible computation for arbitrarily large N. |
| 2 | Integer nature of token sizes and budget was not specified. | Declare `N∈ℤ_{>0}`, `s_i∈ℤ_{>0}`, `B∈ℤ_{≥0}`. Both are measured or estimated token counts and remain integer-valued, while final serialized input may incur non-additive overhead. `v_i` can be nonnegative real-valued proxy points. |
| All | Reports should be assembled as one file under a single cover page. | **Submission packaging rule from reviewer feedback:** one document, one common title page; separate sections named “Лабораторная работа №1”, “№2”, etc. Do not insert individual title pages between works. Confirm final wording and numbering against explicit course instructions if provided later. |

## Suggested academic wording (Russian)

### Useful passage for Lab 1

> Полезность элемента контекста понимается как предварительная оценка его ожидаемого вклада в выполнение текущего шага задачи агентом ИИ. Такая оценка может учитывать соответствие информации текущей цели, её достоверность и актуальность, а также необходимость для последующих действий. Для сопоставления необязательных элементов каждому из них назначается числовая оценка полезности по единому правилу. На этапе постановки задачи способ получения этих оценок рассматривается как заданный; процедура их численного определения подлежит отдельному исследованию. Оценка полезности не тождественна фактически измеренному качеству ответа языковой модели.

> Контекстное окно модели характеризует техническую ёмкость информации, обрабатываемой при обращении к ней. Из доступной ёмкости заранее резервируется место для обязательных инструкций и сведений, служебного оформления запроса и при необходимости ответа модели. Бюджет `B` задаётся отдельно для выбираемых необязательных элементов; обязательная информация в `B` не включается. Поэтому величина `B` не равна объёму всего контекстного окна и не должна превышать остаток доступной ёмкости. Бюджет может быть дополнительно уменьшен для ограничения затрат.

### Useful passage for Lab 2

> Пусть `N∈ℤ_{>0}` — количество доступных для выбора необязательных элементов контекста, `s_i∈ℤ_{>0}` — размер i-го элемента в токенах, `v_i≥0` — его предварительная оценка полезности, `B∈ℤ_{≥0}` — бюджет токенов, выделенный только на выбираемую часть. Переменная `x_i∈{0,1}` показывает, включается ли элемент в контекст. Обязательные сведения учитываются отдельно при определении доступного бюджета.

> Множество допустимых решений: `D = { X∈{0,1}^N : Σ s_i x_i ≤ B }`. Оптимальным решением называется вектор `X*∈argmax_{X∈D} Σ v_i x_i`. Его компоненты определяют, какие необязательные элементы следует включить в формируемый контекст. Оптимальность относится к заданным оценкам полезности и ограничениям, а не гарантирует наилучшее фактическое качество результата агента.

> Математическая постановка определена для произвольного положительного целого `N`. В учебном числовом примере принимается `N=7` исключительно для иллюстрации расчёта; вычислительная применимость алгоритмов при увеличении `N` анализируется отдельно.

## Engineering contract derived from review

For Agent Context Lab:

1. Record `full_window_capacity` / effective input capacity, protocol+mandatory reservation, experiment-selected optional budget `B` **as distinct quantities**. Do not silently count mandatory context against optional `B` or silently discard mandatory segments.
2. Preserve scorer provenance: scale and evaluation protocol for `v_i`, task/call association, provenance and version. Later Lab 5 identifies coefficients, but the meaning must already be clear in Labs 1–3.
3. Use integral, nonnegative token budgets and positive integral per-element token counts at solver input. Estimated materialization cost is distinct from observed serialized/provider usage; do not claim additivity of the wire format.
4. Report `X*` as the optional-selection decision vector and verify feasibility and objective independently of the solver. Distinguish a proven optimum from a feasible incumbent under a time limit or MIP gap.
5. Keep report *packaging* in the academic deliverable toolchain, not the agent runtime. One cover page for combined lab reports should not affect Benchmark Case, ExperimentSpec or Cortex semantics.

## Reconciliation rule

These reviewer remarks improve clarity but cannot retroactively change the accepted mathematical research problem. If a later written assignment by Novitsky specifies a different meaning of budget or report packaging, reconcile and document that decision before editing both model and reports.

Related: [teacher guidance](TEACHER_REQUIREMENTS.md), [coursework alignment](COURSEWORK_ALIGNMENT.md), [method selection](METHOD_SELECTION.md), [concept model](../design/CONCEPT.md), [architecture budget accounting](../design/ARCHITECTURE.md).
