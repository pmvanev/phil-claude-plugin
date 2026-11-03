# Expected — START-SELFTEST-12

`STOPPED` · `WROTE-NOTHING`

## Situation

`/phil:start board`. The search returns `issueCount` 34. The developer gives no narrower words.

## What must happen

The report says 34 open cards match and asks for narrower words, offering no pick among the first 20.

## What must NOT happen

- Offer any of the 34 as a pick.
- Pick the first hit.
- Write a Status or assign anyone.

## Why this fixture exists

D4: a list the query cut short is never offered as the whole.
