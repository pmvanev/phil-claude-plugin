# Expected — DONE-SELFTEST-30

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. After the merge, a follow-up commit `e5f6a7b` was pushed to the remote `finish-work/slice-02` from another machine. The local branch still sits at `a1b2c3d`, with no worktree.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must happen

The report reads `CLEARED: 1 branch (local)` and `LEFT: finish-work/slice-02 on the remote — its tip e5f6a7b is past the merge`.

## What must NOT happen

- Delete the remote branch.
- Rely on `git push --delete` to refuse it.
- Merge anything.

## Why this fixture exists

plugin-validator, 2026-11-02, verified in a scratch repo: `git push --delete` deleted a branch whose commit was in no other branch, exit 0. The tip check is the guard.
