# Slice 04 — Land the work

**Goal (one sentence):** the run pushes, opens the pull request, merges on a green pipeline and closes
the card through `/phil:done`, keeping the card's label, block and Status current at each step.

Story 4 · Decisions D4, D5, D7.

## IN scope
- The push, the pull request and the merge, each made without an ask after the authorization comment
  (D4); never a merge on red; a failure it cannot fix within its attempts is a blocker.
- `/phil:done`, its yes answered by D4.
- The `wave:` label, the generated block and Status at each step boundary (D7).
- Fixtures: a red pipeline never merges (AC4.2); each boundary updates the card (AC4.3).

## OUT of scope
- In-browser checks (slice 05).

## Learning hypothesis
- **Disproves** "an implied yes is enough to land work" if the developer, reading a landed card,
  wishes any of its writes had asked first.
- **Confirms** it if the developer reads the card and changes nothing about what was written.

## Acceptance criteria
AC4.1–AC4.3 in `feature-delta.md`.

## Dependencies
Slice 03; `/phil:done` (shipped).

## Effort estimate
≤1 day. Reference class: `finish-work` slice 03, the close and cleanup.

## Production data
The next small card on this board, carried end to end.

## Dogfood moment
The same day: a card on this board goes from `/phil:autopilot` to closed with no question asked.
