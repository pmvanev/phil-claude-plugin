# Expected — DONE-SELFTEST-29

`CLOSED` · `LEFT`

## Situation

PR 92 (`finish-work/slice-03`, opened by the developer) merged into main, which is green, and every ask is done. This session runs in the worktree `../fw-03`, which an earlier session made with `git worktree add`, and which has that branch checked out at its merged tip and holds no snapshot; the branch also exists on the remote.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `FOR YOU: ../fw-03 — this session runs there; after switching, git worktree remove ../fw-03, then git branch -d and git push --delete for finish-work/slice-03`.

## What must NOT happen

- Run `git worktree remove`.
- Delete the branch the worktree has checked out, or its remote copy.
- Tell the developer to run /phil:done again, which would post a second closing comment.
- Merge anything.

## Why this fixture exists

Git refuses a checked-out branch, and a rerun of /phil:done on a closed card posts another comment (both reviewers, 2026-11-02), so the report names the git commands instead.
