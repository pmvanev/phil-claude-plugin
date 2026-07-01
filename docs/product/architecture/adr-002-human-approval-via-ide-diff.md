# ADR-002 — refactor-tests: human-approval oracle via IDE diff review; critic deferred

Status: accepted (DESIGN wave, 2026-07-01) · Feature: refactor-tests

## Context

For test refactoring the suite cannot be the safety oracle — the test *is* the oracle, so a
green run cannot prove an assertion was not weakened (DISCUSS D2). DISCUSS chose human approval
per diff. DESIGN must fix the *mechanism*: how the diff is surfaced and when the suite runs.

## Decision

**Apply-then-review, editor-first.** Per approved backlog item the loop:

1. Applies the single proposed structure-only move to the **working tree**.
2. Runs the suite as a sanity check. If red → `git checkout` auto-revert, mark the item
   blocked, continue (DD6) — the human is not bothered with a broken change.
3. If green → **pause** and ask the developer to review the *uncommitted diff in their
   IDE/editor* (against git), then answer a structured **approve / reject / skip / quit** prompt
   via AskUserQuestion. **No diff is printed in chat.**
4. Approve → commit (one commit per item). Reject/skip/quit → `git checkout` revert.

Never refactor on a red baseline (DD6). The **automated test-diff critic is deferred to slice
04**; the propose step leaves a clean pre-screen seam. A draft is recoverable at commit
`b29f6aa`.

## Alternatives considered

- **Print full diff in chat + confirm** — rejected: developers review diffs better in their
  editor against git; chat diffs are noisy, lossy, and duplicate the editor.
- **Propose-then-apply (apply only after approval)** — rejected: the developer could not review
  the *real* on-disk change in their IDE before deciding; apply-then-review gives a true diff
  and a trivial `git checkout` undo.
- **Build the critic now** — rejected: its value (reducing review burden) is only measurable
  once a working loop produces real burden data. Empirical over speculative (DD5).

## Consequences

- (+) Best-fit review UX; real diffs, real undo, structured + logged decision.
- (+) v1 matches the DISCUSS oracle exactly; critic slots in without rework.
- (−) A change briefly exists on disk before approval; bounded by the immediate
  suite-check + auto-revert and the single-item commit discipline.
