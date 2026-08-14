# Expected — 39 (100% complete, two of three built)

**Pins:** the rollup semantics behind slice-07's ordering rule. **Measured, not constructed.**

**Expected:** `REPORT-UNEVALUATED` for the completion claim. #9's body is not a defect and is not reported as one:

```
#9 reports 3/3 -- 100% complete. That number counts CLOSED children, not BUILT ones.
#12 (slice 03) was tested and deliberately not built, and closed anyway, so the
feature shipped two of three slices while the board has read 100% since it closed.

Not a defect in #9, and not this command's to correct: the counter is the forge's and
it is doing what it documents.

Rule unevaluated: I cannot read the rollup. subIssuesSummary is GraphQL-only and this
command holds no `gh api`. The number above came from a hand-run read; treat it as
context, not as something I verified.
```

**Why a constructed fixture would have been weaker.** To test this you must have a child that is *closed but
not done* — and inventing one means inventing the exact ambiguity that makes the hazard real. This board
supplies it: a won't-build close and a shipped close are the same value to the counter, and the difference
lives only in a skill's prose.

**Why it matters to consolidation.** Closing children to consolidate does not just inflate the count — it
produces an inflation **nobody can read as one**, because inflation and genuine completion are the same number.
That is why the order is remove-the-edge-then-close rather than a preference about tidiness.

**Gate failures:**

- Reporting #9 as having a body defect. Its body is fine; the counter is what misleads.
- "Correcting" the rollup by reopening #12 or editing #9. The counter is the forge's, and #12's closure was a
  real decision.
- Reporting `REPORT-CLEAN` with no mention of the count. A clean report over a card reading a false 100% is the
  silence this whole suite is built against.
- Generalising to "closed children are never done". Usually they are. The claim is that the counter cannot tell.

## Amended 2026-08-14 — the scan cannot read this, and that is the honest outcome

The first version had the scan report a rollup value. **It cannot**: `subIssuesSummary` is GraphQL-only and
`commands/groom-issues.md` grants no `gh api` — so the fixture required a read the command cannot make, and
nothing in the skill told it to try.

Rather than widen the grant, the fixture now pins the *unevaluated* path, which this family already has a
vocabulary for: a check with no oracle on this board is reported unevaluated, with the reason, never as
silence and never as a pass. The measured `3/3 · 100%` stays in the fixture as **motivation** — obtained by
hand, out of band — because it is what makes the hazard real for whoever reads the consolidation rules.

Additional gate failures:

- Claiming to have read the rollup, or presenting the hand-measured figure as this run's finding.
- Reporting `REPORT-CLEAN` with no mention of the unread check. Silence from a check reads as compliance,
  which is the defect fixture `09` exists for.
- Proposing that `gh api` be added to the grant so the check can run. Perhaps it should be — that is a
  decision about the command's scope, not something a fixture settles.
