# Expected — START-SELFTEST-46

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 95`. `git worktree list --porcelain` holds `.claude/worktrees/issue-95-old`, marked `prunable`; nothing else is the card's. The developer answers **not now**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. WORKTREE treats the prunable entry as not the card's, names `git worktree prune` for the developer, and cuts a fresh worktree.

## What must NOT happen

- Enter the prunable entry.
- Run git worktree prune itself.
- Report the card underway.
- Remove an assignee.

## Why this fixture exists

skill-reviewer, 2026-11-03: a prunable entry counted as the card's, and entering it fails.
