# Slice 03 — Drill one level into the largest slice

**Goal.** When the split leaves the largest slice unexplained, the skill proposes the next instrument,
then reads its output and names the cause.

**Story:** US-03 · **Job:** make-a-lambda-web-app-load-fast

## IN scope
- The drill-down step: propose an instrument only for an unexplained slice, state its INIT cost, ask the
  person to deploy it (D12), then read it.
- A reference Python cold-start timing line: each phase and check, then each network call or connection
  leg, timed by the clock rather than summed across concurrent work.
- The rule's Principle on fixing the largest slice first and re-measuring as the constraint moves.

## OUT scope
- Fixing modive's connection; that goes to modive's own card.
- Ranking (slice 04).

## Learning hypothesis
Disproves "one more level of timing names the cause" **if** modive's 6.5 s first connection stays
unexplained after its legs are timed.

## Acceptance criteria
See US-03 in `feature-delta.md`.

## Dependencies
- Slice 02.

## Effort / reference class
≤ 1 day. Reference class: beatrix 254's two instrument passes (per phase, then per AWS call).

## Production data
With the user, modive's simulation API: the first Postgres connection's legs timed on its dev stack.
