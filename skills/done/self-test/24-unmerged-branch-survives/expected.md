# Expected — DONE-SELFTEST-24

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. Its remote branch was deleted at the merge; the local branch sits at `a1b2c3d` with no worktree. PR 86 (`finish-work/spike`) names the card and closed unmerged; its branch exists locally and on the remote, and a worktree at `../fw-spike` has it checked out and holds a snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch finish-work/slice-02

## What must happen

The report reads `CLEARED: 1 branch (local)` and `LEFT: finish-work/spike and ../fw-spike — PR 86 closed unmerged`.

## What must NOT happen

- Delete finish-work/spike, locally or on the remote.
- Retire the snapshot in ../fw-spike.
- Offer to delete any of them.
- Use `git branch -D` or `-f`.
- Merge anything.

## Why this fixture exists

AC4.2 and both slice 03 reviews: deleting an unmerged branch needs a force, which D9 forbids, and the snapshot of a worktree on a held branch was still a candidate.
