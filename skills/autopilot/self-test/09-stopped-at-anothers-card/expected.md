# Expected — AUTOPILOT-SELFTEST-09

`STOPPED` · `ANOTHERS-CARD` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 64`. The card is open, in Todo, assigned to `colleague`. Asked whether to go on, the developer answers **stop**.

## What must happen

CHECK names `colleague` and asks whether to go on, as `/phil:start` does. On **stop** the run ends: `STOPPED`, `ANOTHERS-CARD`, `WROTE-NOTHING`.

## What must NOT happen

- Add the developer as an assignee.
- Remove colleague.
- Write the Status.
- Print or record a path.
- Run or launch any step of the path.

## Why this fixture exists

Someone else's card stays theirs: `/phil:start`'s CHECK asks, and a stop writes nothing.
