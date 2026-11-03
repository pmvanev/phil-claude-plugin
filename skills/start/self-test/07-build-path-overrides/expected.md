# Expected — START-SELFTEST-07

`LAUNCHED` · `BUILD-PATH` · `WROTE-NOTHING`

## Situation

`/phil:start 76`. The card asks for a new command, `/phil:autopilot`, and carries no `wave:` label. A user would see the change, so rule 3 alone would pick `phil:edd`. This repo's CLAUDE.md reads `Run nw-discuss before authoring a new feature, skill or command`. The developer answers **start it**.

## What must happen

ROUTE reads `nw-discuss`, quoting the CLAUDE.md rule and naming the file. On the yes, the run invokes `nw-discuss` through the Skill tool.

## What must NOT happen

- Recommend phil:edd.
- Name the route without citing the rule.
- Launch before the yes.
- Write a Status or assign anyone.

## Why this fixture exists

AC2.2. The repo's recorded build path comes before any default; this is the dogfood card the slice brief names.
