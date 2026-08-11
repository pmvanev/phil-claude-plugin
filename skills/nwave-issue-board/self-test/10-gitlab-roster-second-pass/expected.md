# Expected outcome — fixture 10 (numbers do not exist until creation)

**Where it fails silently.** Writing the roster during the creation pass means guessing the numbers.
Guessing produces a table of references that render as plain text or, worse, resolve to unrelated
issues that already existed in the project. Both look like a finished roster.

**Expected decision:** `TWO-PASS-BARE-REFS`.

**Checkable assertions (all must hold):**

1. All four slice issues are created first and their assigned numbers recorded, per *Bulk seeding
   needs two passes* in `phil:issue-board`.
2. The roster is written in a second pass, after the numbers are known.
3. Roster entries are **bare** `#N` references, never markdown links — a bare reference renders live
   state, a link freezes it.
4. The roster is described as the project-scoped rollup, not as the only rollup that exists; epics
   remain available on Premium groups.
5. The rendered result is read back, per `phil:issue-board`, since an unlinked `#N` means the number
   is wrong.

**Gate failure (blocks the skill change):** roster numbers written before creation; OR entries written
as markdown links.
