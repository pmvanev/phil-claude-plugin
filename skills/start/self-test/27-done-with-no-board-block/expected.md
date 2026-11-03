# Expected — START-SELFTEST-27

`NOT-LAUNCHED` · `OPEN-IN-DONE` · `NO-BOARD-BLOCK`

## Situation

`/phil:start 12` in a consumer repo whose CLAUDE.md holds a forge line and no board lines. Issue 12 is open, unassigned, and Done on the one project it is on. The developer answers **go on**, then **not now**.

## What must happen

The ask says going on leaves the card in Done, because no board block names a project. CLAIM writes no Status, assigns the developer and reads the assignee back; the report names `/phil:board-setup` and says the card is still in Done.

## What must NOT happen

- Promise that going on moves the card.
- Write a Status on the card's project.
- Probe the forge for a board.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-03: go on promised a move that CLAIM without a block never makes.
