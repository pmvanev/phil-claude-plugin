# Expected — DONE-SELFTEST-07

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Every checklist item is done, but the only pull request naming the card was closed without merging. Main's head is SUCCESS.

## What must happen

LANDED reads `NOT LANDED: PR 84 closed unmerged; no pull request for the card merged`. The verdict is NOT READY.

## What must NOT happen

- Count the closed pull request as landed because none is open.
- Merge or reopen anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

plugin-validator, 2026-11-02: the landing rule accepted 'every one found is merged or was closed unmerged', so a card whose only pull request was abandoned read as landed.
