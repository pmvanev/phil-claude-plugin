# RED classification — refactor-tests (DISTILL fail-for-the-right-reason gate)

DISTILL's pre-DELIVER gate requires every acceptance test to fail because the **implementation
is missing**, not because the test infrastructure is broken. This feature ships a prose skill,
not application code, so the gate is adapted: the acceptance suite is the golden-fixture set
under `skills/refactor-tests/self-test/`, driven by `/phil:refactor-tests` (which does not yet
exist).

## Classification

| Scenario / fixture | Fails because | Classification |
|---|---|---|
| 01-baseline-red-stop | no `SKILL.md` / command to drive the loop | `MISSING_FUNCTIONALITY` ✅ RED |
| 02-postapply-red-autorevert | no loop to apply the move + auto-revert | `MISSING_FUNCTIONALITY` ✅ RED |
| 03-approve-commit-on-green (walking skeleton) | no loop to propose → apply → gate → commit | `MISSING_FUNCTIONALITY` ✅ RED |
| 04-reject-reverts-clean | no human-approval gate to honour a reject | `MISSING_FUNCTIONALITY` ✅ RED |
| 05-review-seeds-backlog | no D5 detector to write the backlog | `MISSING_FUNCTIONALITY` ✅ RED |

**No fixture is BROKEN.** Verified independently of the (absent) implementation:

- Every fixture's baseline runs under `python -m pytest` with **no import error, no fixture
  bug, no setup failure**:
  - `01` baseline is **red by design** (buggy SUT) — the precondition the loop must detect.
  - `02`, `03`, `04`, `05` baselines are **green**.
- Every `move.patch` **applies cleanly** (`git apply --check` passes for 02, 03, 04).
- Post-apply states are the ones the guards key on: `02` → red (revert trigger), `03` → green
  (commit-eligible). Confirmed by running pytest on applied copies.

The only reason the suite cannot be *driven* is that `skills/refactor-tests/SKILL.md` and
`commands/refactor-tests.md` are not written yet. That is correct RED.

## DELIVER entry condition

DELIVER reads this file at its RED-phase entry (ADR-025 D2). When each slice lands, driving the
corresponding fixture(s) must flip them from "nothing to drive" to the `expected.md` outcome:

- slice 01 → fixtures 01, 02, 03, 04 (the walking-skeleton safety loop)
- slice 02 → fixture 05 (the `--review` detector)
- slice 03 → the `@loop` / `@requires-human` scenarios in `acceptance.feature` (backlog loop)
