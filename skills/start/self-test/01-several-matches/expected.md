# Expected — START-SELFTEST-01

`NOT-LAUNCHED` · `PICKED` · `BUILD-PATH` · `WROTE-NOTHING`

## Situation

`/phil:start worktree` on this repo. Three open cards match: 89 (the handoff snapshot lands in the shell's worktree), 80 (`/phil:start`) and 76 (`/phil:autopilot`). The developer picks the `/phil:autopilot` card: open, in Todo, unassigned, labelled `enhancement` only, and linking no `docs/feature/` directory. The developer answers **not now** at the route.

## What must happen

The report lists all three by number and title above one question and waits. After the pick it runs CHECK on 76, describes it, and routes it to `nw-discuss`, quoting CLAUDE.md's build path.

## What must NOT happen

- Pick the closest match itself.
- Describe or route any card before the developer picks.
- Drop a match from the list.
- Write a Status or assign anyone.

## Why this fixture exists

AC1.1, and issue 80's first fixture behaviour: an ambiguous argument lists candidates instead of picking one.
