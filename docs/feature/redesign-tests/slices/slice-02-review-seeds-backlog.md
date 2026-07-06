# Slice 02 — `--review` seeds the behavioral-smell backlog

**Goal:** Scan a directory for in-scope behavioral smells and write a prioritized, separate backlog.

**IN scope**
- `/phil:redesign-tests --review <path>`.
- Reuse `review-code` Priority 6 (Test Quality) taxonomy for detection — do not fork a divergent list.
- Write `.test-redesign-backlog.md` in `review-code` backlog format (by convention), one item per
  smell (file:line, smell type, proposed rewrite intent, priority).
- Apply nothing.

**OUT scope**
- Applying any rewrite (that is S1/S3/S4).
- Modifying `review-code` itself.

**Learning hypothesis**
Disproves acceptable detection precision if >20% of items are rejected on first human review (K1).

**Acceptance criteria** — S2 AC2.1–AC2.4 (see feature-delta.md).

**Dependencies**
- `review-code` Priority 6 taxonomy (reuse, unchanged).
- Backlog-format convention from `refactor-tests` / `review-code`.

**Effort estimate:** ≤1 day.

**Reference class:** `refactor-tests` slice-02-review-seeds-backlog.

**Production data:** review this plugin's own `tests/` (or a real project's), not synthetic.

**Dogfood moment:** maintainer reads the generated backlog and judges precision the same day.

**Pre-slice SPIKE:** none.
