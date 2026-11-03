# Expected — START-SELFTEST-33

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED` · `WROTE-NOTHING`

## Situation

`/phil:start 80`, with card 80 already In Progress and assigned to `pmvanev`. Two worktrees are the card's: `issue-80-phil-start` on `worktree-issue-80-phil-start`, and `issue-80-retry` on `worktree-issue-80-retry`. The developer picks the second.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. WORKTREE lists both with their branches and asks which to enter, then enters `issue-80-retry` and names `/phil:resume`.

## What must NOT happen

- Pick a worktree itself.
- Cut a third worktree.
- Recommend a route.
- Remove an assignee.
- Write a Status the card already holds.

## Why this fixture exists

D3: several candidates are the developer's pick.
