# RED classification — phil-work acceptance self-test

Per the DISTILL pre-DELIVER "fail-for-the-right-reason" gate.

**Status: RED for the right reason — implementation missing.**

The acceptance scenarios (`skills/work/acceptance.feature`) and the golden fixtures
(`skills/work/self-test/`) exist, but the software under test — `commands/work.md` +
`skills/work/SKILL.md` — is **not yet built** (that is DELIVER's job). There is therefore nothing
to drive the fixtures against yet. This is genuine RED (missing functionality), not BROKEN
(setup/import/infrastructure error).

| Fixture | Failure mode until DELIVER | Classification |
|---|---|---|
| 01-frame-refuses-vague-goal | no orchestrator to make the FRAME decision | `MISSING_FUNCTIONALITY` ✅ |
| 02-frame-offramp-trivial | no orchestrator to off-ramp | `MISSING_FUNCTIONALITY` ✅ |
| 03-walking-skeleton-end-to-end | no orchestrator to frame→delegate→document | `MISSING_FUNCTIONALITY` ✅ |
| 04-route-code-to-loop | no router to delegate to refactor-loop | `MISSING_FUNCTIONALITY` ✅ |
| 05-route-prose-to-approval | no router to delegate to refactor-tests/redesign-tests | `MISSING_FUNCTIONALITY` ✅ |
| 06-delegate-failure-leaves-last-good | no sequencing gate to stop/leave-last-good | `MISSING_FUNCTIONALITY` ✅ |
| 07-verify-reports-goal-not-met | no VERIFY step to report goal honesty | `MISSING_FUNCTIONALITY` ✅ |

No fixture is BROKEN (no import/fixture/setup failure): each is a self-contained situation whose
expected decision is documented in its `expected.md`. The target files in fixtures 04/05 are
runnable stand-ins; fixtures 01/02/03/06/07 are manifest-driven decision fixtures, matching the
plugin's established `refactor/self-test/` and `refactor-tests/self-test/` style.

DELIVER reads this file at its RED-phase entry to confirm RED is genuine before writing
`skills/work/SKILL.md`.
