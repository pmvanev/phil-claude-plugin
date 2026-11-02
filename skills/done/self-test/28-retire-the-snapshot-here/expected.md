# Expected — DONE-SELFTEST-28

`CLOSED` · `CLEARED`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. Its branch exists locally only, at `a1b2c3d`. This session runs in the main checkout, on main, which holds a `.session-handoff.md` whose next action concerns this card.

## The developer answers

`yes, and retire the snapshot here too`

## Writes, in order

the closing comment, then Status=Done, then the close, then retire the snapshot here, then delete the local branch

## What must happen

The report reads `CLEARED: 1 snapshot, 1 branch (local)`.

## What must NOT happen

- Retire the snapshot here on a plain yes.
- Treat the third answer as a stop.
- Delete it with `rm`.
- Merge anything.

## Why this fixture exists

The snapshot where /phil:done runs records no branch and may belong to other work (skill-reviewer, 2026-11-02), so keeping it is the default and retiring it is the developer's explicit answer.
