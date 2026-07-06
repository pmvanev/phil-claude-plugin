# Slice 01 — Walking skeleton: one coupling rewrite

**Goal:** Run the full loop end-to-end on a single implementation-coupled test — propose one
behavioral rewrite, apply, sanity-check the suite, get human approval in the IDE, commit.

**IN scope**
- Scoped invocation: `/phil:redesign-tests <file-path>` or `<test-id>`.
- Detect one implementation-coupling smell in that target (assertion on private call / mock
  interaction / internal state).
- Propose ONE behavioral rewrite with before/after intent.
- Apply → re-run suite → auto-revert on red → human gate (approve/reject/skip/quit) → one commit.

**OUT scope**
- `--review` backlog seeding (S2).
- Over-mock (S3) and flakiness (S4) smell families.
- Any automated coverage oracle.

**Learning hypothesis**
Disproves *"a human can confidently approve a behavioral test rewrite from an IDE diff"* if Tess
distrusts or rejects the rewrites at the gate. This is the core bet of the whole feature.

**Acceptance criteria** — S1 AC1.1–AC1.7 (see feature-delta.md).

**Dependencies**
- `skills/shared/test-runner-detection.md` (reuse).
- `refactor-tests` loop pattern + git safety mechanics (reuse).

**Effort estimate:** ≤1 day (loop reused; net-new = behavioral-rewrite move + coupling detector).

**Reference class:** `refactor-tests` slice-01-one-approved-move (same loop, behavior-preserving vs.
behavior-changing move).

**Production data:** run against a real implementation-coupled test in this plugin's own suite (or
a representative fixture drawn from one), not synthetic.

**Dogfood moment:** maintainer sits at the approval gate for one real rewrite the same day.

**Pre-slice SPIKE:** none — mechanism is proven by `refactor-tests`; only the move set changes.
