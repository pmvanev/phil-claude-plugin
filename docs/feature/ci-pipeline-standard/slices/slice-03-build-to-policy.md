# Slice 03 — Build a pipeline to the declared policy

**Goal.** `/phil:build-ci` declares a project's policy, then writes or edits its pipeline so that the
trigger matrix matches that policy in every cell.

**Story:** US-03 · **Job:** shape-a-pipeline-to-the-change

## IN scope
- `skills/build-ci/SKILL.md` and `commands/build-ci.md` (`mutates: true`).
- Steps: confirm or ask for the policy; write the `CLAUDE.md` block; map change classes to jobs; write
  jobs as entry-point script calls (D13); print the matrix; lint; read the forge's merge gate and ask
  before changing it (D15); document the branch, MR, merge-on-green workflow.
- Self-test fixture `01-empty-project/`: a project with no CI, and the matrix it must reach.

## OUT scope
- Speed and rework passes (slice 04). Runner settings (slice 05).

## Learning hypothesis
Disproves "a procedure plus the rule gets a project to its policy in one run" **if** the dogfood run
needs a user correction to the policy or to any matrix cell.

## Acceptance criteria
See US-03 in `feature-delta.md`.

## Dependencies
- Slices 01 and 02.

## Effort / reference class
≤ 1 day. Reference class: `board-setup` (writes a delimited CLAUDE.md block after probing the forge).

## Production data
One real repo, run with the user, its matrix recorded.
