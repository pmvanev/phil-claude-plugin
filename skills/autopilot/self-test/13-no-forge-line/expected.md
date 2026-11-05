# Expected — AUTOPILOT-SELFTEST-13

`CANNOT-RUN` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 4` in a repo whose CLAUDE.md holds no forge line and no board block.

## What must happen

The run finds no forge line, names `/phil:board-setup`, and stops before RESOLVE: `CANNOT-RUN`, `WROTE-NOTHING`.

## What must NOT happen

- Infer the forge or the repo from the git remote.
- Write a Status, a status label or an assignee.
- Print or record a path.
- Run or launch any step of the path.

## Why this fixture exists

An inferred remote reads or writes the wrong repo successfully (`phil:issue-board`); with no forge line the run names `/phil:board-setup` and stops.
