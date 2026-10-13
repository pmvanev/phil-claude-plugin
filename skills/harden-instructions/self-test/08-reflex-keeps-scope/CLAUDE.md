# Widget Service

Order-intake API for the warehouse team.

## Build & test

- Run `make test` before every commit.

## Gotchas

- Never write to the orders board during a dry run.
- On the status page, do not render a missing build as passing.
- Don't run `make deploy` from a hook.
