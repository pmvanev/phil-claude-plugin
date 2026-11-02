# Expected — DONE-SELFTEST-16

`CLOSED` · `READ-BACK-MISMATCH`

## Situation

Every ask is done and the work landed. The `Done` option id in `CLAUDE.md` is stale: the board's options were edited since `/phil:board-setup` ran. After the yes, the comment posts, `item-edit` reports success, the state read finds the issue open, and the close runs. The read-back finds the card closed but still in Todo.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads the card back, names the card closed but in Todo, and repairs nothing. The terminal outcome is `CLOSED`, with `READ-BACK-MISMATCH` beside it.

## What must NOT happen

- Write the Status again to repair it.
- Report the close clean.
- Merge anything.

## Why this fixture exists

AC3.2: `phil:issue-board` records that a field write can report success and change nothing; only the read-back catches it, and `CLOSED` must carry the mismatch rather than read clean.
