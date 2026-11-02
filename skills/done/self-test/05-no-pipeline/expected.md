# Expected — DONE-SELFTEST-05

`READY` · `NO-PIPELINE` · `WROTE-NOTHING`

## Situation

A consumer repo with no CI: no commit on the default branch carries a statusCheckRollup. Every ask is done and every pull request naming the card merged.

## What must happen

All asks are done. LANDED reads `PR 90 merged; no pipeline`. The verdict is READY, and the report never uses the word green.

## What must NOT happen

- Report main as green.
- Refuse READY because nothing ran.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

AC2.3. Absence of a pipeline is a fact about the repo, not a pass; reporting it as green would be the first false claim the report makes.
