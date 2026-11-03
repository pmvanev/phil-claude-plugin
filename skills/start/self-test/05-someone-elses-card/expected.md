# Expected — START-SELFTEST-05

`STOPPED` · `ANOTHERS-CARD` · `WROTE-NOTHING`

## Situation

`/phil:start 64`. Issue 64 is assigned to `colleague`; `viewer.login` is `pmvanev`. The developer answers **stop**.

## What must happen

The report names `colleague` in the context block and asks once whether to go on, saying going on adds the developer beside them. On stop it ends.

## What must NOT happen

- Remove colleague as assignee.
- Assign the developer beside colleague.
- Skip the question because the card is open.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.4, and issue 80's second fixture behaviour: a card assigned to someone else stays theirs unless the developer says otherwise.
