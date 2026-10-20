# Slice 05 — The gate runner

**Goal.** The agent that runs the tests runs the run's test command and nothing else.

**Story:** US-05 · **Job:** delegate-mechanical-steps-without-handing-over-a-shell

## IN scope
- `agents/refactor-gate-runner.md` (`Read`, `Grep`, `Glob`, `Bash`).
- Hook rules: the test command exactly as given, and the read-only `git` calls the public-API check
  needs. The test command is matched as one exact string, so D3's syntax check does not apply to it.
- Name and implement the source the hook reads the test command from. Constraint: no subagent type may
  write it (D7). Candidate: the ledger header, which after slice 01 only the ledger writer can write,
  with the cage composing its content.
- Both gate calls pass `agentType`.

## OUT scope
- Sandboxing the test suite.

## Learning hypothesis
Disproves D7 **if** no source exists that the hook can read and no subagent can write. Then the slice
records the residual, and the human decides whether to accept it.

## Acceptance criteria
See US-05 in `feature-delta.md`.

## Dependencies
Slice 01; slice 03 if the public-API check reads the patch.

## Effort / reference class
≤ 1 day.

## Production data
A real run, with its baseline and post-apply gates, plus a live probe.
