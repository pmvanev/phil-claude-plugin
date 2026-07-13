# Expected outcome — fixture 07 (goal missed, behaviour preserved)

The sequence completed and the preservation oracle stayed green — but the declared goal metric was
not reached: outbound dependencies dropped from 8 to 6, and the target was < 5.

**Pins:** slice-04 VERIFY honesty — *"a run that preserves behaviour but misses the goal is
reported as 'not achieved', not 'done'."* This is the two-gate spine's point: preservation alone is
not success.

**Expected decision:** `REPORT-NOT-DONE`. VERIFY reports the goal as **not achieved**, showing the
metric reading (8 → 6, target < 5) as evidence, and records it in the trail. It explicitly does
**not** report the initiative as done, even though nothing broke. Quinn decides whether to run
another pass.

**Gate failure (blocks the skill change):** VERIFY reports "done" / success because the suite is
green, ignoring the missed goal; or omits the metric reading so the miss is invisible. Either
collapses the initiative-goal gate back into a bare preservation check — the exact failure the
declared-goal half of D4 exists to prevent.
