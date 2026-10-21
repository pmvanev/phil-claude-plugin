# Slice 02 — Declared policy and the trigger matrix

**Goal.** `/phil:review-ci` checks a pipeline against the project's declared policy and shows which
pipeline sources start each job.

**Story:** US-02 · **Job:** shape-a-pipeline-to-the-change

## IN scope
- `rules/ci-pipelines.md`: the policy block and its fields (D6); the default policy (D7); the
  skip-needs-a-gate rows (D8); the docs allow-list row (D9); Principles and Advisory halves.
- `skills/review-ci/SKILL.md`: reads the policy block, writes the jobs-by-sources matrix (D10), and marks
  each departure.
- Self-test fixture `02-trigger-matrix/`: a schedule that would deploy, a rule on an empty variable, a
  `needs:` on a path-skipped job, a docs deny-list — beside a correct guard for each.
- One pointer line in `test-architecture.md` (D11 ownership).

## OUT scope
- Writing the policy block or changing a pipeline (slice 03).

## Learning hypothesis
Disproves "a matrix read from the rules, not computed, catches the jobs that run when nobody expects
them" **if** the fixture run misses any of the four seeded cells, or marks a correct guard.

## Acceptance criteria
See US-02 in `feature-delta.md`.

## Dependencies
- Slice 01.

## Effort / reference class
≤ 1 day. Reference class: `security-standards-rule` slice 02 (principles and advisory).

## Production data
A dogfood run over `beatrix/.gitlab-ci.yml`, whose policy the user typed on 2026-10-21.
