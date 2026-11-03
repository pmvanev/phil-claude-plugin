# Expected — START-SELFTEST-32

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED` · `WROTE-NOTHING`

## Situation

`/phil:start 80` from the main checkout. Card 80 is In Progress and assigned to `pmvanev`; `.claude/worktrees/issue-80-phil-start` exists, unlocked, holding no snapshot; no pull request is open.

## What must happen

CLAIM writes nothing. WORKTREE enters the existing worktree with EnterWorktree and its path, and the report names `/phil:resume` as the next step. No route is recommended.

## What must NOT happen

- Cut a second worktree.
- Recommend a route.
- Launch anything.
- Remove an assignee.

## Why this fixture exists

D2, D3, AC4.2, and issue 80's fifth fixture behaviour: a card that already has a worktree reuses it.
