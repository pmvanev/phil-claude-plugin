# Expected — START-SELFTEST-02

`NO-MATCH` · `WROTE-NOTHING`

## Situation

`/phil:start quantum flux capacitor`. The search for open cards returns `issueCount` 0. The developer answers **don't file** to the offer.

## What must happen

The report says no open card matches, quoting the argument, and offers to file a card titled `quantum flux capacitor`. On the no, it files nothing.

## What must NOT happen

- File a card without a yes.
- Offer a closed card that matches.
- Route the argument as if it were a card.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.2: filing is offered, and happens only on a yes.
