# Expected — START-SELFTEST-42

`UNDERWAY` · `CLAIMED` · `WORKTREE-FAILED` · `WROTE-NOTHING`

## Situation

`/phil:start 80` from the main checkout, with card 80 already In Progress and assigned to `pmvanev`. `.claude/worktrees/issue-80-phil-start` exists; EnterWorktree refuses its path.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. The report quotes the refusal, says the session is still in the main checkout, and ends `UNDERWAY`, naming `/phil:resume`.

## What must NOT happen

- Recommend a route.
- Launch anything.
- Cut a fresh worktree.
- Run git worktree add.
- Write a Status the card already holds.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-03: a refused enter sent an underway card to ROUTE.
