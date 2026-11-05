# Slice 03 — Stop on a blocker, leave it resumable

**Goal (one sentence):** on a blocker the run comments on the card, runs `/phil:handoff` and ends
blocked, and the next run resumes at the step that stopped.

Story 3 · Decisions D1, D8, D9.

## IN scope
- The blocker comment: what stopped the run, its kind and the source line behind it.
- `/phil:handoff`, then a blocked outcome naming `/phil:autopilot <card>` to resume.
- Resuming at the stopped step from the snapshot.
- A write the path does not name — filing a new card included — stops before it is made.
- Fixtures: a blocker yields a comment and a snapshot (AC3.1); a resumed run skips finished steps
  (AC3.2); an unnamed write stops (AC3.3).

## OUT of scope
- Clearing the blocker; that is the developer's.

## Learning hypothesis
- **Disproves** "a snapshot carries enough to resume mid-path" if the resumed run repeats a finished
  step or asks a question the stopped run already answered.
- **Confirms** it if the resumed run starts at the stopped step with every earlier decision intact.

## Acceptance criteria
AC3.1–AC3.3 in `feature-delta.md`.

## Dependencies
Slice 02; `/phil:handoff` and `/phil:resume` (shipped).

## Effort estimate
≤1 day. Reference class: `session-handoff`'s handoff and resume pair.

## Production data
A card on this board whose path reaches a question about the developer's own material.

## Dogfood moment
The same day: stop on the blocker, clear it, rerun, and confirm the run resumes where it stopped.
