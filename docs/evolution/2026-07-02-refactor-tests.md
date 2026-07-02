# Evolution — refactor-tests (`/phil:refactor-tests`)

**Finalized:** 2026-07-02 · **Branch:** `feat/refactor-tests-discuss` · **Type:** user-facing plugin feature (prose skill)
**Waves run:** DISCUSS → DESIGN → DISTILL → DELIVER (DISCOVER folded into DISCUSS; SPIKE/DEVOPS skipped — no new mechanism, no infrastructure)

## Feature summary

A new `/phil:refactor-tests` command + `skills/refactor-tests/SKILL.md` that cleans test code to
`rules/testing.md` structure standards via a **human-approved, structure-only** refactoring loop —
without silently weakening what the tests verify.

## Business context (JTBD)

`job_id: keep-test-suite-trustworthy` — persona **Tess** trusts `/phil:refactor` on production code
*because the tests catch her mistakes*; she needs that same trust when the tests themselves are what
changes. The crux: for test refactoring the test *is* the oracle, so a green suite cannot prove an
assertion was not weakened. The feature's answer is a human-in-the-loop approval gate over
assertion-preserving moves only.

## Key decisions

| ID | Decision | Where it lives |
|----|----------|----------------|
| D1 | Structure-only (assertion-preserving) moves only | SKILL scope guards |
| D2 / DD4 | Safety oracle = **human approval per diff**, reviewed in the IDE; apply→suite→pause→approve/reject/skip/quit; no chat diffs | ADR-002; SKILL human gate |
| D3 / DD1 | Ship a **new** command + skill (do not expand `phil:refactor`/`refactor-loop`) | ADR-001 |
| D4 | Separate `.test-refactoring-backlog.md` in `review-code` format by convention | SKILL review mode |
| D5 | Four moves only: Extract Fixture/Helper, Reorder into AAA, Rename, Extract Test Helper | SKILL D5 taxonomy |
| D6 | v1 acts on Python + TS/React (globs from `testing.md`; extensible) | SKILL detection |
| D7 / DD6 | Inherit `phil:refactor` safety: never on red; auto-revert on post-apply red; one commit per item | SKILL safety rules |
| DD3 | New D5 detector in the skill; `review-code` and the G2 hook left untouched | ADR-001 |
| DD5 | Automated test-diff critic **deferred to slice 04**; propose step leaves a pre-screen seam (draft recoverable at `b29f6aa`) | ADR-002 |
| DD8 | No development paradigm — prose skill + reused Bash/git | DESIGN |

## Work completed

- **DISCUSS** (`c51f67c`): persona, JTBD, 4 stories (S1–S4) with elevator pitches + ACs, D1–D7, KPIs, DoR. Bootstrapped `docs/product/{jobs.yaml,personas,journeys}`.
- **DESIGN** (`767c810`): ports-and-adapters architecture, DD1–DD8, component decomposition, reuse analysis; ADR-001 (reuse boundaries), ADR-002 (human-approval oracle); 3 carpaccio slices.
- **DISTILL** (`b476e1a`): golden-fixture acceptance suite (project convention over pytest-bdd, per DDD8) — 5 fixtures + Gherkin scenario SSOT + RED-classification. Reviewers (Sentinel + Architect) approved.
- **DELIVER** (`49d6fef`): shipped `commands/refactor-tests.md` + `skills/refactor-tests/SKILL.md`. Reviewer (crafter, prose-framed) approved after fixing AC1.3 glob coverage + prune algorithm + prereq ordering.

## Lessons learned

1. **The nWave code-oriented machinery mismatches prose-skill features.** DISTILL's pytest-bdd/RED-scaffold
   apparatus and DELIVER's DES/roadmap/crafter/mutation pipeline both assume application code. This feature
   ships Markdown executed by the model (DDD8). Both waves were adapted: DISTILL used the plugin's own
   `refactor/self-test/` golden-fixture convention; DELIVER authored prose directly and validated by
   dogfooding those fixtures. "Project conventions win" was the right call each time.
2. **Deterministic vs human-judgment validation split cleanly.** The git/suite safety mechanics
   (never-on-red, auto-revert, commit-on-green, reject-reverts) are fully scriptable and were proven 4/4 in
   throwaway git repos. The human-approval judgment and `--review` detection precision are *inherently* not
   auto-testable — the oracle is a person (D2). Naming that boundary honestly beats faking coverage.
3. **A premature artifact was correctly parked, not deleted.** The test-diff critic draft was forged early,
   reverted, and preserved in git (`b29f6aa`) for slice 04 — empirical-over-speculative (DD5).

## Issues encountered

- None blocking. Two reviewer findings in DELIVER (AC1.3 missing 2 of 10 `testing.md` globs; underspecified
  prune algorithm) were fixed in-wave and re-verified.

## Deferred / follow-ups

- **Slice 04** — automated test-diff critic as a pre-screen before the human gate (seam already in the propose
  step; draft at `b29f6aa`).
- **TS/React review fixture** — Python fixtures dogfooded; a `.test.tsx` review fixture is the documented D6 gap.
- **Live behavioral dogfood** — run `/phil:refactor-tests` against this plugin's own tests with the maintainer
  at the approval gate to confirm the `--review` precision KPI (≤20% false positives) and the S3/S4 loop.

## Permanent artifacts

- Architecture: `docs/product/architecture/brief.md`, `docs/product/architecture/adr-001-refactor-tests-reuse-boundaries.md`, `docs/product/architecture/adr-002-human-approval-via-ide-diff.md`
- Shipped code (prose): `commands/refactor-tests.md`, `skills/refactor-tests/SKILL.md`
- Acceptance suite (ships with the skill): `skills/refactor-tests/acceptance.feature`, `skills/refactor-tests/self-test/`
- Full wave record (preserved workspace): `docs/feature/refactor-tests/feature-delta.md`, `slices/`, `distill/red-classification.md`
- Product SSOT: `docs/product/jobs.yaml`, `docs/product/personas/tess-test-maintainer.yaml`, `docs/product/journeys/refactor-tests.yaml`
