# Expected outcome — fixture 41 (the recorded commit is off HEAD's history)

**Expected decision:** `RESUME-STALE + BOARD-DIVERGES`. The verdict comes first and gives no distance:

```
STALE — snapshot at 9f8e7d6, not in HEAD's history (another branch, or rebased); HEAD is now e17bd55,
working tree clean. The recorded next action may no longer apply.
```

The board holds nothing In Progress, so the check compares against the top Todo card, #12, which
names other work than the recorded next action: `BOARD-DIVERGES`, both sides named, as
`references/board-divergence.md` gives it.

**Gate failure (blocks the skill change):** any of —

- a commit count, such as `(5 commits)` from a plain `git rev-list --count 9f8e7d6..HEAD`: the
  squash merge left the recorded commit on another line of history, and the count reads as "5 behind";
- `unreachable`: the commit resolves, so the word misstates why it is stale;
- the briefing presented before the verdict.

**Why this fixture exists:** `plugin-dev:skill-reviewer` found the gap in `/phil:done` on 2026-11-09.
`bootstrap.md` declared a recorded commit unknown only when the count failed, and the count succeeds
for any commit the object store still holds. `git rev-list --count --left-right 9f8e7d6...HEAD` prints
`3	5`: both sides hold commits the other lacks.
