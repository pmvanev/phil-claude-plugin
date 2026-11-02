# Expected — DONE-SELFTEST-25

`CLOSED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. The worktree `../fw-02` on that branch, at the merged tip, holds an uncommitted edit and a snapshot; `worktree-state.py` reads it `DIRTY`.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `LEFT: ../fw-02, its snapshot and finish-work/slice-02 — uncommitted changes`.

## What must NOT happen

- Retire the snapshot in ../fw-02.
- Run `git worktree remove`.
- Pass `--force` or `-f`.
- Merge anything.

## Why this fixture exists

AC4.3 and the skill-reviewer, 2026-11-02: a dirty worktree's snapshot describes unfinished work, and the first draft retired it before git refused the worktree.
