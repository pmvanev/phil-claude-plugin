# Expected — DONE-SELFTEST-12

`NOT-READY` · `OPEN-ASKS` · `WROTE-NOTHING`

## Situation

The card has no checklist and no Done-when heading. Under `## What it does` it lists four numbered steps; the merged pull request delivers the first two. Main's head is SUCCESS.

## The developer answers

`do it`

## Writes, in order

None.

## What must happen

ASKS reads `4: 2 done, 2 open`. LANDED is green. The verdict is NOT READY: 2 open asks. The developer answers `do it`, so the run stops and closes nothing.

## What must NOT happen

- Read a card with no checkboxes as having no asks.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

Dogfood, `/phil:done 75` on 1.17.0 (2026-11-02): the card's six steps sat under *What it does*, outside every source the skill read, and reached the report only by accident.
