# Expected — START-SELFTEST-14

`NOT-LAUNCHED` · `ANOTHERS-CARD` · `CLAIMED`

## Situation

`/phil:start 64`. Issue 64 is in Todo, assigned to `colleague`; `viewer.login` is `pmvanev`. The developer answers **go on**, then **not now** at the route.

## What must happen

On go on, CLAIM writes Status In Progress and adds `pmvanev` beside `colleague`, reading both back — `colleague` still among the assignees: `CLAIMED: … assigned to pmvanev beside colleague — read back`.

## What must NOT happen

- Remove colleague.
- Replace colleague with the developer.
- Assign before the go-on answer.

## Why this fixture exists

AC1.4 and AC3: another's card answered yes adds the developer beside them, never in their place.
