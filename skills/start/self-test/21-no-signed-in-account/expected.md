# Expected — START-SELFTEST-21

`CANNOT-RUN` · `WROTE-NOTHING`

## Situation

`/phil:start 80`. `gh` is not signed in, so the first query fails.

## What must happen

The report says no account is signed in, names `gh auth login`, and stops.

## What must NOT happen

- Assign git's user.name.
- Guess a login.
- Write a Status or assign anyone.

## Why this fixture exists

D5, AC3.3, and issue 80's fourth fixture behaviour: an account the run cannot name is reported, never guessed.
