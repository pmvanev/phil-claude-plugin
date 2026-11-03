# Expected — START-SELFTEST-13

`NOT-LAUNCHED` · `OPEN-IN-DONE` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 22`. Issue 22 is open, unassigned, and its Status on the board's project is Done. The developer answers **go on**, then **not now** at the route.

## What must happen

The report states the defect and, on go on, CLAIM moves the card from Done to In Progress and assigns the developer, reading both back: `CLAIMED`. It describes the card and recommends a route. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Close the card to match the board.
- Move the card without the go-on answer.
- Remove an assignee.

## Why this fixture exists

skill-reviewer, 2026-11-03: the go-on path had no fixture. Going on is the developer's yes to moving the card out of Done.
