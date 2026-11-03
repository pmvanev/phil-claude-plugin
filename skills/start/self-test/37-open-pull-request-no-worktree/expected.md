# Expected — START-SELFTEST-37

`UNDERWAY` · `CLAIMED` · `WROTE-NOTHING`

## Situation

`/phil:start 80` on a second machine, with card 80 already In Progress and assigned to `pmvanev`. The developer's PR 94 is open, names issue 80, and is on `worktree-issue-80-phil-start`; this clone has no worktree for the card.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. WORKTREE names the pull request and its head branch, cuts nothing, and names `/phil:resume`.

## What must NOT happen

- Cut a fresh worktree from the default branch.
- Recommend a route.
- Remove an assignee.
- Write a Status the card already holds.

## Why this fixture exists

D2: an open pull request means the work is underway, and a fresh worktree would restart it.
