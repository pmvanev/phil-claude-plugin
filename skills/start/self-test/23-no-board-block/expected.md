# Expected — START-SELFTEST-23

`NOT-LAUNCHED` · `NO-BOARD-BLOCK`

## Situation

`/phil:start 12` in a consumer repo whose CLAUDE.md holds a forge line and no board block. The card is open and unassigned. The developer answers **not now**.

## What must happen

The report names `/phil:board-setup`, writes no Status, assigns the developer and reads the assignee back: `NO BOARD BLOCK: Status not written — run /phil:board-setup; assigned to pmvanev — read back`.

## What must NOT happen

- Probe the forge for a project or Status field.
- Write a Status.
- Report CLAIMED.

## Why this fixture exists

D8, AC3.4, and the learning hypothesis: the board block, not a probe, supplies the Status ids.
