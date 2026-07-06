# Expected outcome — fixture 02 (a rewrite reds the suite)

Baseline is green: the coupled `test_place_saves_order` passes (a `Mock`'s `save` is called). The
proposed rewrite (`move.patch`) changes the test to assert on the persisted order — but gets the
expected value **wrong** (`status="confirmed"` where the SUT produces `"placed"`). Applying it and
running the suite goes **red**.

**Pins:** AC1.3 — *"Never reaches the human on red: post-apply red → `git checkout` auto-revert,
mark blocked, continue."*

**How the loop drives it:** apply `move.patch`, run the suite. Read the exit code directly.

**Expected gate outcome:** `REVERT`. On the red suite the loop runs `git checkout -- test_orders.py`,
marks the item `blocked (post-apply red)` with the failing test as evidence, and continues to the
next item. **Tess is never asked** — a broken rewrite must not reach the human gate.

**Gate failure (blocks the skill change):** the loop pauses for human approval on the red suite, or
commits the broken rewrite, or leaves the working tree dirty. Any of these means the auto-revert
guard is decorative — the human would be asked to bless a broken change, defeating the
"never bother the human with a broken change" contract.
