# Slice 01 — Show the path

**Goal (one sentence):** `/phil:autopilot <card>` claims the card through `/phil:start`, reads the
repo's build path from its prose, prints each step beside its source line with the writes the path
authorizes, records both on the card, and stops before the first step.

Story 1 · Decisions D2, D4, D5, D11.

## IN scope
- `commands/autopilot.md` (`mutates: true`) and `skills/autopilot/SKILL.md`.
- Claiming through `/phil:start`; a card underway resumes at its next step (D5).
- Reading the path from `CLAUDE.md` and `AGENTS.md`; the fallback by `/phil:start`'s route rules 2–3,
  named when taken.
- The PATH and AUTHORIZED lines, and one card comment holding both; the skill names `rules/writing.md`.
- On GitLab: say the command covers GitHub only and stop with a named outcome (D10).
- Fixtures: a declared path beside nWave directories (AC1.1); no declared path (AC1.2); a missing
  `rules/writing.md` citation fails a test (AC2.4).

## OUT of scope
- Running any step (slice 02).

## Learning hypothesis
- **Disproves** "a build path can be read reliably from prose" if, on the five local repos with a
  `CLAUDE.md`, the printed path disagrees with the developer's reading of any of them.
- **Confirms** it if the developer accepts all five readings unchanged.

## Acceptance criteria
AC1.1–AC1.4 and AC2.4 in `feature-delta.md`.

## Dependencies
None; `/phil:start` has shipped.

## Effort estimate
≤1 day. Reference class: `start-work` slice 01, a read-only report ending in a route.

## Production data
This repo's `CLAUDE.md`, and those of harebrain, modive, beatrix and submission-tracker.

## Dogfood moment
The same day, run it on issue 76 here and check the printed path against "Build path for this plugin".
