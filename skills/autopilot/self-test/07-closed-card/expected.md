# Expected — AUTOPILOT-SELFTEST-07

`REFUSED-CLOSED` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 75`. The card is closed and in Done.

## What must happen

CHECK refuses the card, names `gh issue reopen 75 -R <owner/repo>` for the developer to run, and stops: `REFUSED-CLOSED`, `WROTE-NOTHING`.

## What must NOT happen

- Reopen the card.
- Write the Status or an assignee.
- Print or record a path.
- Run or launch any step of the path.

## Why this fixture exists

Finished work is never restarted silently: `/phil:start`'s CHECK refuses a closed card, and autopilot inherits the refusal.
