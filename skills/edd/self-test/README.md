# phil-edd — Acceptance Self-Test

The `phil:edd` **expectation loop and its evidence gate** are the software under test. Their bugs are
silent: an opt-out that quietly skips a qualitative expectation, a classifier that marks provable work
qualitative, a gate that accepts narration — a pass count included — as evidence, an
evidence-producer that is secretly the builder, or a completion reported over a rejected expectation —
each looks exactly like a smooth run. These fixtures feed the tool known situations and assert each
produces the correct **decision outcome** (`CAPTURE-GAPS` / `CLASSIFY-CHECKABLE` / `OPT-OUT` /
`GATE-RERUN-EXISTING` / `GATE-COMMISSION` / `REJECT-NARRATION` / `SPOT-CHECK` / `REVIEW-THEN-ASK` /
`CHALLENGE` / `BLOCK-DONE` / `WAIVE-RECORDED` / `REPORT-NOT-DONE` / `PIN-APPROVAL` /
`REVIEW-CODE-GATE` / `UX-GATE` / `PROSE-REVIEWED` / `ENGINE-CANNOT-MEET` / `DOCUMENT-TRAIL`).

**No driver runs these fixtures** (issue 42). They gate a change only when a human or the model drives
them as described below. `tests/test_edd_skill.py` is what fails the build.

This suite is the **acceptance + regression suite** for `skills/edd/SKILL.md`. Run
it whenever the skill or the command loader changes — every such edit is non-monotonic, so the skill
is never changed and eyeballed; it is changed and regression-tested here. Format and intent mirror
`skills/work/self-test/` and `skills/refactor-tests/self-test/` — the plugin's established way to
test a skill/gate.

Unlike `phil:work` (which delegates a *change*), `phil:edd` delegates the *build* and then gates
*each expectation* on executed evidence. So most fixtures pin a loop/gate **decision**
given a situation described in `manifest.json`, and the engine build result and the evidence-producer
result are supplied by the manifest (`engine_evidence`, `producer_result`) so the suite runs
unattended. In live use those come from the real engine (nwave / `phil:work`) and the real
non-builder producer subagent. Those have their own gates; this suite does not re-test them — it
tests the loop and the gate around them.

## What the fixtures pin

