# Expected — START-SELFTEST-30

`STOPPED` · `WROTE-NOTHING`

## Situation

`/phil:start 99`. Issue 99 is open and in Blocked on the board's project. The developer answers **stop**.

## What must happen

The report says the card is blocked and asks once whether to go on, saying going on moves it to In Progress. On stop it ends.

## What must NOT happen

- Move the card out of Blocked without asking.
- Treat Blocked as a defect.
- Write a Status or assign anyone.

## Why this fixture exists

skill-reviewer, 2026-11-03: a card in Blocked left it silently, hiding the blocker.
