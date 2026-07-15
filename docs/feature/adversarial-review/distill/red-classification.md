# RED classification — adversarial-review DISTILL

The acceptance suite (`skills/adversarial-review/acceptance.feature` + `self-test/` fixtures 01–07)
is authored ahead of the implementation. Per the pre-DELIVER fail-for-the-right-reason gate:

| Scenario / fixture | Failure mode | Classification |
|---|---|---|
| 01 draft-signal-no-oracle (WS) | `skills/adversarial-review/SKILL.md` + `agents/adversarial-reviewer.md` do not exist yet | `MISSING_FUNCTIONALITY` ✅ correct RED |
| 02 sound-gate-with-oracle | same — no reviewer/skill to dispatch | `MISSING_FUNCTIONALITY` ✅ |
| 03 never-sound-gate-without-oracle | same | `MISSING_FUNCTIONALITY` ✅ |
| 04 independent-dispatch | same — no dispatch curation logic yet | `MISSING_FUNCTIONALITY` ✅ |
| 05 cannot-assess-empty-praise | same | `MISSING_FUNCTIONALITY` ✅ |
| 06 advisory-never-self-adjudicate | same | `MISSING_FUNCTIONALITY` ✅ |
| 07 clean-pass-no-manufactured-findings | same | `MISSING_FUNCTIONALITY` ✅ |
| 08 clean-sound-gate-green-oracle | same | `MISSING_FUNCTIONALITY` ✅ |

Fixtures 01–08 are RED for the right reason — the implementation is missing, not a fixture/setup bug.
There is no `IMPORT_ERROR` / `FIXTURE_BROKEN` / `WRONG_ASSERTION` class here because the suite is
prose-driven (a human or the model drives each fixture against `expected.md`), exactly as
`skills/edd/self-test/` and `skills/work/self-test/` are. DELIVER reads this file at PREPARE to
confirm RED is genuine before building the skill/agent.

## Slice 03 addendum (fixtures 09–10, the judge)

Fixtures 09 (judge refutes a false positive) and 10 (judge confirms a real finding) were authored in
slice 03 alongside `agents/adversarial-verifier.md`. Their pre-implementation state was
`MISSING_FUNCTIONALITY` (no verifier agent + no VERIFY step to dispatch) — same correct RED as
01–08 — and both were driven GREEN in the same slice (09 dogfood-verified: the judge refuted a stale
finding against the real, fixed agent file, conf 0.97; 10 fixture-verified). All 10 now green.
