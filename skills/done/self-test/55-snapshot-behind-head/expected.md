# Expected — DONE-SELFTEST-55

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 100 (`fix-12`, head `b2c3d4e`, opened by the developer) merged into main, which is green, and every ask is done. Its branch exists locally only, at `b2c3d4e`. This session runs in the main checkout, on main at `2c3d4e5`, clean, after `git reset --hard` took it back three commits from `4a91c02`. The checkout holds a `.session-handoff.md` whose header reads `commit: 4a91c02` and `dirty: no`. `git rev-list --count --left-right 4a91c02...HEAD` prints `3	0`.

## The plan shows

```
SURVIVES
  ./.session-handoff.md — STALE — snapshot at 4a91c02, HEAD is now 2c3d4e5, 3 commits behind it (reset or checked out backwards); tree clean;
                          next: "<its next action>"; may be other work; the third answer retires it
```

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must NOT happen

- Print `(0 commits)`.
- Call it `not in HEAD's history`.
- Retire the snapshot here on a plain yes.
- Read the snapshot's recorded exchanges.
- Merge anything.

## Why this fixture exists

A tree reset behind the snapshot reads 0 from a plain count and failed the first ancestry test, which sent it to the off-history line (skill-reviewer, 2026-11-09).
