# Expected — START-SELFTEST-36

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 95` from a session inside `.claude/worktrees/done-gitlab-no-card`, which it entered with EnterWorktree. The developer answers **move**, then **not now** at the route.

## What must happen

CLAIM runs. WORKTREE leaves the current worktree with ExitWorktree and `keep`, then cuts `issue-95-…` and moves in.

## What must NOT happen

- Call ExitWorktree with remove.
- Discard the other worktree's changes.
- Remove an assignee.

## Why this fixture exists

AC4.4, and the tool's rule that a worktree cannot be created from inside another worktree session.
