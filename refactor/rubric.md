# Refactor-Loop Frozen Rubric

Authored once, frozen, committed, and applied to every proposal. Critics read it and apply
it as written — they do not re-improvise their standard per call. That is what makes their
verdicts order-invariant.

This rubric is analytic, not holistic: criteria are scored individually, with behavioral
anchors instead of adjectives. Where a criterion can be binary, it is.

> **Frozen + regression-tested.** This file changes only on the slow clock, by a human who
> owns construct validity. Every edit to it is non-monotonic — a change that helps one axis
> can silently cost another. So any change to this rubric is regression-tested against the
> critic self-test suite in `refactor/self-test/` before it ships, never eyeballed. See
> that directory's README for how the gate runs.

## Scoring rules (apply to every criterion)

- **Binary where possible.** Prefer `met: true/false`. Reserve graded scores for criteria
  that genuinely need them, and give those a narrow 3-level ordinal with anchors.
- **Behavioral anchors, not adjectives.** "reduces nesting depth below the original" beats
  "good style."
- **Per-criterion explanation is mandatory.** Justification is written before the verdict.
- **`CANNOT_ASSESS` abstention.** A criterion the critic cannot judge from the diff abstains
  rather than guessing.
- **Anti-flattery clause.** A verdict of generic praise with no `span` is coerced to
  `CANNOT_ASSESS`, never `accept`.
- **Negative-weight anti-patterns.** The items marked *(anti-pattern, negative weight)* dock
  the verdict when present — they counter leniency. A diff that introduces one cannot be a
  clean `accept`.

## Verdict mapping

| Condition | Verdict |
|---|---|
| All active criteria `met`, no anti-pattern present | `accept` |
| A fixable criterion fails (`severity` minor/major, behavior-preserving fix exists) | `revise` |
| The refactoring is wrong in kind (changes behavior, wrong target) | `reject` |
| The critic cannot point to a span supporting its judgment | `CANNOT_ASSESS` |

The orchestrator routes on `verdict + severity + confidence` with threshold **θ = 0.6**: an
item of `severity ≥ major` at `confidence ≥ 0.6` blocks an `accept` and back-prompts the
proposer.

---

## Slice 1 — Correctness / Behavior  *(ACTIVE in v1)*

Owner: `refactor-critic-correctness`. References `~/.claude/rules/refactoring.md`
(Definition: tests pass before and after) and `~/.claude/rules/testing.md`. Named
refactorings are drawn from `~/.claude/rules/refactoring-catalog.md` so critic and proposer
share one dictionary.

| Criterion | Type | Test (behavioral anchor) | Kind |
|---|---|---|---|
| `behavior-preserved` | correctness | Every input/output and side effect observable in `original_code` is observable, in the same order, after the diff. | binary |
| `public-api-unchanged` | correctness | No exported/public symbol is added, removed, renamed, or has its signature changed — unless `public_api_touched: true` was declared and the change is the stated intent. | binary |
| `single-named-refactoring` | scope | The diff is exactly one named refactoring from the catalog, not a bundle and not a behavior change smuggled in as structure. | binary |
| `no-behavior-change-smuggled` | correctness | The diff does not fix a bug, add a feature, or alter control flow outcomes under the guise of refactoring. | binary |
| `side-effect-order-preserved` | correctness | I/O, logging, mutation, and exception timing occur in the same order relative to observable boundaries. | binary |
| `error-paths-preserved` | correctness | The same exceptions are raised for the same inputs; no error path is swallowed or broadened. | binary |
| `extracted-unit-single-responsibility` | structure | An extracted function/variable does one thing; its name reveals intent. | graded (3) |
| `tests-not-weakened` *(anti-pattern, negative weight)* | correctness | The diff does not touch, delete, or relax any test — that is the proposer's hard boundary and a hook-blocked write. | binary |
| `no-lateral-churn` *(anti-pattern, negative weight)* | scope | The diff does not rename/reshuffle unrelated code to look productive. | binary |
| `no-hallucinated-abstraction` *(anti-pattern, negative weight)* | structure | No interface/indirection is introduced with only one caller and no present need (speculative generality). | binary |
| `no-broadened-surface` *(anti-pattern, negative weight)* | correctness | The public surface is not widened (new exports, loosened visibility) beyond the declared intent. | binary |

Graded anchor for `extracted-unit-single-responsibility`:

- **met** — the unit has one responsibility and an intention-revealing name.
- **partial** — one responsibility but a weak/encoded name (route to `revise`).
- **not-met** — the unit still does more than one thing (route to `revise` or `reject`).

---

## Slice 2 — Idiom / Readability  *(STUB — activated in v2)*

Owner (v2): `refactor-critic-idiom`. Will reference `~/.claude/rules/coding.md` and the
path-scoped language idiom files `~/.claude/rules/cpp.md`, `~/.claude/rules/python.md`,
`~/.claude/rules/typescript.md`, `~/.claude/rules/react.md` (a `.tsx` file is judged against
both TypeScript and React rules).

Not active in v1. v1 ships a single correctness critic; the disjoint idiom slice is earned,
not default (ADR-002). When v2 adds the idiom critic, populate this slice with binary/graded
criteria such as: preferred-constant-form, no-mutable-default-argument, no-bare-except,
`unknown`-over-`any`, no-floating-promise, no-array-index-key, no-conditional-hook — each
with the preferred form named from the matching idiom file, and idiom violations that are
genuine correctness hazards promoted into Slice 1.

> Activation trigger (ADR-001/§7): add this critic only when the §6.3 human spot-check shows
> the single correctness critic recurrently misses an idiom class — measured, not speculated.

---

## Slice 3 — Architecture / Coupling  *(STUB — activated in v2)*

Owner (v2): `refactor-critic-architecture`. Will reference `~/.claude/rules/architecture.md`
and `~/.claude/rules/refactoring.md` §Economics (Constantine's equivalence: change cost =
coupling cost).

Not active in v1. When v2 adds the architecture critic, populate this slice with criteria
such as: dependency-direction-points-inward, no-new-dependency-cycle, cohesion-not-reduced,
abstraction-levels-not-mixed, no-speculative-generality — behavioral anchors quoting the
architecture guide, anti-patterns negative-weighted.

> The panel earns its tokens only because the three slices partition the concern space —
> three copies of one rubric mostly agree and waste tokens. Do not activate Slices 2–3 until
> v1 has proven convergence on a real package.
