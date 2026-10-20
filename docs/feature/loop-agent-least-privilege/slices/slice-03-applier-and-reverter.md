# Slice 03 — The applier and the reverter

**Goal.** Applying and reverting a diff each run one `git apply` shape on one patch file.

**Story:** US-03 · **Job:** delegate-mechanical-steps-without-handing-over-a-shell

## IN scope
- `agents/refactor-applier.md` (`Read`, `Write`, `Bash`) and `agents/refactor-reverter.md` (`Bash`).
- Hook rules: the patch file's path pinned for `Read`/`Write`; `git apply --recount [--check] <patch>`
  and its `-R` twin, matched word for word; D3's syntax refused.
- On `git apply`, the hook reads the patch and refuses one touching a test path, the ledger or a loop
  file (D6).
- The workflow writes the diff through the applier, and both revert calls use the reverter type.
- Every diff scan refuses a diff touching the patch file. ADR-009 dated update (D5).

## OUT scope
- Committing; the gate.

## Learning hypothesis
Disproves D5 **if** a red gate leaves the tree so `git apply -R` cannot restore it, for example when the
test run rewrites a file the patch touched. Then the run halts, which the slice records as the cost.

## Acceptance criteria
See US-03 in `feature-delta.md`.

## Dependencies
Slice 01 (the hook).

## Effort / reference class
≤ 1 day.

## Production data
A real `/phil:refactor-loop` run that reaches at least one red gate, plus a live probe per type.
