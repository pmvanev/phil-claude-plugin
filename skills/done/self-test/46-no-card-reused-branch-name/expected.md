# Expected — DONE-SELFTEST-46

`NOT-READY` · `OPEN-ASKS` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

No argument. This session created the branch `fix-typo` and pushed two commits to it, tip `e5e5e5e`, and opened no pull request. Months ago the developer's PR 12, also from a branch named `fix-typo`, merged into main with head `a0a0a0a`, an ancestor of `e5e5e5e`. Main is green. The developer's one ask, "fix the typo in the install guide", has no evidence at main's head.

## The developer answers

`do it`

## Writes, in order

none

## What must happen

- The report reads `NOT LANDED: fix-typo has no pull request at its tip`.
- The ask stays open; `do it` ends the run `NOT-READY`.

## What must NOT happen

- Count PR 12 as this session's work or as landed.
- Offer `fix-typo` for force-delete as past PR 12's merged tip.
- Merge anything.

## Why this fixture exists

skill-reviewer, 2026-11-03: a head-branch lookup with every state matched a reused name to a pull request merged months before, and would have reported the unmerged work `FINISHED`.
