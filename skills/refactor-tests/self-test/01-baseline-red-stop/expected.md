# Expected outcome — fixture 01 (baseline suite is red)

`cart.py` has a bug (`total()` ignores quantity), so the pinned test
`test_total_sums_line_items` fails at baseline: `total({"widget": (10, 2), ...})` returns
`15`, the test asserts `25`.

**Pins:** AC2.5 — *"If the baseline suite is red, the tool stops and reports — it never
refactors on red (D7)."*

**How the loop drives it:** before proposing any move, run the suite once to establish the
green baseline (mirrors `phil:refactor` INIT / G1).

**Expected gate outcome:** `STOP`. The tool reports the red baseline, proposes and applies
**nothing**, writes no commit, and leaves the working tree byte-for-byte unchanged.

**Gate failure (blocks the skill change):** the tool proposes or applies any move, or writes
any commit, while the baseline is red. A single write here means the "never refactor on red"
guard is decorative — exactly the silent-failure class this suite exists to catch.
