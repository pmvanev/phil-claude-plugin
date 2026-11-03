# Expected — START-SELFTEST-31

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 95` from the main checkout. The card has no worktree, no open pull request and no surviving branch. The clone fetched an hour ago, and the remote's `main` has gained a commit since. The developer answers **not now**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. WORKTREE runs `git fetch origin main` itself, then cuts `issue-95-retry-flaky-uploads` with EnterWorktree, and the session moves in. The report names the path, the branch `worktree-issue-95-retry-flaky-uploads` and the base commit, which equals the remote's head as GitHub reports it.

## What must NOT happen

- Skip the fetch because the tool fetches.
- Run git worktree add.
- Branch from the clone's stale origin/main.
- Compare the base only against the local origin/main.
- Remove an assignee.

## Why this fixture exists

D1, AC4.1. Read from Claude Code 2.1.317's source on 2026-11-03: the tool fetches only when the last fetch is a day old, so a repo fetched today branches from a stale ref unless the run fetches.
