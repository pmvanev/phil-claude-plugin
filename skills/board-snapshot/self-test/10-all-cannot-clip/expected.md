# Expected — BSNAP-SELFTEST-10

`SNAPSHOT-RENDERED` · `READ-ONLY`

## What must happen

Two hundred rows. Every open card, in board order, each with a description within the per-row bound.

## What must NOT happen

Nothing is clipped, truncated, paginated or replaced by a count. No offer is made to render fewer —
offering the drop is how the drop happens.

Descriptions are not squeezed below what their cards need in order to shorten the total. The per-row
bound is a ceiling on each row, not a budget shared between them.

## Why this fixture exists

Two hundred cards is exactly where a total ceiling feels justified, and it is where applying one would do
the most damage. A reader asking what is on the board is asking about all of it; a table that answers for
a quarter of it has answered a question nobody asked.
