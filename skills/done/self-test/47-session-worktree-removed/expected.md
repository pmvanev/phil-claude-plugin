# Expected — DONE-SELFTEST-47

`FINISHED` · `CLEARED`

## Situation

No argument. Early in this conversation the session called `EnterWorktree`, which made `.claude/worktrees/fix-07` on the branch `worktree-fix-07`, and it runs there still. It opened PR 95 from that branch and merged it into main, which is green; every ask is done. The worktree's `HEAD` and the remote branch both sit at PR 95's merged head, `f7f7f7f`. `git worktree list --porcelain` marks it `locked claude session fix-07 (pid 3131)`, Claude Code's lock for this session. `worktree-state.py` reads the worktree `CLEAN`, and it holds no snapshot.

## The developer answers

`yes`

## Writes, in order

remove the worktree this session made, with its local branch, then delete the remote branch

## What must happen

- The plan lists `remove worktree  .claude/worktrees/fix-07 — clean, at PR 95's merged tip, locked only by this session`.
- After the yes, the run reads `worktree-state.py` again, then calls `ExitWorktree` with `action: "remove"`; where it refuses the merged commit, it passes `discard_changes: true`, because the worktree read `CLEAN` at the merged tip.
- Then `git push --delete --force-with-lease=refs/heads/worktree-fix-07:f7f7f7f origin refs/heads/worktree-fix-07`.
- `CLEARED: 1 worktree, 1 branch (local and remote)`.

## What must NOT happen

- Pass `--force` to `git worktree remove`.
- Delete the remote branch before the worktree is gone.
- List the worktree for the developer to remove.
- Merge anything.

## Why this fixture exists

The developer, 2026-11-03, after the first run without a card left this session's worktree standing: "wait why didn't phil:done cleanup this session's worktree?"
