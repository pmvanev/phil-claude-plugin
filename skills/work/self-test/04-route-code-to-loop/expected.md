# Expected outcome — fixture 04 (code wave → gated code loop)

The wave changes executable code (`orders.py`) and that code has a runnable test suite.

**Pins:** slice-05 + DDD3 (routing) + DDD4/D9 (inherited oracle) — code waves route to the
code-refactoring loop, whose suite gate IS the preservation oracle.

**Expected decision:** `DELEGATE-TO-CODE-LOOP`. EXECUTE hands the wave to `refactor-loop` (or
`refactor`/`extract-method` for a simpler move) and relies on that delegate's suite gate to
certify behaviour preservation. `phil:work` runs **no preservation gate of its own** — it only
enforces the cross-wave sequencing rule (fixture 06).

**Gate failure (blocks the skill change):** the tool routes a code wave to a prose/human-approval
cleaner, or re-implements a suite gate itself instead of inheriting the delegate's. Either breaks
DDD4/ADR-005 ("never re-implement a delegate's gate").
