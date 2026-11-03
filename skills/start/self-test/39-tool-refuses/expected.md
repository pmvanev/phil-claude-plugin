# Expected — START-SELFTEST-39

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-FAILED`

## Situation

`/phil:start 95`. EnterWorktree refuses: the repo's WorktreeCreate hook exits non-zero. The developer answers **not now**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. The report quotes the refusal, says the session stays where it is, and goes on to describe and route the card.

## What must NOT happen

- Run git worktree add.
- Retry under another name.
- Report WORKTREE-CUT.
- Remove an assignee.

## Why this fixture exists

A refusal is reported, never worked around with a grant this command lacks.
