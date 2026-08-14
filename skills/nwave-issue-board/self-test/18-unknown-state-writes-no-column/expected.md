# Expected — 18 (no column means no write, not the nearest column)

**Pins:** *Six states, four columns* — the two states with no column are never coerced into one.

**Expected outcome:** `NO-COLUMN-WRITTEN`. **No Status write is issued at all.** The card stays in whatever
column it was already in, and the generated block says why:

```
Feature state: unknown — no progress record of any kind
Column not set: the board has no column for `unknown`, so this card's position
                is whatever it already was and does not reflect its state.
```

**Why this is the trap and not an edge case.** The card is *already* in `Todo`, and `unknown` folds from a
feature with nothing recorded — so `Todo` looks not merely acceptable but already true. It is not true, and
the difference is the whole point: `Todo` asserts *nobody has started this*, while `unknown` asserts
*nobody has checked*. A reader scanning the column cannot tell those apart, and the second one is a
question, not a status.

This is the sibling skill's cardinal rule — `unknown` is never published as `not started` — applied one
level up, where it is read by more people and inspected by fewer. `deferred` fails the same way more
quietly: `Todo` invites someone to pick up a feature its own artifacts set aside.

**Gate failures:**

- Writing `Todo`. The defect, and it is invisible afterwards: the card looks correctly placed.
- Writing `Todo` *because the card was already there*. Re-asserting a value is still asserting it, and the
  write is what turns an accident into a claim.
- Creating an `Unknown` column. Not this skill's call, and a fifth column for a non-state is how the
  wave-column noise problem starts again.
- Removing the card from the board so it has no column. Absence is a stronger claim than silence, and it
  loses the card.
- Writing the column and noting `unknown` in the block. The note does not undo the write, and the column
  is what gets read.
