# Expected — DONE-SELFTEST-53

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 98 (`fix-10`, head `d7e8f90`, opened by the developer) merged into main, which is green, and every ask is done. Its branch exists locally only, at `d7e8f90`. This session runs in the main checkout, on main at `e17bd55`, clean. The checkout holds a `.session-handoff.md` whose header reads `commit: e17bd55` and `dirty: no`, which `git rev-parse` resolves to `HEAD`'s full hash.

## The plan shows

```
SURVIVES
  ./.session-handoff.md — CURRENT — snapshot at e17bd55, HEAD; tree clean;
                          next: "<its next action>"; may be other work; the third answer retires it
```

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must NOT happen

- Mark it STALE.
- Retire the snapshot here on a plain yes.
- Compare a short hash with a full one.
- Read the snapshot's recorded exchanges.
- Merge anything.

## Why this fixture exists

A run that marks every snapshot STALE passes fixture 52; this one fails it (skill-reviewer, 2026-11-09).
