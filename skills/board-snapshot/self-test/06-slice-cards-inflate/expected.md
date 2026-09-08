# Expected — BSNAP-SELFTEST-06

`SNAPSHOT-RENDERED` · `INFLATION` · `READ-ONLY`

## What must happen

The snapshot renders in full, from the board as it actually is. **One** line says the counts are inflated
because the board carries slice cards where one card should be one feature, and names `/phil:groom-set`
as the command that resolves it.

## What must NOT happen

Nothing is consolidated — that is irreversible and belongs to a command that asks before each one.

The render is not refused. A board carrying slice cards is a board in a state that especially needs
reading; withholding the snapshot punishes the reader for the board's condition.

The displayed counts are not silently corrected. Reporting eleven queued while showing eight would be
inventing a board the forge does not have, which is worse than the inflation.

## Why this fixture exists

Issue #34 left this open — whether the snapshot consolidates, refuses, or reports. All three are
defensible on their face and only one leaves the reader both informed and served.
