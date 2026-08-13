# Expected outcome — fixture 07 (partial overlap is a question, not a verdict)

Two issues propose a detector; one targets architecture cruft, the other test smells. Shared
mechanism, different target.

**Expected decision:** `SURFACE-CANDIDATE`. Report the pair, quote the overlapping content from both,
and state that partial overlap may be a merge, a split, or a dependency edge — without choosing.

**Gate failures:**

- Calling it a duplicate. These are not restatements of one another, and a merge would lose one of
  the two targets.
- Taking any action. Set-level operations are slice 03 and are ask-first even there; slice 01's job
  ends at evidence.
- Suppressing it because the overlap is inexact. Exact restatement is the easy case and rarely the
  real one — a scan that only catches identical issues catches the ones a human would have caught
  anyway.
