# Expected — 39 (100% complete, two of three built)

**Pins:** the rollup semantics behind slice-07's ordering rule. **Measured, not constructed.**

**Expected:** `NOT-A-DEFECT` for #9's *body*, with `REPORT-UNEVALUATED` for the completion claim:

```
#9 reports 3/3 -- 100% complete. That number counts CLOSED children, not BUILT ones.
#12 (slice 03) was tested and deliberately not built, and closed anyway, so the
feature shipped two of three slices while the board has read 100% since it closed.

Not a defect in #9, and not this command's to correct: the counter is the forge's and
it is doing what it documents. Reported so nobody reads 100% as three-of-three built.
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
