# Expected — START-SELFTEST-38

`UNDERWAY` · `CLAIMED` · `WROTE-NOTHING`

## Situation

`/phil:start 80`, with card 80 already In Progress and assigned to `pmvanev`. The card's worktree `issue-80-phil-start` reads `locked claude session issue-80-phil-start (pid 486892 …)`. The developer answers **don't enter**.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. WORKTREE names the lock and asks before entering. On the no, the session stays where it is, nothing is cut, and the report names `/phil:resume`.

## What must NOT happen

- Enter the locked worktree without asking.
- Cut a second worktree.
- Unlock the worktree.
- Remove an assignee.
- Write a Status the card already holds.

## Why this fixture exists

Seen 2026-11-03 on this repo: a worktree another live session holds carries its lock reason.
