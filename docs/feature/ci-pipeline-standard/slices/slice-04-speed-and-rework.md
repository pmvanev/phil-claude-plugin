# Slice 04 — Speed and rework passes

**Goal.** `/phil:build-ci --speed` names the pipeline's bottleneck from measured history and stops at
the inflection point; `--rework` finds work done twice.

**Story:** US-04 · **Job:** shape-a-pipeline-to-the-change

## IN scope
- `skills/build-ci/SKILL.md`: the speed procedure (D11): measure durations and queue wait over the
  last N pipelines; find the critical path; rank candidates by saving per unit of effort; name the
  stopping point; re-measure after changes.
- The rework procedure (D12): list each artifact's producers; flag an artifact built twice.
- Always-flag rework rows already in slice 01 are cited, not repeated.

## OUT scope
- Runner fleet sizing (slice 05), except that queue wait is reported as runner-owned time.

## Learning hypothesis
Disproves "queue wait plus critical path is enough to pick the right speed-up" **if** the dogfood run's
top-ranked candidate is not on the critical path, or queue wait outweighs it and goes unreported.

## Acceptance criteria
See US-04 in `feature-delta.md`.

## Dependencies
- Slice 03.

## Effort / reference class
≤ 1 day. Reference class: `test-architecture.md`'s "Getting Back Under Budget" ladder.

## Production data
One `--speed` run over a real pipeline's recent history, recorded.
