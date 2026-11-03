# Expected — START-SELFTEST-15

`LAUNCHED` · `BUILD-PATH` · `WROTE-NOTHING`

## Situation

`/phil:start /phil:autopilot` on this repo. The search, with the argument as given, returns `issueCount` 1: card 76. The developer answers **start it**.

## What must happen

The run reads 76 with the number query, describes it and routes it to `nw-discuss` by CLAUDE.md's build path. It prints the outcome tokens, then invokes `nw-discuss` through the Skill tool.

## What must NOT happen

- Report NO-MATCH.
- Strip `/phil:autopilot` as if it were a search qualifier.
- Report outcomes after the launch.
- Write a Status or assign anyone.

## Why this fixture exists

The slice brief's dogfood moment. Run live 2026-11-03: the search reads the colon in `/phil:autopilot` as text, not as a qualifier.
