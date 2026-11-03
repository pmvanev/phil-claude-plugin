# Expected — START-SELFTEST-02

`NO-MATCH` · `WROTE-NOTHING`

## Situation

`/phil:start quantum flux capacitor`. The search for open cards returns `issueCount` 0.

## What must happen

The report says no open card matches, quoting the argument, and says this version cannot file a card.

## What must NOT happen

- File a card.
- Offer a closed card that matches.
- Route the argument as if it were a card.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.2. Filing arrives with the claim in slice 02; until then, a run with no match files nothing.
