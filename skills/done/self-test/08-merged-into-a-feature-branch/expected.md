# Expected — DONE-SELFTEST-08

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

The card's one pull request merged, but into `finish-work/slice-02`, a stacked branch, not into main. Every ask names it. Main's head is SUCCESS.

## What must happen

LANDED reads `NOT LANDED: PR 85 merged into finish-work/slice-02, not main`. The asks citing it are open. The verdict is NOT READY.

## What must NOT happen

- Count a merge into any branch as landed.
- Merge the stacked branch into main.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

plugin-validator, 2026-11-02: the query fetched each pull request's base and the landing rule never read it, so a stacked merge counted as landed.
