# Expected outcome — fixture 01 (uncheckable goal)

The initiative's declared goal — *"make it better"* — has no checkable metric. FRAME cannot turn
it into a gate.

**Pins:** slice-01/04 FRAME + DDD9 — *"FRAME captures a checkable goal metric and rejects a vague,
uncheckable one (or accepts explicit behaviour-preservation only)."*

**Expected decision:** `REFUSE`. FRAME declines to proceed and does one of:
- asks Quinn to restate the goal as a checkable metric (e.g. a coupling/fan-out target, a
  dependency-count target, a benchmark, or a prose check such as "self-test passes / no broken
  skill refs"), OR
- offers to continue on a **behaviour-preservation-only** basis (the preservation floor as the
  sole gate), which Quinn must explicitly accept.

Nothing is surveyed, planned, delegated, or written until a checkable goal or preservation-only is
agreed.

**Gate failure (blocks the skill change):** FRAME proceeds to MAP/EXECUTE with the goal still
uncheckable, or silently invents a metric Quinn never approved. Either means the "checkable goal"
guard is decorative — the run could later report "done" against a goal that was never measurable.
