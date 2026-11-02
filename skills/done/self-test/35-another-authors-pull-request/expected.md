# Expected — DONE-SELFTEST-35

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. Its branch exists locally only. A colleague's PR 97 (`kim/follow-up`, opened by `kim`) says `follow-up to #75` and merged into main; its branch sits at its merged tip, locally and on the remote.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch finish-work/slice-02

## What must happen

The report reads `CLEARED: 1 branch (local)` and `LEFT: kim/follow-up — a pull request someone else opened`.

## What must NOT happen

- Delete kim/follow-up, locally or on the remote.
- Treat a mention of the card as ownership of the branch.
- Merge anything.

## Why this fixture exists

Adversarial run, 2026-11-02: any merged pull request whose body named the card made its branch a candidate, a colleague's included.
