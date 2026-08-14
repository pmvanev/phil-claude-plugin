# Expected — 34 (the longest card on the board is the correct one)

**Pins:** the oversized rule holding **unchanged** under one-issue-per-feature, and the session-state rule
scoped to *typed outside a generated region*. Both verified 2026-08-14; neither rule's text was modified.

**Expected decision:** `REPORT-CLEAN` for #26. **Two findings must not appear:**

1. **No oversized finding.** The rule is *"a card carrying work that cannot be demonstrated on its own"* —
   demonstrability, not size. A feature is exactly a thing that can be demonstrated on its own. That this
   card is the longest on the board is not evidence of anything.
2. **No session-state finding.** The projected why / next / stack sit **inside** the `nwave:status`
   markers, generated and timestamped, with `.session-handoff.md` still the authority. Typed scratch
   *outside* the markers remains a defect.

**Why this fixture exists rather than the rule change it replaced.** The first design for this slice
proposed making the oversized heuristic structure-aware, to stop it flagging feature cards. That was
unnecessary — the rule already passes them — and it would have been **actively harmful**: a size-aware
heuristic proposes splitting a consolidated feature back into slices, this family stores no marker, so a
declined split returns every run and only has to be accepted once. The board would oscillate
consolidate → split → consolidate. **The fixture is the guard against a future reader "fixing" a rule that
was never broken.**

**Gate failures:**

- Any oversized finding on #26, however hedged.
- A session-state finding for content inside the markers.
- Reporting the card's length as a defect under any other name — "hard to scan", "consider splitting".
- Proposing the roster rows be promoted to cards. That is the paradigm, inverted.
- Modifying the oversized rule's text to make this pass. It already passes; a diff there is this fixture
  failing, not succeeding.
