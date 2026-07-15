# phil-edd — Acceptance Self-Test

The `phil:edd` **front-door + evidence gate** is the software under test. Its bugs are silent: an
off-ramp that quietly builds a gate, a classifier that marks provable work qualitative, a gate that
accepts narration as evidence, an evidence-producer that is secretly the builder, or a completion
reported over a rejected expectation — each looks exactly like a smooth run. These fixtures feed the
tool known situations and assert each produces the correct **decision outcome**
(`OFF-RAMP` / `CLASSIFY-CHECKABLE` / `GATE-POINT-EXISTING` / `GATE-COMMISSION` /
`REJECT-NARRATION` / `BLOCK-DONE` / `DOCUMENT-TRAIL`).

This suite is the **acceptance + regression gate** for `skills/edd/SKILL.md` (built in DELIVER). Run
it whenever the skill or the command loader changes — every such edit is non-monotonic, so the skill
is never changed and eyeballed; it is changed and regression-tested here. Format and intent mirror
`skills/work/self-test/` and `skills/refactor-tests/self-test/` — the plugin's established way to
test a skill/gate.

Unlike `phil:work` (which delegates a *change*), `phil:edd` delegates the *build* and then gates a
*qualitative expectation on executed evidence*. So most fixtures pin a front-door/gate **decision**
given a situation described in `manifest.json`, and the engine build result and the evidence-producer
result are supplied by the manifest (`engine_evidence`, `producer_result`) so the suite runs
unattended. In live use those come from the real engine (nwave / `phil:work`) and the real
non-builder producer subagent. Those have their own gates; this suite does not re-test them — it
tests the front-door and the gate around them.

## What the fixtures pin

| Fixture | Situation | Pins (AC / KPI) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-offramp-all-checkable/` | every expectation engine-provable | AC1.1, KPI zero-ceremony (**walking skeleton**) | off-ramp adds nothing (D1/DDD1) | `OFF-RAMP` — recommend the engine, exit, zero trail |
| `02-classify-bias-to-offramp/` | provability unclear / unjustified-qualitative | AC1.2, AC1.3 | bias-to-off-ramp (D1) | `CLASSIFY-CHECKABLE` — default provable; confirm before ever marking qualitative |
| `03-gate-evidence-exists/` | qualitative, engine already produced evidence | AC2.1 | scaled gate reuses existing evidence (DDD3) | `GATE-POINT-EXISTING` — point at it, no new commission, adjudicate |
| `04-gate-commission-new/` | qualitative, no evidence yet | AC2.2, AC2.4 | commission executed evidence from a **non-builder** (D2/D4/DDD4) | `GATE-COMMISSION` — fresh verbatim artifact + repro command; producer ≠ builder |
| `05-reject-narration/` | "evidence" is a description, not a run | AC2.3, KPI narration-rejection | executed-not-narrated (D2/DDD5) | `REJECT-NARRATION` — reject, re-commission a real artifact |
| `06-blocked-done/` | a qualitative expectation was rejected | AC2.5, KPI no-false-done | never report done over a rejection (D4) | `BLOCK-DONE` — not done, iterate, no false completion |
| `07-living-docs-gate-ran-only/` | loop completes with ≥1 adjudication | AC3.1, AC3.2, AC3.3, KPI zero-ceremony | trail only when the gate ran (DDD6/ADR-009) | `DOCUMENT-TRAIL` — write `docs/edd/<slug>/` + evolution; off-ramp writes none |

`01` is the single walking-skeleton scenario (the front-door end-to-end). `04`, `05`, `06` are the
safety core: the bug classes most likely to ship silently — the builder grading its own homework,
narration masquerading as proof, and a rejected expectation reported as done.

## Layout

Each fixture is self-contained:

- `manifest.json` — the situation the tool faces (intent, expectations + classification, engine,
  whether engine evidence already exists), and, where relevant, the `engine_evidence` /
  `producer_result` the driver supplies, the `builder_agent` / `producer_agent` identities (so
  separation of powers is checkable), the `human_verdict`, and the `expected_decision`.
- `expected.md` — the decision outcome the tool must produce, the guard that must produce it, and
  the gate-failure condition that blocks the skill change.
- Minimal sample artifacts for two fixtures — `03` (a real captured engine-evidence transcript to
  reuse) and `05` (a narrated non-artifact to reject). Fixtures `01`, `02`, `04`, `06`, `07` are
  manifest-driven.

## How to drive it (as the skill acceptance/regression gate)

For each fixture, drive the front-door/gate exactly as `/phil:edd` would, using `manifest.json`, and
compare against `expected.md`. Any fixture that produces the wrong outcome is a gate failure —
**block the skill change**. These are metamorphic/differential tests on the tool's **decision
behaviour**, not on the engines or the producer.

Until `skills/edd/SKILL.md` exists (DELIVER), there is nothing to drive: the suite is RED for the
right reason — the implementation is missing. See
`docs/feature/edd-loop/distill/red-classification.md`.
