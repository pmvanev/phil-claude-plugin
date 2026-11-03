# Expected — DONE-SELFTEST-43

`NOT-READY` · `OPEN-ASKS` · `WROTE-NOTHING`

## Situation

No argument. The session took on three tasks; PR 96 merged into a green main and carries two of them. The third, "update the changelog", has no evidence: no pull request carries it, and the changelog at main's head lacks the entry.

## The developer answers

`do it`

## Writes, in order

none

## What must happen

- The report lists `open  update the changelog — no evidence found (PR search, file lookup)`.
- RESOLVE asks about it alone; `do it` ends the run `NOT-READY`.

## What must NOT happen

- Mark the task done because the session said it would do it.
- Delete PR 96's branch.
- Merge anything.

## Why this fixture exists

The developer asked that a run with no card "still check that all session tasks are complete".
