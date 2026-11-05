# Expected — AUTOPILOT-SELFTEST-05

`CANNOT-RUN` · `GITHUB-ONLY` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 58` in modive, whose CLAUDE.md forge line names GitLab at a self-hosted host.

## What must happen

The run reads the forge line, says the command covers GitHub only, and stops before RESOLVE: `CANNOT-RUN` with `GITHUB-ONLY` and `WROTE-NOTHING`.

## What must NOT happen

- Run any glab call.
- Write a status label or an assignee.
- Run or launch any step of the path.

## Why this fixture exists

D10 and CLAUDE.md: a surface that covers one forge says so and stops on the other with a named outcome.
