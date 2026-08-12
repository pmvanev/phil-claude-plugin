# Expected outcome — fixture 03 (derivable state offered)

Four of the six fields offered are already owned by artifacts and derivable at read-back by the
read-only `nwave-slice-status` skill.

**Pins:** slice-01 AC6 and **KPI-5** (`facts duplicated between the snapshot and an artifact that owns
them = 0`).

**Expected decision:** `REFUSE-DERIVABLE`. The snapshot records the *why* and the *next action* only.
The wave, slice, step, and branch are left out and looked up at read-back instead.

**Gate failure (blocks the skill change):** all six fields are recorded. This is the seductive failure
— the snapshot looks *more* complete and reads better, and it is wrong. The moment the work moves on,
those four fields disagree with the artifacts and the snapshot becomes a second authority. That is
exactly the drift anxiety B describes and `phil:issue-board` forbids.

Read this fixture together with `05`: there, the same class of state must be actively derived. The
rule is not "never touch position" — it is **never at capture, always at read-back**.
