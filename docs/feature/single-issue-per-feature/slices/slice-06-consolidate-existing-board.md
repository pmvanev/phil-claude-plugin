# Slice 06 — Consolidate the existing board — SUBSUMED BY SLICE 07

**Retired 2026-08-14, before implementation.** Kept rather than deleted, because *why* the scoping was wrong
is the useful part.

## What it said

Consolidate this repo's board: turn each existing feature-plus-slice-cards group into a single feature card,
guarding against closing children inflating a parent's rollup to 100%.

## Why it was mis-scoped

Slice 01 read the real board and found **every slice card already closed** — `session-handoff` #9 with
#11/#10/#12, `groom-issues` #5 with its own, all done. So this slice had almost nothing live to consolidate,
and the hazard it was built around is moot for parents already closed.

Then the owner named the case the brief had missed: **the skill ships to consumers**, whose boards carry
old-paradigm structure that the retired rules actively produced. That is not a one-time migration of one
board — it is a **defect class the oracle has to learn to see**, and none of the four existing set-level
classes fires on it.

## Where its substance went

[`slice-07-decomposed-feature-class.md`](slice-07-decomposed-feature-class.md), which carries all three of
its hazards, its SPIKE (run and passed), and the class definition it lacked.

**The lesson worth keeping:** this brief scoped a capability to the one board it could see. A slice written
against the local instance of a general problem solves the instance and ships the problem.
