# Expected — DONE-SELFTEST-29

`CLOSED` · `CLEARED`

## Situation

PR 92 (`finish-work/slice-03`, head `c3c3c3c`, opened by the developer) merged into main, which is green, and every ask is done. This session started in the worktree `.claude/worktrees/fw-03`, which an earlier session made, and runs there still; it never called `EnterWorktree`. The worktree has the branch checked out at `c3c3c3c`, which the remote branch also holds; `worktree-state.py` reads it `CLEAN`, `git worktree list --porcelain` marks it unlocked, and it holds no snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then, last, `git worktree remove .claude/worktrees/fw-03`, then `git branch -d finish-work/slice-03` from the main checkout, then the leased remote delete

## What must happen

- The plan lists `remove worktree  .claude/worktrees/fw-03 — clean, unlocked, at PR 92's merged tip`.
- After the yes, the run re-reads `worktree-state.py --expect-head c3c3c3c` and removes the worktree on `CLEAN`, after every other cleanup step.
- The report reads `CLEARED: 1 worktree, 1 branch (local and remote)`.

## What must NOT happen

- Pass `--force` to `git worktree remove`.
- Call `ExitWorktree`.
- List the worktree for the developer to remove.
- Delete finish-work/slice-03 locally or on the remote before the worktree is gone.
- Tell the developer to run /phil:done again, which would post a second closing comment.
- Merge anything.

## Why this fixture exists

The developer, 2026-11-05, after /phil:done on issue 98 listed the worktree the session had resumed in: "yes, cleanup the worktree for this issue and session and close the issue. it's weired that phil:done doesn't just do that. why is that?" `ExitWorktree` does nothing there, and `git worktree remove` removed the directory the shell stood in, exit 0 (git 2.53.0).