| Fixture | Situation | Pins (AC / KPI) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-opt-out-checkable-only/` | developer trusts the tests; one expectation is qualitative | AC2.2 (edd-article-alignment), KPI no-silent-opt-out | the opt-out covers checkable expectations only (D1) | `OPT-OUT` — checkable rows trusted to tests, qualitative still evidenced, build runs, record names them |
| `02-classify-honesty-rule/` | provability unclear / unjustified-qualitative | AC1.2, AC1.3 (edd-loop) | the honesty rule (D5) | `CLASSIFY-CHECKABLE` — default checkable; confirm before ever marking qualitative |
| `03-gate-evidence-exists/` | qualitative, engine already produced evidence | AC2.1 (edd-loop) | evidence reuse (DDD3) | `GATE-RERUN-EXISTING` — the producer re-runs its reproduce command; no new scenario; adjudicate |
| `04-gate-commission-new/` | qualitative, no evidence yet | AC2.2, AC2.4 (edd-loop) | commission executed evidence from a **non-builder** (D4/DDD4) | `GATE-COMMISSION` — fresh verbatim artifact + repro command; producer ≠ builder |
| `05-reject-narration/` | "evidence" is a description, not a run | AC2.3 (edd-loop), KPI narration-rejection | executed-not-narrated (D2/DDD5) | `REJECT-NARRATION` — reject, re-commission a real artifact |
| `06-blocked-done/` | an expectation was rejected | AC2.5 (edd-loop), KPI no-false-done | never report done over a rejection (D4) | `BLOCK-DONE` — not done, iterate, no false completion |
| `07-trail-every-run-that-built/` | loop completes; contrasts an opt-out run and a capture-only stop | AC5.1 (edd-article-alignment), AC3.1, AC3.3 (edd-loop) | a trail for every run that built (D9) | `DOCUMENT-TRAIL` — trail for both runs that built; none for the capture-only stop |
| `08-checkable-scenario-evidence/` | checkable, no opt-out | AC2.1 (edd-article-alignment), KPI evidence-coverage | scenario evidence for checkable expectations (D1/D5/D6) | `GATE-COMMISSION` — inputs + verbatim output + repro, from a non-builder |
| `09-pass-count-is-narration/` | "evidence" is a test runner's pass count | AC2.3 (edd-article-alignment) | a pass count is narration (D6) | `REJECT-NARRATION` — re-commission the scenario itself |
| `10-not-executable-in-the-loop/` | a rendered animation no agent can watch | AC2.4 (edd-article-alignment) | the article's third evidence category (D5) | `SPOT-CHECK` — commission nothing; developer spot-checks or stops; record says which |
| `11-capture-coverage-size-risk/` | draft misses categories and packs two behaviours | AC1.1–AC1.4 (edd-article-alignment) | the article's capture guidance (D4) | `CAPTURE-GAPS` — gaps named, split proposed, risk-ordered, provenance labelled |
| `12-review-before-verdict/` | evidence in; reviewer raises two findings, judge confirms one | AC3.1 (edd-article-alignment) | review before any verdict, curated input, judge per finding (D7) | `REVIEW-THEN-ASK` — confirmed finding and four questions in the ask |
| `13-challenge-rebuilds-nothing/` | Avery asks for the scenario that would break it | AC3.2 (edd-article-alignment) | a challenge is not a reject (D7) | `CHALLENGE` — evidence for the named scenario; no rebuild |
| `14-unwaived-major-blocks-done/` | expectation accepted; a confirmed major stands | AC3.3 (edd-article-alignment), KPI no-standing-blocker | a confirmed major blocks done until fixed or waived by name (D2) | `BLOCK-DONE` (run a); `WAIVE-RECORDED` (run b) — waiver, reason and timestamp recorded |
| `15-stop-over-a-standing-challenge/` | Avery challenges, then stops | AC3.4 (edd-article-alignment) | stop ends the run at any round (D7) | `REPORT-NOT-DONE` — trail written with the standing challenge |
| `16-unpinned-expectation-blocks-done/` | the engine pins one of two accepted expectations | AC4.1 (edd-article-alignment), KPI pinned-expectations | every accepted expectation is pinned (D8) | `BLOCK-DONE` — unpinned goes to FINDINGS; its fix is the pin, not a rebuild |
| `17-approval-test-from-accepted-evidence/` | a qualitative expectation was accepted | AC4.2 (edd-article-alignment) | the accepted evidence becomes the approved output (D8) | `PIN-APPROVAL` — approval test, approved output verbatim |
| `18-review-code-priority-1-blocks/` | review-code writes a Priority 1, a Priority 6 on a pinning test, and two advisories | AC4.3, AC4.4 (edd-article-alignment) | serious findings block; advisories go to their owners (D2, D8) | `REVIEW-CODE-GATE` — two blockers to FINDINGS, repairs offered by owner |
| `19-ui-change-runs-ux-review/` | the change touches UI files | AC4.5 (edd-article-alignment) | `phil:ux-review` on a UI change; `must-fix` blocks (D2) | `UX-GATE` — must-fix to FINDINGS, consider advises |
| `20-record-reviewed-words-and-evidence-untouched/` | the drafted trail mixes the developer's words, composed prose, and a missing pin | AC5.2–AC5.5 (edd-article-alignment), KPI untouched-evidence | composed prose reviewed before disk; developer's words and evidence untouched (D9) | `PROSE-REVIEWED` — fixes on composed spans only; fitness blocks until rewritten |
| `21-engine-cannot-meet-an-expectation/` | the engine reports, with a benchmark, it cannot meet an expectation | protocol step 3 | the engine explains; the developer decides | `ENGINE-CANNOT-MEET` — reword, drop on the record, or stop |
| `22-challenge-tightens-a-vague-expectation/` | the developer rewords a vague expectation | protocol step 5 | a challenge may tighten; old evidence lapses | `CHALLENGE` — reclassified, fresh evidence, no rebuild |

`04`, `05`, `06`, `09`, `12`, `14` are the safety core: the bug classes most likely to ship silently —
the builder grading its own homework, narration masquerading as proof, a green suite standing in for
evidence, a rejected expectation reported as done, the builder's reasoning reaching the reviewer, and
a confirmed defect waved through.

## Layout

Each fixture is self-contained:

- `manifest.json` — the situation the tool faces (intent, expectations + classification, engine,
  whether engine evidence already exists, the developer's opt-out answer), and, where relevant, the `engine_evidence` /
  `producer_result` the driver supplies, the `builder_agent` / `producer_agent` identities (so
  separation of powers is checkable), the `human_verdict`, and the `expected_decision`.
- `expected.md` — the decision outcome the tool must produce, the guard that must produce it, and
  the gate-failure condition that blocks the skill change.
- Minimal sample artifacts for two fixtures — `03` (a real captured engine-evidence transcript to
  reuse) and `05` (a narrated non-artifact to reject). The rest are manifest-driven.

## How to drive it (as the skill acceptance/regression gate)

For each fixture, drive the loop/gate exactly as `/phil:edd` would, using `manifest.json`, and
compare against `expected.md`. Any fixture that produces the wrong outcome is a gate failure —
**block the skill change**. These are metamorphic/differential tests on the tool's **decision
behaviour**, not on the engines or the producer.
