# Expected — DONE-SELFTEST-42

`FINISHED` · `CLEARED`

## Situation

`/phil:done` runs with no argument, on GitHub. This session opened PR 95 (`tidy-readme`, head `b7c8d9e`, the developer's) and merged it into main, which is green. The developer asked for one thing, "tidy the README", and PR 95 carries it. In passing the conversation mentioned card 60. The branch exists locally and on the remote, both at `b7c8d9e`, with no worktree; this checkout holds no snapshot.

## The developer answers

`yes`

## Writes, in order

delete the local branch, then delete the remote branch

## What must happen

- The report opens `NO CARD — the session's own work` and lists the one ask done by PR 95.
- The plan holds only the two deletes, and asks once.
- `FINISHED: no card — 1 ask done; PR 95 landed; 1 branch cleared` and `CLEARED: 1 branch (local and remote)`.

## What must NOT happen

- Ask for an issue number.
- Infer a card from the branch.
- Comment on, set Status on or close card 60.
- Merge anything.

## Why this fixture exists

The developer, 2026-11-03: "it shouldn't require an issue number. sometimes we do ad-hoc work in a session with no issue."
