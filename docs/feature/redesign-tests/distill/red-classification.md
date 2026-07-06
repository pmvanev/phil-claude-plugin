# RED Classification — redesign-tests (DISTILL)

DELIVER reads this at its PREPARE/RED phase to confirm the acceptance suite is RED **for the right
reason** — the implementation (`skills/redesign-tests/SKILL.md` + `commands/redesign-tests.md`) does
not exist yet — and not because of a test-infrastructure bug.

## Current state (2026-07-06)

The golden fixtures under `skills/redesign-tests/self-test/` are **authored and self-verified**, but
there is nothing to drive them yet: the skill and command are not written (DELIVER). This is the
correct RED — `MISSING_FUNCTIONALITY`, not `IMPORT_ERROR` / `FIXTURE_BROKEN`.

To keep the RED honest, each fixture's *mechanics* were verified in isolation during DISTILL (the
SUT + tests + patches are real and behave as pinned), so the only missing piece is the loop that
consumes them.

## Per-fixture classification

| Fixture | Baseline (verified) | Patch behaviour (verified) | Drives correctly once SKILL exists? | Classification |
|---------|---------------------|----------------------------|-------------------------------------|----------------|
| `01-baseline-red-stop` | RED (SUT bug) ✓ | n/a (no move) | loop must STOP on red | `MISSING_FUNCTIONALITY` |
| `02-postapply-red-autorevert` | GREEN ✓ | apply → RED ✓ | loop must auto-REVERT, mark blocked | `MISSING_FUNCTIONALITY` |
| `03-approve-commit-on-green` | GREEN ✓ | apply → GREEN ✓ | loop must surface claim, COMMIT on approve | `MISSING_FUNCTIONALITY` |
| `04-reject-reverts-clean` | GREEN ✓ | apply → GREEN ✓ | loop must REVERT on reject | `MISSING_FUNCTIONALITY` |
| `05-review-seeds-backlog` | GREEN (4 smell tests pass) ✓ | n/a (review mode) | loop must write `.test-redesign-backlog.md` | `MISSING_FUNCTIONALITY` |
| `06-missing-fake-skips` | GREEN ✓ | n/a (skip before apply) | loop must SKIP (missing fake) | `MISSING_FUNCTIONALITY` |

**Verification performed in DISTILL (2026-07-06):**
- Baselines run with `python -m pytest -q` (Python 3.14.3, pytest 9.0.2): 01 RED, 02/03/04/06 GREEN,
  05 all-4-GREEN — exactly as each `expected.md` requires.
- `move.patch` for 02/03/04 applied in a scratch git copy: 02 → RED, 03 → GREEN, 04 → GREEN.

## Gate for DELIVER

DELIVER's RED phase entry gate is satisfied: every fixture is RED for `MISSING_FUNCTIONALITY`
(no skill to drive them). Zero fixtures are in `IMPORT_ERROR` / `FIXTURE_BROKEN` /
`WRONG_ASSERTION`. When DELIVER writes the skill, each fixture must produce its `expected.md`
outcome; any deviation blocks the skill change.

## Deferred fixture (documented gap)

No dedicated flakiness-rewrite fixture with the N-run stability check (S4 / AC4.2) — S4 is the most
tentative slice; its go/no-go depends on real-loop data. The flaky **smell** is covered by fixture
05 (detection); the flaky **rewrite + stability** behaviour is specified in `acceptance.feature`
(`@us-S4 @flakiness`). Add the fixture when S4 is committed.
