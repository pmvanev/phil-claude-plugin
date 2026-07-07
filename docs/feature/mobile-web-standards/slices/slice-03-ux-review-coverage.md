# Slice 03 — `/phil:ux-review` covers the mobile always-flag items

**Goal.** Extend the audit command so the on-demand review touchpoint (T3) catches the new mobile
always-flag defects, not only in-flow editing (T1/T2).

**Story:** US-03 · **Job:** catch-ux-violations-while-building-ui (mobile facet)

## IN scope
- Add the 5 US-01 mobile always-flag classes to the must-fix list in `skills/ux-review/SKILL.md`,
  each tracing to a `ux.md` principle + WCAG SC.
- Mark reflow/zoom items "verify at runtime" (they depend on rendered output).

## OUT scope
- Any new flag not present in `ux.md` after Slice 1 — the skill mirrors the rule, never leads it.
- Changes to the backlog file format or command argument parsing.
- `commands/ux-review.md` behavioural change beyond what the SKILL.md list drives.

## Learning hypothesis
Disproves "the audit skill can mirror the new rule items 1:1 without inventing flags or drifting
from `ux.md`" **if** review finds a must-fix item in the skill with no corresponding `ux.md` line.

## Acceptance criteria
See US-03 ACs in `feature-delta.md`. Trace check: every added must-fix item ↔ a `ux.md` line.

## Dependencies
- **Hard:** Slice 1 must land first — the skill mirrors `ux.md`, so the rule items must exist.

## Effort / reference class
≤ 0.5 day. Reference class: editing the must-fix enumeration in an existing SKILL.md.

## Pre-slice SPIKE
None.
