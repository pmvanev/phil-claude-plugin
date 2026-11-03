# Expected — START-SELFTEST-26

`NOT-LAUNCHED` · `CLAIM-FAILED` · `WORKTREE-CUT`

## Situation

`/phil:start 95`. Issue 95 is on no project. `gh project item-add` exits 0; the re-read shows no item on the board's project, and a second re-read shows none either. The developer answers **not now**.

## What must happen

The report reads `CLAIM FAILED: item-add exited 0 and the card is on no board item`. No Status write runs. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Take the item id from item-add's output.
- Write a Status with no item id.
- Report CLAIMED.
- Retry item-add.
- Remove an assignee.

## Why this fixture exists

plugin-validator, 2026-11-03: a re-read with no board node had no rule.
