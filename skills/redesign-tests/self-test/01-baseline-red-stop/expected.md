# Expected outcome — fixture 01 (baseline suite is red)

`orders.py` has a bug (`place()` persists `status="pending"` instead of `"placed"`), so the pinned
test `test_placed_order_is_retrievable_with_its_details` fails at baseline: `repo.get(order_id)`
returns a dict with `status="pending"`, the test asserts `status="placed"`.

**Pins:** AC1.7 — *"Never redesigns on a red baseline (verify green before proposing)."*

**How the loop drives it:** before proposing any rewrite, run the suite once to establish the green
baseline (mirrors `refactor-tests` / `phil:refactor` INIT / G1).

**Expected gate outcome:** `STOP`. The tool reports the red baseline, proposes and applies
**nothing**, writes no commit, and leaves the working tree byte-for-byte unchanged.

**Gate failure (blocks the skill change):** the tool proposes or applies any rewrite, or writes any
commit, while the baseline is red. A single write here means the "never redesign on red" guard is
decorative — exactly the silent-failure class this suite exists to catch.
