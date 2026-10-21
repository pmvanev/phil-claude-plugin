# Slice 05 — Runner rule and review of runner config

**Goal.** `/phil:review-ci` judges runner configuration by the isolation, wait and cost each setting
buys, and the rule holds answers about a fleet to what is live.

**Story:** US-05 · **Job:** run-a-runner-fleet-knowingly

## IN scope
- `rules/ci-runners.md`: Principles (SLSA isolated builds, one trust class per machine, setup-time
  queueing); Always-flag RUN-1 to RUN-13; fleet-answer rows RUN-T1 and RUN-T2 (D16); Advisory, including
  VM reuse; Do not flag.
- `skills/review-ci/SKILL.md`: gathers runner config (`config.toml*`, runner Terraform) and applies the rule.
- Self-test fixture `03-runner-config/`.

## OUT scope
- Changing a fleet. `/phil:build-ci` does not touch runners.

## Learning hypothesis
Disproves "runner settings can be judged from config without the live system" **if** the dogfood
finding on `scale_factor` or VM reuse needs live state to be right.

## Acceptance criteria
See US-05 in `feature-delta.md`.

## Dependencies
- V2 (CWE ids) and V3 (taskscaler at the pinned revision).

## Effort / reference class
≤ 1 day. Reference class: `security-standards-rule` slice 03 (agent and hook rows).

## Production data
A dogfood run over `runbooks/runners/`.
