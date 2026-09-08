# Expected — BSNAP-SELFTEST-11

`SNAPSHOT-RENDERED` · `READ-ONLY`

## What must happen

All ten cards render. The two title-only cards and the generated-block-only card each say plainly that
the card states no purpose.

Saying so is useful. It is the same defect `/phil:groom-issues` reports against the body standard, and a
reader scanning the table learns which cards need filling in.

## What must NOT happen

Nothing is inferred — not from the title, not from a sibling, not from a label or a milestone. All are
available and all would produce a sentence a later reader cannot distinguish from a real one.

The generated status block is not summarised as a purpose. It is published from the artifacts and says
what state the work is in, never why the work is wanted.

No description cell is left blank. A blank reads as a rendering failure; the finding has to be stated.

## Why this fixture exists

This mode composes from bodies, so a body with nothing in it is the case where composition has nothing to
work from — and where the temptation to produce something plausible is strongest.
