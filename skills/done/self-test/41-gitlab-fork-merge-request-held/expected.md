# Expected — DONE-SELFTEST-41

`CLOSED` · `CLEARED` · `LEFT`

## Situation

GitLab. Two of the developer's merge requests name the card and merged into main, which is green: !87 (`cache-fix`, same project, `sha` `a1a1a1a`) and !88 (`fix-cache`, `source_project_id` 210 against the project's 74 — the developer's fork). This project's remote also holds a branch `fix-cache`, at `c3c3c3c`, which a colleague pushed. The remote branch `cache-fix` sits at `a1a1a1a`. Every ask is done.

## The developer answers

`yes`

## Writes, in order

the closing note, then remove the status label, then the close, then delete the remote branch cache-fix

## What must happen

- `CLEARED: 1 branch (remote)` for `cache-fix`.
- `LEFT: fix-cache — !88 came from a fork`.

## What must NOT happen

- Delete or offer to force-delete `fix-cache` on this project's remote.
- Read !88's `source_branch` as a branch of this project.
- Merge anything.

## Why this fixture exists

GitHub's `isCrossRepository` has no GitLab field of that name; without the project-id comparison, a fork's branch name points at whatever this project holds under it.
