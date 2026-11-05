# Slice 04 — Land the work and hand it back

**Goal (one sentence):** the run pushes, opens the pull request and merges on a green pipeline, keeping
the card's label, block and Status current at each step, then runs `/phil:handoff` and names
`/phil:done` for the developer to run after inspecting the work.

Story 4 · Decisions D4, D5, D7, D13.

## IN scope
- The push, the pull request and the merge, each made without an ask after the authorization comment
  (D4); never a merge on red; a failure it cannot fix within its attempts is a blocker.
- The `wave:` label, the generated block and Status at each step boundary (D7).
- The end: `/phil:handoff`, then an outcome naming `/phil:done` for the developer. Never `/phil:done`,
  never a close (D13).
- Both forges: a merge request and its pipeline on GitLab (D10).
- Fixtures: a red pipeline never merges (AC4.2); each boundary updates the card (AC4.3); a finished run
  hands off and leaves the card open (AC4.4).

## OUT of scope
- In-browser checks (slice 05).

## Learning hypothesis
- **Disproves** "an implied yes is enough to land work" if the developer, inspecting a landed card,
  wishes any of its writes had asked first.
- **Confirms** it if the developer inspects the work and runs `/phil:done` with nothing to undo.

## Acceptance criteria
AC4.1–AC4.4 in `feature-delta.md`.

## Dependencies
Slice 03; `/phil:handoff` (shipped).

## Effort estimate
≤1 day. Reference class: `finish-work` slice 03, a merged-work check with read-back.

## Production data
The next small card on this board, carried to a merged change.

## Dogfood moment
The same day: a card on this board goes from `/phil:autopilot` to merged and handed back with no
question asked; the developer inspects it and runs `/phil:done`.
