# Widget Service

Order-intake API for the warehouse team.

## Build & test

- Run `make test` before every commit.
- Set `TZ=UTC` before the integration tests. Wound: a runner in `America/Denver` broke every
  date-boundary assertion (2026-03-02).

## Workflow

- Name branches `wid-<ticket>-<slug>`.

Rationale and history cut 2026-09-01: git show 0000000:CLAUDE.md
