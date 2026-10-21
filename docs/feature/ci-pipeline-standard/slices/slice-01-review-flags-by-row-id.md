# Slice 01 — Review flags pipeline defects by row id

**Goal.** `/phil:review-ci` names each objective pipeline defect by its `PIPE-n` row and fix, and
leaves the documented false alarms alone. *(Walking-skeleton slice.)*

**Story:** US-01 · **Job:** shape-a-pipeline-to-the-change

## IN scope
- `rules/ci-pipelines.md`: frontmatter, sources line, ownership paragraph, Always-flag rows from
  research P1–P21 renumbered `PIPE-n`, each with its Zampetti id, Do-not-flag list, dated editions line.
- `skills/review-ci/SKILL.md` and `commands/review-ci.md`: read the rule, gather CI files, write
  `.ci-review.md`.
- Self-test fixture `01-pipeline-findings-cite-a-row/`: eight or more seeded defects, five or more
  look-alikes; a test pinning every `PIPE-n` id and each expected item's id and fix.
- One pointer line each in `continuous-delivery.md` and `security.md`. README; version bump.

## OUT scope
- Policy block, Principles, Advisory and the trigger matrix (slice 02).
- `/phil:build-ci` (slices 03 and 04); runners (slice 05).

## Learning hypothesis
Disproves "Zampetti-cited rows, renumbered as the rule's own, are precise enough that a reviewer flags
the seeded defects and no look-alike" **if** the fixture run misses a defect, names the wrong row, or
files a look-alike.

## Acceptance criteria
See US-01 in `feature-delta.md`.

## Dependencies
- V1: every cited Zampetti id checked against the paper's tables.

## Effort / reference class
≤ 1 day. Reference class: `security-standards-rule` slice 01.

## Production data
A dogfood run over `modive/.gitlab-ci.yml` (889 lines), recorded in `feature-delta.md`.
