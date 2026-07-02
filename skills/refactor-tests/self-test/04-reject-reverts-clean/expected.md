# Expected outcome — fixture 04 (human rejects a green move → clean revert)

This fixture is deliberately identical to fixture 03 in every way *except the human decision*.
The move is correct, the suite is green after applying it — and the developer still says **no**.
This pins the fact that the human is the oracle, not the suite: a green run never overrides a
rejection.

**Pins:** AC2.4 — *"If Tess rejects, nothing is written; the item is skipped."* (Same outcome
for `skip` and `quit`, which also revert without committing.)

**How the loop drives it:**
1. Propose → apply `move.patch` → run suite (green) → pause for IDE review.
2. Decision = **reject** (this fixture).
3. `git checkout -- test_cart.py` — the working tree returns to the pre-apply state.

**Expected gate outcome:** `REVERT`, no commit. After the run, `git status` is clean and
`test_cart.py` is byte-for-byte the original. The item is marked `skipped` (rejected); on
`quit` the loop also stops after reverting.

**Gate failure (blocks the skill change):** the tool commits (or leaves the applied change on
disk) because the suite was green despite the human's rejection. That would make the suite —
not the human — the oracle, inverting D2.
