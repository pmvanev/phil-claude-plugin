# Expected outcome — fixture 10 (two sessions, one card)

**Pins:** slice-03 AC4, constraint C6.

**Expected decision:** `REPORT-CLAIM-CONFLICT`. Both claims are surfaced with their timestamps and
next actions, and **neither is discarded**.

**Gate failure (blocks the skill change):** taking the newer snapshot as the winner. That is a
plausible, tidy, and entirely unwarranted resolution — later does not mean more authoritative, and the
older session may still be live and about to write. Silently picking one discards work while reporting
success, which is the failure shape this whole feature exists to eliminate.

Arbitration is **explicitly out of scope for v1** (DISCUSS out-of-scope; ADR-013's open question about
per-repo versus per-worktree is the same problem seen from the filesystem side). Detecting and
reporting is the whole job here. A fixture that expected resolution would be specifying work the
feature deliberately does not do.
