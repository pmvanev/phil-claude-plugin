# ADR-001 — refactor-tests: new command + reuse boundaries

Status: accepted (DESIGN wave, 2026-07-01) · Feature: refactor-tests

## Context

`testing.md` structure smells accumulate, but neither `phil:refactor` (auto pass/fail oracle,
"preserve behavior absolutely") nor `phil:refactor-loop` (G2 hook + rubric hard-block test
writes) can safely refactor tests. DISCUSS decided a new command, structure-only scope, and a
human-approval oracle (D1–D3). The plugin already has overlapping machinery: `review-code`
writes a prioritized backlog, `phil:refactor` runs a backlog-driven apply→verify→commit loop,
and `test-runner-detection.md` locates the suite.

## Decision

Ship a **new** `commands/refactor-tests.md` + `skills/refactor-tests/SKILL.md` (command→skill
split, matching the plugin). Reuse boundaries:

- **REUSE as-is:** `skills/shared/test-runner-detection.md`.
- **EXTEND (pattern):** copy `phil:refactor`'s loop shape; swap the gate for human approval and
  the move set for structure-only test moves.
- **CREATE NEW:** the D5 test-smell detector, living in the skill. It writes
  `.test-refactoring-backlog.md` in `review-code`'s backlog **format, by convention** — no
  shared code module. `review-code` is left UNCHANGED.

## Alternatives considered

- **Add `--tests` to `review-code`** — rejected: overloads one command with two taxonomies and
  two backlog targets, the same overloading DISCUSS-D3 rejected for the refactor commands.
- **Extract a shared backlog-writer module** — rejected for v1: best DRY, but refactors a
  working command for a format unlikely to churn. Revisit if the two writers drift.

## Consequences

- (+) `review-code` untouched; no regression risk to a working command.
- (+) New command is auto-discovered; no manifest change.
- (−) Two places write the backlog format; if it changes, both update. Accepted; low churn.
