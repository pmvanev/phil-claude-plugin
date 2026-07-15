# DISTILL Decisions — adversarial-review

## Reconciliation
- Read DISCUSS + DESIGN wave-decisions. **PASS — 0 contradictions.** DESIGN's one change (slice 03
  dropped → composition doc-only) was back-propagated in `design/upstream-changes.md`; nothing
  contradicts DISCUSS. DEVOPS/SPIKE not run (WARN, proceeded with defaults).

## Key Decisions
- [DT1] Prose-shaped acceptance: `acceptance.feature` (scenario SSOT) + author-then-ablate `self-test/`
  golden fixtures, driven by a human/model (no pytest collector) — mirrors edd/work/refactor-tests.
- [DT2] Typed verdict schema locked (feature-delta § DISTILL): `justification` first;
  `overall_label ∈ {sound-gate, draft-signal}` (mechanical, C4); `verdict ∈ {findings, clean,
  cannot-assess}` (no done/not-done field, C3); per-finding `kind ∈ {hard, soft}` (C2); every finding
  has span+evidence, ranked worst-first (C5 / anxiety B).
- [DT3] 7 fixtures pin WS + C1–C5 + honest reporting. Safety core = 03 (never sound-gate w/o oracle),
  04 (independent dispatch), 06 (advisory never self-adjudicate) — the silent theatre bug classes.
- [DT4] Register-outcomes SKIPPED (methodology/prose feature; no outcomes registry — D-6 scoping),
  consistent with DESIGN's Outcome Collision Check skip.

## Scenario / fixture inventory
01 draft-signal-no-oracle (WS) · 02 sound-gate-with-oracle · 03 never-sound-gate-without-oracle ·
04 independent-dispatch · 05 cannot-assess-empty-praise · 06 advisory-never-self-adjudicate ·
07 clean-pass-no-manufactured-findings.

## Test placement
`skills/adversarial-review/` (acceptance.feature + self-test/) — the skill IS the SUT; not `tests/`.

## RED status
All 7 RED for the right reason (implementation missing). See `distill/red-classification.md`.

## Step-reuse ratio (Mandate-12, informational)
N/A — prose fixtures, not pytest-bdd step decorators. The shared vocabulary is the decision-outcome
set (DRAFT-SIGNAL / SOUND-GATE / NEVER-SOUND-GATE / INDEPENDENT-DISPATCH / CANNOT-ASSESS /
ADVISORY-ONLY / CLEAN-PASS) reused across fixtures + acceptance.feature.

## Handoff
- To: DELIVER. Build `commands/adversarial-review.md`, `skills/adversarial-review/SKILL.md`,
  `agents/adversarial-reviewer.md` (pattern-copy `refactor-critic-correctness`) to turn all 7
  fixtures GREEN. Slices 01 (WS) then 02 (hard half + composition-contract doc).
