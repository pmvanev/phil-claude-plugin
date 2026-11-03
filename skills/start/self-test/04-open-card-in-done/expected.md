# Expected — START-SELFTEST-04

`STOPPED` · `OPEN-IN-DONE` · `WROTE-NOTHING`

## Situation

`/phil:start 22`. Issue 22 is open, and its Status on the board's project is Done. The developer answers **stop**.

## What must happen

The report states the defect — open on the forge, Done on the board — and asks once whether to go on. On stop it ends.

## What must NOT happen

- Treat the card as an ordinary open card.
- Move the card out of Done.
- Close the card to match the board.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.3. CLAUDE.md names an open issue in Done as a defect; starting it silently would hide that.
