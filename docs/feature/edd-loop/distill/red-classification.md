# RED classification — edd-loop (pre-DELIVER fail-for-the-right-reason)

The acceptance suite (`skills/edd/acceptance.feature` + `skills/edd/self-test/`) is authored, but
`skills/edd/SKILL.md` and `agents/edd-evidence-producer.md` do **not** exist yet — they are built in
DELIVER. So there is nothing to drive the fixtures against.

**Classification: RED for the right reason — implementation missing.**

This is a prose-artifact feature, so "RED" is not a pytest collector result (there is no runner in
this plugin — see `skills/work/self-test/README.md`). It means: every fixture describes a decision
the front-door/gate must make, and none can be produced because the skill under test is not written.
There are **no** BROKEN-class problems (no import errors, no fixture bugs) — the fixtures are plain
`manifest.json` + `expected.md` + two sample artifacts, all self-contained and readable now.

| Fixture | Would-be outcome | Why RED (not BROKEN) |
|---|---|---|
| 01-offramp-all-checkable | `OFF-RAMP` | no SKILL.md to make the off-ramp decision |
| 02-classify-bias-to-offramp | `CLASSIFY-CHECKABLE` | no classifier to apply bias-to-off-ramp |
| 03-gate-evidence-exists | `GATE-POINT-EXISTING` | no gate to reuse existing evidence |
| 04-gate-commission-new | `GATE-COMMISSION` | no gate + no `edd-evidence-producer` agent |
| 05-reject-narration | `REJECT-NARRATION` | no gate to judge executed-vs-narrated |
| 06-blocked-done | `BLOCK-DONE` | no adjudication/done logic |
| 07-living-docs-gate-ran-only | `DOCUMENT-TRAIL` | no DOCUMENT step to write/withhold the trail |

**DELIVER entry gate:** each slice's step is GREEN when its fixture(s) reach the expected decision by
driving `skills/edd/SKILL.md` (built that slice), and the human-approval oracle passes for the
judgment scenarios — exactly the phil-work model (`roadmap.json` step criteria = "Fixture NN reaches
<STATE>"). No RED→GREEN production-code cycle; this is prose authoring gated by fixtures (DDD8).
