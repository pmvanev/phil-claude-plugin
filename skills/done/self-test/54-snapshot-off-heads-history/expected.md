# Expected — DONE-SELFTEST-54

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 99 (`fix-11`, head `a0b1c2d`, opened by the developer) squash-merged into main, which is green, and every ask is done. Its branch exists locally only, at `a0b1c2d`. This session runs in the main checkout, on main at `e17bd55`, clean. The checkout holds a `.session-handoff.md` written while `fix-11` was checked out there: its header reads `commit: 9f8e7d6` and `dirty: no`. `git rev-parse --verify --quiet 9f8e7d6^{commit}` resolves it, but `git merge-base --is-ancestor 9f8e7d6 HEAD` exits 1, because the squash merge left it off main's history.

## The plan shows

```
SURVIVES
  ./.session-handoff.md — STALE — snapshot at 9f8e7d6, not in HEAD's history (another branch, or rebased); HEAD is now e17bd55;
                          next: "<its next action>"; may be other work; the third answer retires it
```

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must NOT happen

- Print a commit count from `git rev-list --count 9f8e7d6..HEAD`.
- Call it unreachable because it resolved.
- Retire the snapshot here on a plain yes.
- Read the snapshot's recorded exchanges.
- Merge anything.

## Why this fixture exists

A snapshot written on a feature branch later squash-merged still resolves, and counting from it reads as N commits behind when the histories diverged (skill-reviewer, 2026-11-09).
