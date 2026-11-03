# Expected — START-SELFTEST-19

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 95`. Issue 95 is open, unassigned, and on no project. The board's add-to-project workflow is enabled. The developer answers **not now**.

## What must happen

CLAIM runs `gh project item-add` first, ignores its exit code, re-reads `projectItems` for the item id, then writes Status In Progress, assigns the developer and reads both back: `CLAIMED: added to the board, Status In Progress, assigned to pmvanev — read back`. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Write a Status before the card is on the board.
- Take item-add's exit code as proof the item landed.
- Take the item id from item-add's output.
- Remove an assignee.

## Why this fixture exists

AC3.1, and `phil:issue-board`: an issue never added has no field to set, and editing it does nothing.
