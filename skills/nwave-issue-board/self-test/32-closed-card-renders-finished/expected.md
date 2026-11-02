# Expected — 32-closed-card-renders-finished

## What must happen

The refresh reads `references/projection.md` because the card is closed. The position half renders as on
any refresh. The reasoning half is one line: `Finished 2026-11-03.` — the UTC date of the issue's
`closedAt`.

## What must NOT happen

- The snapshot's why, next action or stack appear on the closed card.
- Any reasoning section reads `unknown`.
- The date comes from local time or from the snapshot.
- The finished state is read from a marker a command left, not from the closed issue.

## Why this fixture exists

A closed card's projected next action sends a reader to work that is finished. Once `/phil:done` clears
the snapshot, a plain refresh would render `Stack: unknown`, a claim that the record is missing when the
work is done.
