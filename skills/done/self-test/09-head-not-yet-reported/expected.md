# Expected — DONE-SELFTEST-09

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Every ask is done and the card's pull request merged into main a minute ago. Main's head commit carries no statusCheckRollup yet; the twenty commits before it each carry SUCCESS.

## Writes, in order

None.

## What must happen

LANDED reads `NOT LANDED: main's head has not reported yet`. `NO-PIPELINE` does not fire. The verdict is NOT READY.

## What must NOT happen

- Report no pipeline because the head has no rollup.
- Call main green from an older commit's rollup.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

skill-reviewer, 2026-11-02: no fixture distinguished a head the pipeline has not reached from a repo with no pipeline, and the two have opposite verdicts.
