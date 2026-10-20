# Slice 02 — The security rule's narrow-grant row

**Goal.** `review-code` stops calling a command pattern in an agent's `tools:` line a narrow grant.

**Story:** US-02 · **Job:** delegate-mechanical-steps-without-handing-over-a-shell

## IN scope
- `rules/security.md`, the CWE-250 agent row: the measured behaviour and the enforced form (D9).
- A `review-code` self-test fixture: an agent file granting `Bash(git log:*)`, expecting the finding.
- Version bump.

## OUT scope
- Probing command `allowed-tools`; the row says that case is unmeasured.

## Learning hypothesis
Disproves "one row can carry the correction" **if** the fixture still passes with the old row, or the
corrected row makes the reviewer flag the read-only agents of `ab5bf22`, which hold no shell.

## Acceptance criteria
See US-02 in `feature-delta.md`.

## Dependencies
Slice 01, so the enforced form the row names exists.

## Effort / reference class
≤ half a day. Reference: the security-standards-rule refinements 1.2.1–1.2.3.

## Production data
This repository's `agents/` directory.
