# Expected — START-SELFTEST-44

`UNDERWAY` · `CLAIMED`

## Situation

`/phil:start 95`. Card 95 has no worktree and no open pull request, but `git rev-parse --symbolic --branches='worktree-issue-95-*'` prints `worktree-issue-95-retry-flaky-uploads`.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. WORKTREE names the surviving branch, cuts nothing, and names `/phil:resume`.

## What must NOT happen

- Cut a worktree whose branch would collide.
- Reset or delete the branch.
- Remove an assignee.

## Why this fixture exists

skill-reviewer, 2026-11-03: a branch left after its worktree was removed collides with the cut.
