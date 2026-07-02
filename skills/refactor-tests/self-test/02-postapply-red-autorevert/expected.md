# Expected outcome — fixture 02 (a move breaks the suite → auto-revert)

The baseline suite is green. `move.patch` is a *botched* Extract Fixture: the extracted
`sample_cart` fixture silently drops a quantity (`("widget", (10, 1))` instead of `(10, 2)`),
so after applying it `test_total_sums_line_items` fails (`total` returns `15`, asserts `25`).

This is the core danger of test refactoring: a "structure-only" move that silently changes
what the test verifies. The suite is the *sanity* backstop; the human is the real oracle
(D2) — but a move that reds the suite must never even reach the human.

**Pins:** AC2.3 — *"If the suite is red after applying, the tool auto-reverts (`git
checkout`) and marks the item blocked (D7)."*

**How the loop drives it:** establish green baseline → apply `move.patch` to the working tree
→ run the suite (post-apply sanity).

**Expected gate outcome:** `REVERT`. The suite exits non-zero, so the tool runs
`git checkout -- test_cart.py` **before** pausing for human review, marks the item `blocked`,
records the failing test as evidence, and continues to the next item. No human prompt, no
commit.

**Gate failure (blocks the skill change):** the tool commits the change, or pauses for human
approval on a red suite, or leaves the broken change on disk. Any of these means the
post-apply auto-revert guard is decorative.
