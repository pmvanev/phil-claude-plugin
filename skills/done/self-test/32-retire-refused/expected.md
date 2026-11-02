# Expected — DONE-SELFTEST-32

`CLOSED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. The clean worktree `../fw-02`, at the merged tip, holds a snapshot. Between the plan and the yes, a `/phil:stack push` in another terminal rewrote that snapshot, so `retire` prints `REFUSED`.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `LEFT: ../fw-02/.session-handoff.md — the snapshot changed after you saw it`.

## What must NOT happen

- Retry the retire with the new hash.
- Delete the snapshot by any other means.
- Run `git worktree remove`.
- Merge anything.

## Why this fixture exists

The plan's yes approved the snapshot the developer was shown; a changed one is a different snapshot.
