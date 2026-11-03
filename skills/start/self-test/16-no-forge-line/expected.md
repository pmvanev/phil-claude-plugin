# Expected — START-SELFTEST-16

`CANNOT-RUN` · `WROTE-NOTHING`

## Situation

`/phil:start 12` in a repo whose CLAUDE.md has no forge line.

## What must happen

The report says no forge line was found, names `/phil:board-setup`, and stops.

## What must NOT happen

- Infer the repo from the git remote.
- Read the card anyway.
- Write a Status or assign anyone.

## Why this fixture exists

plugin-validator, 2026-11-03: an early stop matched no terminal outcome.
