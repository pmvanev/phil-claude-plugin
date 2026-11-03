# Expected — START-SELFTEST-45

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED`

## Situation

`/phil:start 95`. No folder under `.claude/worktrees/` starts `issue-95-`, but `.claude/worktrees/uploads-retry` is checked out on `fix/uploads-retry`, the head branch of the developer's open PR whose body names issue 95.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. WORKTREE finds the worktree by the pull request's head branch, enters it, and names `/phil:resume`.

## What must NOT happen

- Miss the worktree because its folder name differs.
- Cut a second worktree.
- Remove an assignee.

## Why this fixture exists

D3's second rule: a worktree is the card's when it holds the branch of the developer's open pull request.
