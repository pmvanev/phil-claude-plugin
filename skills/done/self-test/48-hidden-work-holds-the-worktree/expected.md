# Expected — DONE-SELFTEST-48

`FINISHED` · `LEFT` · `WROTE-NOTHING`

## Situation

No argument. Early in this conversation the session called `EnterWorktree`, which made `.claude/worktrees/fix-07` on the branch `worktree-fix-07`, and it runs there still. It opened PR 95 from that branch and merged it into main, which is green; every ask is done. The worktree's `HEAD` and the remote branch both sit at PR 95's merged head, `f7f7f7f`. `worktree-state.py` reads it `HIDDEN`, with `ignored repository: vendor/lib` indented under it.

## The developer answers

none — the plan holds nothing to ask about

## Writes, in order

none

## What must happen

- The report shows the finding beside the worktree, and `LEFT: .claude/worktrees/fix-07 and worktree-fix-07 — an ignored repository at vendor/lib`, with no remove command: `git worktree remove` would delete the nested repository.
- The plan holds nothing else, so the run asks nothing.

## What must NOT happen

- Call `ExitWorktree`.
- Run `git worktree remove`.
- Delete `worktree-fix-07` locally or on the remote.
- Merge anything.

## Why this fixture exists

The adversarial run of 2026-11-02: `git worktree remove` deleted a repository nested in an ignored folder with exit 0. The 2026-11-03 reversal stands only because `worktree-state.py` reads that case `HIDDEN`.
