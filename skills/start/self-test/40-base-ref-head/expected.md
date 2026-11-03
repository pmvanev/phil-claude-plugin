# Expected — START-SELFTEST-40

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 95` in a repo whose `.claude/settings.json` sets `worktree.baseRef: head`. The new worktree's HEAD is `a448a36`; the remote's head, read from GitHub, is `55640cd`. The developer answers **not now**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. The run reads `worktree.baseRef` from the settings, and the worktree line says the worktree branched from local HEAD at `a448a36` while the remote is at `55640cd`, naming `worktree.baseRef: head`.

## What must NOT happen

- Report the base as origin/main.
- Rebase the new branch.
- Remove an assignee.

## Why this fixture exists

D1: the report names the base commit the developer actually got.
