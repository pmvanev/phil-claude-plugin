# Slice 01 — Capture that covers the ground, and evidence for every expectation

**Goal (one sentence):** `/phil:edd` checks the expectations for coverage, size and risk before the
developer confirms them, then gathers executed evidence for each unless the developer opts out the
checkable ones.

Stories 1 and 2 · Decisions D1, D4, D5, D6.

## IN scope
- CAPTURE: coverage check (happy path, past edge cases, non-functional, must-not-happen), split any
  expectation of more than one breath, expand any too thin to test, order by risk; composed
  suggestions follow `rules/writing.md` and are labelled composed.
- The opt-out question after classification, asked once, for checkable expectations only; an
  expectation an approval test pins cannot be opted out.
- CLASSIFY rewritten to pick the evidence kind: checkable, qualitative, not executable in the loop.
- Evidence for checkable expectations: scenario inputs plus verbatim output from the non-builder
  producer; "all tests passed" alone is narration.
- Retire the off-ramp exit. Fixtures 01 and 02 rewritten; new fixtures for the opt-out and for
  not-executable-in-the-loop.
- The trail for every run that built (AC5.1), pulled forward from slice 04: retiring the off-ramp
  leaves an opt-out run with no other rule. Fixture 07 rewritten. The prose review stays in slice 04.
- `tests/test_edd_skill.py` assertions for the opt-out, the coverage categories and the
  `rules/writing.md` citation, each watched failing first.

## OUT of scope
- Adversarial review and challenge (slice 02); stabilize and code review (slice 03); the prose
  review of composed documents (slice 04).

## Learning hypothesis
- **Disproves** "evidence for checkable expectations is worth its cost" if, on a real intent, the
  checkable evidence shows the developer nothing the green suite had not already told them.
- **Confirms** it if at least one checkable scenario's real output surprises the developer or exposes
  a gap the suite missed.

## Acceptance criteria
AC1.1–AC1.4, AC2.1–AC2.4 in `feature-delta.md`.

## Dependencies
None beyond the shipped skill.

## Effort estimate
≤1 day. Reference class: edd-loop slice 01.

## Production data
A real intent on this repo, run without the opt-out.

## Dogfood moment
The same day, run `/phil:edd` on a real intent with at least three checkable expectations; compare
the evidence with what the suite reported.
