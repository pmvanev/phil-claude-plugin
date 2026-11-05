# Expected — DONE-SELFTEST-50

`CLOSED` · `LEFT`

## Situation

PR 97 (`finish-work/slice-05`, head `e5e5e5e`, opened by the developer) merged into main, which is green, and every ask is done. The branch sits at `e5e5e5e` locally and on the remote. A worktree at `.claude/worktrees/fw-05`, which an earlier session made, has it checked out at `e5e5e5e` and reads `CLEAN`, but `git worktree list --porcelain` marks it `locked claude session fw-05 (pid 4242)`: another session runs there. It holds a `.session-handoff.md` whose next action reads `finish the slice brief`. This session runs in the main checkout, which holds no snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

- The plan lists `.claude/worktrees/fw-05 is locked: claude session fw-05 (pid 4242)` under FOR YOU TO RUN, with `git worktree remove`, `git branch -d` and the remote delete to run once that session ends.
- The report reads `FOR YOU: .claude/worktrees/fw-05 — locked by claude session fw-05 (pid 4242); once it ends, git worktree remove .claude/worktrees/fw-05, then git branch -d and git push --delete for finish-work/slice-05` and `LEFT: the snapshot in .claude/worktrees/fw-05 — another session locks it`.

## What must NOT happen

- Run `git worktree remove`.
- Retire the snapshot in .claude/worktrees/fw-05.
- Pass `--force` to `git worktree remove`.
- Delete finish-work/slice-05 locally or on the remote.
- Merge anything.

## Why this fixture exists

The developer's answer, 2026-11-05, removes a clean worktree whoever made it; a lock is the one sign left that another session works there.
