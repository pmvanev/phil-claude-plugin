# Slice 02 — Take the recommendation and record it

**Goal (one sentence):** the run executes each step of the path through the command that owns it,
answers each question by a recorded rule or by its own recommendation, records every answer on the
card, and stops on a question of D1's three kinds.

Story 2 · Decisions D1, D6, D9, D12.

## Pre-slice spike (D12) — done 2026-11-05
`spike-d12/README.md` holds it. A `PreToolUse` hook on `AskUserQuestion` denies each ask during an
autopilot run, giving a reason that carries D1's three kinds and the recommended option. The skill
repeats the instruction for headless runs. Never pre-fill `answers`.

Open for authoring: how the hook knows a run is active. A marker holding the session id, as hook input
carries `session_id`, limits the denial to that session, and a crashed run cannot silence asks in the
next one.

## IN scope
- Answering by rule — the repo's `CLAUDE.md` and `AGENTS.md`, and the developer's saved preferences —
  naming the rule; otherwise by the recommendation.
- One card comment per step listing its decisions: question, option taken, reason.
- Classifying a question into D1's three kinds, and stopping on one (slice 03 owns the stop itself).
- Fixtures: a recommendation taken and recorded (AC2.2); a rule answers (AC2.1); a developer's
  decision stops the run (AC2.3).

## OUT of scope
- The handoff on a stop (slice 03); the push, merge and close (slice 04).

## Learning hypothesis
- **Disproves** "the three kinds catch every question the developer would overturn" if the developer
  overturns a recorded call that belongs to one of the kinds.
- **Confirms** it if every overturned call was one of taste, which D1 accepts.

## Acceptance criteria
AC2.1–AC2.3 in `feature-delta.md`.

## Dependencies
Slice 01; the spike.

## Effort estimate
≤1 day after the spike. Reference class: `phil:edd`'s step that launches a route and reads its result.

## Production data
The next Todo card on this board, carried through `nw-discuss`.

## Dogfood moment
The same day: read the card's decision comments against the transcript's asks; every ask should appear.
