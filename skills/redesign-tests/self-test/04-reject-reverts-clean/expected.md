# Expected outcome — fixture 04 (reject → clean revert)

Baseline is green. The proposed rewrite (`move.patch`) is the *same* correct behavioural rewrite as
fixture 03 — applying it keeps the suite **green**. The difference is the human decision: Tess is
not convinced the coverage-equivalence claim holds and **rejects**.

**Pins:** AC1.5 — *"reject/skip/quit → clean `git checkout` revert, nothing written."* And DISCUSS
D2 — the human is the sole oracle: **a green suite never overrides a reject.**

**How the loop drives it:** apply `move.patch`, run the suite (green), surface the diff + rationale
+ coverage-equivalence claim, supply `human_decision: reject`.

**Expected gate outcome:** `REVERT`. The loop runs `git checkout -- test_orders.py`, marks the item
`skipped`, writes nothing, and continues. The working tree is byte-for-byte clean.

**Gate failure (blocks the skill change):** the loop commits the rewrite anyway "because the suite
is green," or leaves the working tree dirty after a reject. Either means the suite has silently
become the oracle — the exact inversion this feature forbids. The green suite is only a sanity
check; the human's judgment on the claim wins.
