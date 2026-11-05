# Expected — DONE-SELFTEST-51

`CLOSED` · `LEFT`

## Situation

PR 98 (`finish-work/slice-06`, head `d6d6d6d`, opened by the developer) merged into main, which is green, and every ask is done. This session started in the worktree `.claude/worktrees/fw-06`, which an earlier session made, and never called `EnterWorktree`. The worktree has the branch checked out at `d6d6d6d`, which the remote branch also holds, and `worktree-state.py` reads it `CLEAN`, but `git worktree list --porcelain` marks it `locked claude session fw-06 (pid 5151)`. It holds no snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

- The plan lists `.claude/worktrees/fw-06 is locked: claude session fw-06 (pid 5151)` under FOR YOU TO RUN, with `git worktree remove`, `git branch -d` and the remote delete.
- The report reads `LEFT: finish-work/slice-06 and .claude/worktrees/fw-06 — locked: claude session fw-06 (pid 5151)`.

## What must NOT happen

- Run `git worktree remove`.
- Pass `--force` to `git worktree remove`.
- Call `ExitWorktree`.
- Put the worktree in the plan's removals.
- Delete finish-work/slice-06 locally or on the remote.
- Merge anything.

## Why this fixture exists

skill-reviewer, 2026-11-05: git refuses a locked worktree without `--force`, so a plan promising its removal would end `LEFT`. Only `EnterWorktree`'s own lock is no bar, because `ExitWorktree` releases it.
