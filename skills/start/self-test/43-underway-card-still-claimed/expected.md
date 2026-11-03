# Expected — START-SELFTEST-43

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED`

## Situation

`/phil:start 95` from the main checkout. Card 95 is in Todo and unassigned, and `.claude/worktrees/issue-95-retry-flaky-uploads` exists.

## What must happen

CLAIM writes Status In Progress and assigns the developer, reading both back: `CLAIMED`. WORKTREE enters the existing worktree and names `/phil:resume`.

## What must NOT happen

- Skip the claim because the card is underway.
- Cut a second worktree.
- Recommend a route.
- Remove an assignee.

## Why this fixture exists

D2, plugin-validator, 2026-11-03: a card underway is still claimed.
