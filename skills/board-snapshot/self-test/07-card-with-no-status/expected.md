# Expected — BSNAP-SELFTEST-07

`SNAPSHOT-RENDERED` · `UNCOLUMNED` · `READ-ONLY`

## What must happen

The three sections render without the uncolumned card. **One** line names it and says it sits in no
column.

## What must NOT happen

No column is guessed for it. It is not folded into the queued section, which would give it a board
position the forge never assigned.

It is not omitted. A card appearing in no section and no line has vanished from a read whose whole purpose
is telling the reader what is there.

Its Status is not set. That is `phil:issue-board`'s territory and needs a write this command does not hold.

## Why this fixture exists

`phil:issue-board` records that an issue never added to a project has no Status and is invisible in a
kanban grouped by it. The same holds one step later, for a card added and never placed — and a bounded
read is exactly where a silent omission is hardest to notice.
