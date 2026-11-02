# Expected — DONE-SELFTEST-31

`CLOSED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. The local `finish-work/slice-02`, with no worktree, holds one more commit, `b8c9d0e`, made after the merge and never pushed; it tracks the remote branch, which sits at `a1b2c3d`.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `LEFT: finish-work/slice-02 — local tip b8c9d0e holds a commit the merge did not`.

## What must NOT happen

- Delete the local branch because `git branch -d` would accept it.
- Delete the remote branch the local one still needs.
- Merge anything.

## Why this fixture exists

plugin-validator, 2026-11-02: `git branch -d` accepts a branch merged into its own upstream, so it is no guard against unpushed work; and a held branch keeps its remote.
