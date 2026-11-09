# Expected outcome — fixture 42 (the tree went back behind the snapshot)

**Expected decision:** `RESUME-STALE + BOARD-AGREES`. The verdict comes first and counts what the tree
lost:

```
STALE — snapshot at 4a91c02, HEAD is now 2c3d4e5, 3 commits behind it (reset or checked out backwards),
working tree clean. The recorded next action may no longer apply.
```

The recorded next action and the In Progress card name the same work: `BOARD-AGREES`. Agreement does
not soften the verdict; freshness and the board are independent facts.

**Gate failure (blocks the skill change):** any of —

- `(0 commits)`, from a plain `git rev-list --count 4a91c02..HEAD`: the tree lacks three commits the
  next action assumes;
- `not in HEAD's history (another branch, or rebased)`: the recorded commit is a descendant of `HEAD`,
  not on another branch;
- the briefing presented before the verdict.

**Why this fixture exists:** `plugin-dev:skill-reviewer`, 2026-11-09. The first fix for fixture 41
tested ancestry one way only and sent this case to the off-history line with no count.
