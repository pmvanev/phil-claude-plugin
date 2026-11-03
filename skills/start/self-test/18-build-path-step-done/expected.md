# Expected — START-SELFTEST-18

`NOT-LAUNCHED` · `BUILD-PATH` · `WROTE-NOTHING`

## Situation

`/phil:start 80` on this repo, after DISCUSS merged. The card links `docs/feature/start-work/`, which holds `feature-delta.md`. CLAUDE.md's build path reads `Run nw-discuss before authoring a new feature, skill or command`, then `Read plugin-dev:skill-development, command-development, agent-development or plugin-structure before writing the file`. The developer answers **not now**.

## What must happen

ROUTE names the build path's next step — read plugin-dev's command and skill guidance, then author — quoting CLAUDE.md, and never `nw-discuss`.

## What must NOT happen

- Recommend nw-discuss again.
- Fall through to phil:edd while the build path names a next step.
- Write a Status or assign anyone.

## Why this fixture exists

skill-reviewer, 2026-11-03: the build path sent card 80 back through a wave that had run.
