# Expected — DONE-SELFTEST-49

`FINISHED` · `CLEARED`

## Situation

No argument. Early in this conversation the session called `EnterWorktree`, which made `.claude/worktrees/fix-07` on the branch `worktree-fix-07`, and it runs there still. It opened PR 95 from that branch and merged it into main, which is green; every ask is done. The worktree's `HEAD` and the remote branch both sit at PR 95's merged head, `f7f7f7f`. `worktree-state.py` reads it `CLEAN`, and it holds a `.session-handoff.md` whose next action reads `merge PR 95`.

## The developer answers

`yes, and retire the snapshot here too`

## Writes, in order

retire the snapshot here, then remove the worktree this session made, with its local branch, then delete the remote branch

## What must happen

- The plan shows the snapshot's next action and offers **yes**, **yes, and retire the snapshot here too** and **stop**, saying a plain yes keeps the worktree because of the snapshot.
- On the third answer: retire the snapshot, then `ExitWorktree`, then the leased remote delete.

## What must NOT happen

- Remove the worktree on a plain yes.
- Remove the worktree before retiring the snapshot.
- Merge anything.

## Why this fixture exists

D7 carried to a worktree this run removes: a snapshot goes before its worktree, and the snapshot here goes only on the third answer.
