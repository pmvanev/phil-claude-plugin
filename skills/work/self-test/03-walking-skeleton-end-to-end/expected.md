# Expected outcome — fixture 03 (walking skeleton — end-to-end)

The thinnest complete path through the contractor spine on a real code initiative with a checkable
goal and a green preservation oracle.

**Pins:** slice-01 walking skeleton — *"a run produces a confirmed goal + preservation contract, a
delegated change, a still-passing oracle, and a written decisions record — verified end-to-end on a
real initiative."* This is the ONE `@walking_skeleton` scenario for the feature.

**Expected decision:** `DELEGATE + RECORD`. In order, the tool:
1. FRAME — confirms the checkable goal and the preservation contract with Quinn.
2. delegates the change to exactly one skill (`refactor-loop`, per the code routing in DDD3).
3. relies on the delegate's own suite gate as the preservation oracle (DDD4) — it runs no gate of
   its own.
4. after the delegate reports green, writes `docs/work/<initiative>/decisions.md` (and the rest of
   the trail per ADR-006).
5. reports a summary naming the goal, the preservation result (oracle green), and the commit made.

**Gate failure (blocks the skill change):** the tool re-implements a preservation gate instead of
inheriting the delegate's (violates DDD4/ADR-005); or reports "done" without writing the decision
record; or writes the record but the oracle was not actually green. Any of these breaks the
minimal promise the whole feature rests on.
