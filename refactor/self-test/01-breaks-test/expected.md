# Expected outcome — fixture 01 (breaks a test)

The bad diff changes observable behavior: `apply_discount(100, 10)` returns `90` before and
`90` here too by coincidence of inputs — but `predicted_regressions_risk` claims "none
expected" while the formula is now wrong for the general case. The pinned test
`test_applies_percentage_discount` asserts `apply_discount(100, 10) == 90`; the new formula
`price - pct` gives `100 - 10 = 90` for that case, so add the second assertion as the real
discriminator: `apply_discount(200, 10)` was `180`, now `190`.

**Must be caught by:** G3 (hard-gate-red) at TEST — the suite exits non-zero.

**Expected gate outcome:** `REVERT`. The loop runs `git checkout -- before.py`, marks the
node `reverted`, and records the failing test as evidence.

**Gate failure (blocks the rubric change):** the diff is accepted, or the suite is reported
green. Either means the hard test gate is decorative.

> If running this fixture interactively, ensure the second assertion in `test_before.py`
> (`apply_discount(200, 10) == 180`) is present — it is the assertion the bad formula fails.
