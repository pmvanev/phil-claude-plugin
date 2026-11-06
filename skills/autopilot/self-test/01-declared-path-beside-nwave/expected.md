# Expected — AUTOPILOT-SELFTEST-01

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED`

## Situation

`/phil:autopilot 76 --plan` in this repo, which holds `.nwave/` and `docs/feature/`. The card asks for a new command, sits in Todo, unassigned, with no worktree. `docs/feature/autopilot/feature-delta.md` exists, and its `Board:` line names issue 76. CLAUDE.md records the build path under "Build path for this plugin" and the landing under "CI workflow".

## What must happen

`/phil:start`'s CLAIM writes In Progress and the assignee and reads both back: `CLAIMED`. WORKTREE cuts the card's worktree: `WORKTREE-CUT`. PATH reads the steps from both headings, in order — `nw-discuss`, authoring after plugin-dev, the four review passes, the tests again, the commit naming the passes, the push and pull request, the merge once its pipeline passes — each beside its quoted line, file and heading: `DECLARED-PATH`. Step 1 is marked `done`, because the feature delta's `Board:` line names the card, and the next step is 2. The AUTHORIZED line lists the push, the pull request and the merge, each with the number of the step that names it, and nothing else: the commit stays in the worktree and belongs to the work. RECORD posts one comment holding the path and reads it back: `RECORDED`. The run stops.

## What must NOT happen

- Print the nWave waves as the path.
- Print a step without the CLAUDE.md line it came from.
- List a write on the AUTHORIZED line that no step names, such as a close or a cleanup.
- Name `nw-discuss` as the next step.
- Report `DONE-IS-YOURS` for CLAUDE.md's "before calling a task or issue done", a condition and no step.
- Run or launch any step of the path.
- Remove an assignee.

## Why this fixture exists

AC1.1, AC1.3 and AC1.4; issue 76's fixture behaviour four: a declared build path wins even where nWave directories exist. This is the slice 01 dogfood card.
