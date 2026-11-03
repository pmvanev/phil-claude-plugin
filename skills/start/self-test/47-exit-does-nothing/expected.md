# Expected — START-SELFTEST-47

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-FAILED`

## Situation

`/phil:start 95` from a session launched inside `.claude/worktrees/done-gitlab-no-card`, not entered with EnterWorktree. The developer answers **move**, then **not now**. ExitWorktree reports no worktree session is active.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. After ExitWorktree, `git rev-parse --show-toplevel` still names the other worktree, so WORKTREE cuts nothing and reports `WORKTREE-FAILED`, naming where the session is.

## What must NOT happen

- Cut a worktree from inside another worktree.
- Call ExitWorktree with remove.
- Report WORKTREE-CUT.
- Remove an assignee.

## Why this fixture exists

plugin-validator and skill-reviewer, 2026-11-03: ExitWorktree acts only on a worktree this session entered.
