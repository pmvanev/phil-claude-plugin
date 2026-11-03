# Expected — START-SELFTEST-17

`NO-MATCH` · `WROTE-NOTHING`

## Situation

`/phil:start 99999`. `gh` exits 1: `Could not resolve to an issue or pull request with the number of 99999` (`NOT_FOUND`).

## What must happen

The report says no card has that number, and stops.

## What must NOT happen

- Report CANNOT-RUN for a NOT_FOUND.
- Search for 99999 as words.
- Write a Status or assign anyone.

## Why this fixture exists

plugin-validator, run live 2026-11-03: a number naming nothing errors; it never answers null.
