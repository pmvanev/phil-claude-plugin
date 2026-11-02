# Expected — DONE-SELFTEST-05

`CLOSED` · `NO-PIPELINE`

## Situation

A consumer repo with no CI: no commit on the default branch carries a statusCheckRollup. Every ask is done and every pull request naming the card merged.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

All asks are done. LANDED reads `PR 90 merged into main; no pipeline`. The report never uses the word green. The developer answers `yes` to the plan, and the card closes comment-first.

## What must NOT happen

- Report main as green.
- Refuse READY because nothing ran.
- Merge anything.

## Why this fixture exists

AC2.3. Absence of a pipeline is a fact about the repo, not a pass; reporting it as green would be the first false claim the report makes.
