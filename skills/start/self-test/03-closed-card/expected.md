# Expected — START-SELFTEST-03

`REFUSED-CLOSED` · `WROTE-NOTHING`

## Situation

`/phil:start 75`. Issue 75 is closed; its Status is Done.

## What must happen

The report says the card is closed, names `gh issue reopen 75 -R pmvanev/phil-claude-plugin` for the developer to run, and stops.

## What must NOT happen

- Reopen the card.
- Claim, describe or route the card.
- Ask whether to go on.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.3, and issue 80's third fixture behaviour: a closed card is never restarted silently.
