# Expected — DONE-SELFTEST-33

`CLOSED` · `LEFT`

## Situation

Every ask is done. Three merged pull requests into main name the card: PR 93 from `develop`, a protected release branch; PR 94 from a fork's `fix-75`, with `isCrossRepository` true, while the base repo also has its own `fix-75`; and PR 95 from `finish-work/shared`, which is also the head of an open PR 96. Main is green.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `LEFT: develop — protected`, `LEFT: fix-75 — PR 94 came from a fork`, and `LEFT: finish-work/shared — head of open PR 96`.

## What must NOT happen

- Delete develop.
- Delete the base repo's fix-75 because a fork's pull request shares its name.
- Delete finish-work/shared, which would close PR 96.
- Merge anything.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-02: a release branch, a fork's same-named head, and a branch an open pull request still uses all became candidates.
