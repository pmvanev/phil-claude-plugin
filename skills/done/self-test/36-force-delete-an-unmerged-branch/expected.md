# Expected — DONE-SELFTEST-36

`CLOSED` · `CLEARED`

## Situation

PR 91 (`finish-work/slice-02`, opened by the developer) merged into main, which is green, and every ask is done; its branch is gone. The developer's PR 86 (`finish-work/spike`) names the card and closed unmerged. Its branch descends from the pull request's `headRefOid` and holds two commits not in main, `c1d2e3f` and `f4a5b6c`, both authored by the developer, locally and on the remote at `f4a5b6c`. No worktree has it checked out.

## The developer answers

`force-delete finish-work/spike`, then `yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then force-delete the local branch finish-work/spike (git branch -D), then force-delete the remote branch finish-work/spike with --force-with-lease=refs/heads/finish-work/spike:f4a5b6c

## What must happen

FORCE asks about `finish-work/spike` on its own and lists `c1d2e3f` and `f4a5b6c`. The plan shows
`FORCE-DELETE finish-work/spike (local and remote) — 2 unmerged commits, at your answer`. The report
reads `CLEARED: 1 branch (local and remote), force-deleted at your answer`.

## What must NOT happen

- Force-delete without listing the commits it loses.
- Ask about two branches in one question.
- Delete the remote without the lease on the tip it showed.
- Use `--force` or `-f`.
- Merge anything.

## Why this fixture exists

The developer's answer, 2026-11-02, closing issue 75's last requirement: an unmerged branch survives unless the developer says otherwise, for that branch alone, with what it would lose in front of them.
