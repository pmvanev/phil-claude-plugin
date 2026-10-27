# Slice 03 — Stabilize to this plugin's testing and coding standards

**Goal (one sentence):** every accepted expectation is pinned by a test meeting `rules/testing.md`,
and the built code and tests are reviewed and repaired with this plugin's own skills, serious findings
blocking done.

Story 4 · Decisions D2 (review-code and ux-review rows), D8.

## IN scope
- STABILIZE: each accepted expectation pinned by a test that `rules/testing.md` and
  `rules/test-patterns.md` accept; an accepted large or subjective output becomes an approval test
  whose approved output is the accepted evidence. The engine that built writes the tests (authoring
  may change the delegate).
- `phil:review-code` over every changed source and test file. Priority 1, and Priority 6 on a pinning
  test, block done until fixed or waived by name.
- Advisory findings offered to `phil:refactor` / `phil:refactor-loop`, `phil:refactor-tests`,
  `phil:redesign-tests`, `phil:clean-comments`; each repair under its own gate.
- `phil:ux-review` when the change touches UI; `must-fix` blocks.
- Retire the one-line citation of `coding.md`, `testing.md` and `architecture.md` that no step
  applies; each rule is named at the step that applies it.
- Fixtures: unpinned accepted expectation blocks done; approval test from accepted evidence;
  Priority 1 blocks and its waiver is recorded; UI change runs `phil:ux-review`.
- `tests/test_edd_skill.py` assertions for each skill dispatch and each block.

## OUT of scope
- Changing what `phil:review-code` or any repair skill does (D10).

## Learning hypothesis
- **Disproves** "this plugin's review catches what the engine's own standards let through" if, on
  real nwave-built work, `phil:review-code` finds nothing at Priority 1 or 6.
- **Confirms** it if the review blocks at least one run, or a pinning test fails `rules/testing.md`.

## Acceptance criteria
AC4.1–AC4.5 in `feature-delta.md`.

## Dependencies
Slices 01 and 02.

## Effort estimate
≤1 day; split the repair offers into their own slice if dispatch exceeds 6 hours.

## Production data
Code built by nwave on a real intent in this repo or a consumer repo.

## Dogfood moment
Run stabilize and review on the slice 02 dogfood output the same day.
