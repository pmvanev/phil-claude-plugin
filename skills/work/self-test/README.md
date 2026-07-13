# phil-work — Acceptance Self-Test

The `phil:work` **orchestrator** is the software under test. Its bugs are silent: a sequencing
gate that fails to stop on a delegate failure, a router that sends prose to a code loop, or a
VERIFY that calls a missed goal "done" — each looks exactly like a smooth run. These fixtures
feed the orchestrator known situations and assert each produces the correct **decision outcome**
(`REFUSE` / `OFF-RAMP` / `DELEGATE` / `STOP-LAST-GOOD` / `REPORT-NOT-DONE`).

This suite is the **acceptance + regression gate** for `skills/work/SKILL.md` (built in DELIVER).
Run it whenever the skill or the command loader changes — every such edit is non-monotonic, so the
skill is never changed and eyeballed; it is changed and regression-tested here. Format and intent
mirror `skills/refactor-tests/self-test/` and `refactor/self-test/` — the plugin's established way
to test a skill/gate.

Unlike `refactor-tests` (which transforms code), `phil:work` **delegates** execution. So most
fixtures pin an orchestrator **decision** given a situation described in `manifest.json`, and the
delegate's own result is supplied by the manifest (`delegate_result`) so the suite runs unattended.
In live use that result comes from the real delegate (`refactor-loop`'s suite gate, or
`refactor-tests`/`redesign-tests`' human gate). The delegates have their own self-tests; this suite
does not re-test them — it tests the contractor around them.

## What the fixtures pin

| Fixture | Situation | Pins (AC / slice) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-frame-refuses-vague-goal/` | goal is uncheckable | slice-01/04 FRAME, DDD9 | goal must be checkable or preservation-only (D4) | `REFUSE` — no change until a checkable goal or preservation-only is agreed |
| `02-frame-offramp-trivial/` | one skill would suffice | slice-01, D7/DDD8 | off-ramp trivial work (anxiety B) | `OFF-RAMP` — recommend the single skill, exit, no trail opened |
| `03-walking-skeleton-end-to-end/` | real initiative, one delegate, oracle passes | slice-01 (**walking skeleton**) | frame→delegate→preserve→document e2e | `DELEGATE` + decision record + summary; oracle still passes |
| `04-route-code-to-loop/` | wave changes executable code | slice-05, DDD3/DDD4 | route code → refactor-loop (suite oracle) | `DELEGATE` to the code loop; no own gate |
| `05-route-prose-to-approval/` | wave changes a skill/rule/agent | slice-05, DDD3/DDD4/D9 | route prose → refactor-tests/redesign-tests (human oracle) | `DELEGATE` to the approval cleaner; no own gate |
| `06-delegate-failure-leaves-last-good/` | a delegate fails mid-sequence | slice-02, DDD4 sequencing gate | stop-and-leave-last-good; never red; not done | `STOP-LAST-GOOD` — sequence halts, tree last-good, run not done |
| `07-verify-reports-goal-not-met/` | behaviour preserved, goal missed | slice-04, VERIFY honesty | never fake done (habit/anxiety) | `REPORT-NOT-DONE` — goal not achieved, with metric evidence |

`03` is the single walking-skeleton scenario. `06` is the safety core: the one bug class most
likely to ship silently (a run that broke something reported as a clean success).

## Layout

Each fixture is self-contained:

- `manifest.json` — the situation the orchestrator faces (initiative, goal, artifact kind), and,
  where relevant, the `delegate_result` the driver should supply and the `expected_guard`.
- `expected.md` — the decision outcome the orchestrator must produce, and the guard that must
  produce it, plus the gate-failure condition that blocks the skill change.
- Minimal target files for the two routing fixtures — `04` (a tiny code module + test) and `05`
  (a tiny prose skill file) — so the router has a concrete artifact to classify. Fixtures `01`,
  `02`, `03`, `06`, `07` are manifest-driven (the situation and any delegate result live in
  `manifest.json`).

## How to drive it (as the skill acceptance/regression gate)

For each fixture, drive the orchestrator exactly as `/phil:work` would, using `manifest.json`,
and compare against `expected.md`. Any fixture that produces the wrong outcome is a gate failure —
**block the skill change**. These are metamorphic/differential tests on the orchestrator's
**decision behaviour**, not on the delegates.

Until `skills/work/SKILL.md` exists (DELIVER), there is nothing to drive: the suite is RED for the
right reason — the implementation is missing. See
`docs/feature/phil-work/distill/red-classification.md`.
