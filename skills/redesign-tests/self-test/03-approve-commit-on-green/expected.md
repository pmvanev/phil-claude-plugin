# Expected outcome — fixture 03 (approve → commit) — WALKING SKELETON (S1)

Baseline is green: the coupled `test_place_saves_order` passes. The proposed rewrite (`move.patch`)
replaces the mock-interaction assertion with a behavioural one — using the real `InMemoryOrderRepo`
and asserting the retrieved order equals `{id:A1, amount:100, status:placed}`. Applying it keeps the
suite **green**.

**Pins:** AC1.1 (one rewrite, never bundled), AC1.2 (apply to working tree, re-run suite), AC1.6
(proposal states what it verifies now vs. before — the `coverage_equivalence_claim`), AC1.5
(approve → exactly one commit of only the touched file). This is the **walking skeleton** — the
whole feature bet in one loop.

**How the loop drives it:** apply `move.patch`, run the suite (green), then **surface to Tess**: the
named move, the target, the one-line rationale, AND the `coverage_equivalence_claim` from the
manifest. No diff is printed in chat — Tess reviews the real uncommitted diff in her editor. Supply
`human_decision: approve` (in live use this comes from the AskUserQuestion gate).

**Expected gate outcome:** `COMMIT`. Exactly one commit is made, staging only `test_orders.py`,
with a message naming the smell family, the move, and that it is human-approved. Nothing is
committed before approval.

**Gate failure (blocks the skill change):** the loop commits before approval; commits without
surfacing the coverage-equivalence claim (the human cannot judge a behavioural rewrite from the diff
alone — ADR-004); bundles more than one item; or stages files the move did not touch.
