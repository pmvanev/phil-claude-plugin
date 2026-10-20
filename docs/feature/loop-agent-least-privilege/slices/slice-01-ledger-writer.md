# Slice 01 — The ledger writer, and the hook it proves

**Goal.** The agent that records a run writes the ledger and nothing else, enforced by a plugin hook
keyed on its agent type.

**Story:** US-01 · **Job:** delegate-mechanical-steps-without-handing-over-a-shell

## IN scope
- `agents/refactor-ledger-writer.md`: `tools: Read, Write`.
- One new hook script under `hooks/refactor-loop/`, registered in `hooks/hooks.json` on
  `Bash|Read|Write|Edit`: silent unless `agent_type` is a narrowed loop type; for the ledger writer,
  `Read` and `Write` only on the ledger path, everything else refused.
- A `Write` or `Edit` to the ledger from any other subagent type is refused (D8).
- Both ledger calls in `workflows/refactor-loop.js` pass `agentType`.

## OUT scope
- The other four roles.

## Learning hypothesis
Disproves D1 for plugin agents **if** a plugin agent's tool calls reach the hook without an
`agent_type`, or with one the hook cannot match. Confirms the mechanism the other slices extend if the
live probe is refused.

## Acceptance criteria
See US-01 in `feature-delta.md`.

## Dependencies
None.

## Effort / reference class
≤ 1 day. Reference: G2's hook and tests (`block-test-file-write.py`).

## Production data
This repository: a live `/phil:refactor-loop` run on a real scope, and a probe from a fresh
`claude -p` process in bypass mode.
