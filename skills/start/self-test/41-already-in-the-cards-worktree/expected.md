# Expected — START-SELFTEST-41

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED` · `WROTE-NOTHING`

## Situation

`/phil:start 80`, run from inside `.claude/worktrees/issue-80-phil-start`, with card 80 already In Progress and assigned to `pmvanev`. The worktree reads `locked claude session issue-80-phil-start (pid …)`: this session's own lock.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. WORKTREE sees the session is already in the card's worktree, calls no tool, skips the lock ask, and reports `UNDERWAY: already in .claude/worktrees/issue-80-phil-start; next: /phil:resume`.

## What must NOT happen

- Ask whether to enter a worktree another session holds.
- Call EnterWorktree.
- Report that the session moved in.
- Recommend a route.
- Write a Status the card already holds.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-03: the second run, the slice brief's dogfood moment, had no rule.
