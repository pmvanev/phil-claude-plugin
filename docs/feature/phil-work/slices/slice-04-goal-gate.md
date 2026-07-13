# Slice 04 — Initiative-goal gate: declare + check a per-initiative metric

**Goal:** FRAME captures a specific, checkable goal metric for the initiative (beyond behavior-preservation), and every wave — plus VERIFY — gates on it. `/phil:work` never claims "done" unless the metric is met.

## IN scope
- FRAME extended: the developer declares a goal metric appropriate to the work type
  (e.g. "God object split into ≥3 cohesive units", "dependency X removed", "p95 < 200ms",
  "cyclomatic complexity of module Y below N"). FRAME refuses to proceed on an uncheckable goal.
- The goal metric becomes an explicit gate alongside the preservation floor at each wave and at VERIFY.
- VERIFY reports goal-met vs goal-not-met with evidence; "not met" is reported honestly, never masked as done.
- Goal + per-wave metric readings recorded in the decision trail.

## OUT scope
- Broad skill routing across initiative types (slice 05) — goal metric is declared by the developer here, not inferred.

## Learning hypothesis
**Disproves** "goal-defined acceptance works for invisible work" **if** developers cannot state a checkable metric for real initiatives, forcing everything back to preservation-only.
**Confirms** the two-gate spine (preservation floor + declared goal) **if** real initiatives yield checkable metrics and the goal gate catches a run that preserved behavior but failed to achieve its point.

## Acceptance criteria
- On a real initiative, FRAME captures a checkable goal metric and rejects a vague, uncheckable one (or accepts explicit "behavior-preservation only").
- VERIFY reports goal-met/not-met with concrete evidence; a run that preserves behavior but misses the goal is reported as "goal not achieved," not "done."
- The decision trail shows the goal metric and its reading at VERIFY.

## Dependencies
- Slices 01–03.

## Effort estimate
~1 day. **Reference class:** the coverage-equivalence claim gate in `redesign-tests` (a declared, human-checked claim at a gate).

## Pre-slice SPIKE
None — the gate mechanism mirrors existing human-checked gates in the repo.
