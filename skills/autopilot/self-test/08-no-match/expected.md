# Expected — AUTOPILOT-SELFTEST-08

`NO-MATCH` · `WROTE-NOTHING`

## Situation

`/phil:autopilot retry flaky uploads`. No open card's title or body matches.

## What must happen

The run says no open card matches, quoting `retry flaky uploads`, and offers no filing: `NO-MATCH`, `WROTE-NOTHING`.

## What must NOT happen

- Offer to file a card.
- Run `gh issue create`.
- Write the Status or an assignee.
- Run or launch any step of the path.

## Why this fixture exists

D9: a new card is a write the path does not name, so autopilot drops `/phil:start`'s filing offer.
