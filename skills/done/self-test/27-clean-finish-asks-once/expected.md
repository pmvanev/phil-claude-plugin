# Expected — DONE-SELFTEST-27

`CLOSED` · `CLEARED`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. Its branch exists locally only, at `a1b2c3d`, with no worktree. No other pull request names the card, and the main checkout holds no snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must happen

One question, one yes, then `CLOSED` and `CLEARED: 1 branch (local)`.

## What must NOT happen

- Ask about each item separately.
- Ask a confirming question after the yes.
- Merge anything.

## Why this fixture exists

AC4.5 and the one-question KPI: a clean finish that asks several questions is the ceremony anxiety the one-yes plan answers.
