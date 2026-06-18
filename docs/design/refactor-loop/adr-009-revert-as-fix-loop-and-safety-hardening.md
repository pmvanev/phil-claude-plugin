# ADR-009: Revert is a last resort behind a bounded fix-loop; safety hardening from the first run

**Status:** Accepted
**Date:** 2026-06-18
**Scope:** loop control (REVERT semantics) + cage safety invariants

## Context

The first real run (wumpus smoke test, run `wf_3138f9d2-f13`) misfired — `args` were passed
as a JSON string, not an object, so every config fell back to defaults: `REPO='.'` (it
refactored the plugin repo itself), `TEST_CMD=''` (no suite found → a vacuously-green,
**decorative** gate), `MAX_ITER=10`. It applied R001–R008 then a later `git checkout -- .`
wiped the whole working tree. The run was informative: it validated the machinery end-to-end
(G3 red-revert and G4 manifest-mismatch both fired correctly) and empirically confirmed three
predicted failures plus two new ones. This ADR records the resulting changes.

## Decision

### A. Revert is the last resort, not the first response (user directive, 2026-06-18)

A red gate after a refactor usually means the refactoring was *slightly wrong*, not
*infeasible*. So `TEST red` no longer reverts immediately. New control flow:

```
TEST red ─► FIX sub-loop (bounded by max_fix_attempts):
              diagnose the failing tests → adjust the SAME refactor → re-apply → re-TEST
                green                                   → resolve (commit-on-green)
                learned the refactor is infeasible      → REVERT + mark UNDOABLE + document
                attempts exhausted (no restabilization) → REVERT + mark UNDOABLE + document
```

- The FIX step feeds the **failing-test evidence** to the proposer and asks it to repair *this
  node's* diff (not invent a new refactoring). Bounded by `max_fix_attempts` (default 2).
- On terminal revert, the node's ledger status becomes **`undoable`** with a **findings** note
  explaining why it could not be made to pass (e.g. "extraction reorders a side effect the
  caller depends on"). Future `PROPOSE` rounds see undoable nodes and do not re-attempt them —
  the findings are durable institutional memory, not just a skip flag.
- Manifest mismatch (G4) and "the change is structurally unsafe" can short-circuit to REVERT
  without exhausting fix attempts when the proposer itself concludes the refactor is infeasible.

### B. Commit-on-green (was already queued; the run proved it essential)

Each resolved refactor is committed immediately (`git commit` per node). The run showed why:
R001–R008 went green but were *uncommitted*, and a later `git checkout` annihilated all of
them. Commit-on-green makes each green state durable, makes revert surgical, and yields a real
git audit trail (gap-memo §replit: "the confession is not an audit trail").

### C. Scoped revert, never the whole tree

REVERT acts only on the files the applied diff touched (or `git reset --hard` to the last
green commit once commit-on-green is in). It must never run `git checkout -- .` / `git checkout
-- <broad scope>`: in the run that destroyed uncommitted work, including the user's.

### D. Fail-fast configuration — the cage must not guess where to work

The orchestrator now **requires** `repo` and `test_cmd` and refuses to run without them. It
must never default `REPO` to `.` (the session cwd) — doing so silently refactored the wrong
repo. A cage that guesses its own target is not a cage.

### E. No-test baseline → HALT (decorative-gate prevention)

If the baseline gate reports zero tests collected (or no runner found), HALT. A "green" derived
from running no tests is not a valid oracle — it is precisely the decorative gate §6.2 warns
about, and the run demonstrated it (it refactored the plugin with no behavior protection).

## Consequences

- (+) Refactors that are *fixable* get fixed instead of thrown away — higher yield, closer to
  how a human refactors against a failing test.
- (+) `undoable` + findings turns dead ends into durable knowledge; the loop stops re-trying
  what provably cannot work and records why.
- (+) Commit-on-green + scoped revert eliminate the data-loss class the run exposed.
- (+) Fail-fast + no-test-HALT prevent the two ways the run misfired.
- (−) The FIX sub-loop adds a second bounded counter (`max_fix_attempts`) and more agent calls
  per hard node; capped to keep churn bounded (AHE coordination budget).
- (−) "Infeasible vs. just-needs-another-fix" is a model judgment (the proposer's) gated by a
  hard counter — the same dynamic-verdict/static-threshold split used elsewhere.

## Operational note (not a code change)

`args` must be passed to the Workflow tool as a real JSON object, never a JSON-encoded string,
or the script receives one string and every field falls back to its default. Fix D makes this
fail loudly instead of silently.

## Trace
First-run post-mortem (run `wf_3138f9d2-f13`, 2026-06-18); user directive on revert semantics
(2026-06-18); ADR-008 (substrate); gap-memo §6.2 (decorative gate), §replit-database (audit
trail); AHE (commit-per-edit, coordination budget).
