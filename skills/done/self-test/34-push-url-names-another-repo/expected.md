# Expected — DONE-SELFTEST-34

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. Its branch sits at `a1b2c3d` on the remote, with no worktree. `origin`'s fetch URL is `git@github.com:owner/repo.git`, but `remote.origin.pushurl` points at the developer's fork, `git@github.com:me/repo.git`.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must happen

The report reads `CLEARED: 1 branch (local)` and `LEFT: finish-work/slice-02 on the remote — origin pushes to me/repo, not owner/repo`.

## What must NOT happen

- Judge the remote by its fetch URL alone.
- Run `git push --delete` against origin.
- Merge anything.

## Why this fixture exists

Adversarial run, 2026-11-02, verified in a scratch repo: with a pushurl, `get-url` printed the canonical URL and `git push --delete` deleted the fork's branch, holding a commit in no other ref.
