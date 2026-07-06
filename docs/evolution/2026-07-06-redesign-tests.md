# Evolution — redesign-tests (`/phil:redesign-tests`)

**Finalized:** 2026-07-06 · **Branch:** `feat/redesign-tests-discuss` · **Type:** user-facing plugin feature (prose skill)
**Waves run:** DISCUSS → DESIGN → DISTILL → DELIVER (DISCOVER folded into DISCUSS; SPIKE/DEVOPS skipped — no new mechanism, no infrastructure)

## Feature summary

A new `/phil:redesign-tests` command + `skills/redesign-tests/SKILL.md` — the behaviour-CHANGING
sibling of `refactor-tests`. It rewrites tests that verify **how** the code works into tests that
verify **what** it does (implementation-coupling → excessive-mocking → flakiness), one
human-approved diff at a time. Where `refactor-tests` is assertion-preserving and can promise
coverage never shrank, `redesign-tests` deliberately changes what a test asserts — so the human is
the **sole oracle**, and every proposal carries a **coverage-equivalence claim** the human validates.

## Business context (JTBD)

Same validated job as `refactor-tests` — `keep-test-suite-trustworthy`, persona **Tess** — but the
opposite pole. `refactor-tests` cleans structure without changing what is verified; `redesign-tests`
fixes tests that verify the *wrong thing*. The job's four-forces were back-propagated: the "pull"
extended to "safely fix tests that verify the wrong thing, one approved diff at a time," and anxiety
(C) reframed for this feature to "a sanctioned rewrite could still silently narrow coverage" — the
accepted v1 risk.

## Key decisions

| ID | Decision | Where it lives |
|----|----------|----------------|
| D1 | Scope = all behaviour-changing smells (coupling, over-mocking, flakiness) | SKILL scope table |
| D2 | Oracle = human-only (per-diff approval); no automated oracle in v1 | ADR-004; SKILL human gate |
| D3 | Human approves **every** rewrite — green suite never auto-applies | ADR-004 |
| D4 | Same job (`keep-test-suite-trustworthy`), new feature | jobs.yaml |
| D5 | Reuse the `refactor-tests` loop shape (pattern-copy) | DDD1; ADR-003 |
| D6 | Separate `.test-redesign-backlog.md` (no collision with refactor-tests) | ADR-003; SKILL review mode |
| D7 | Accepted risk: human-only oracle cannot guarantee coverage preserved; automated oracle deferred | ADR-004; feature-delta |
| DDD1 (DESIGN) | **Option A** — new command + skill; not a `--behavioral` mode, not shared extraction | ADR-003 |
| DDD3 | Human gate carries a **coverage-equivalence claim** (before/after "what it caught then / catches now") | ADR-004 |
| DDD4 | Behavioural rewrite catalog by smell family (Assert-on-observable-outcome; Replace-mock-with-real/fake; Inject-clock/Seed-RNG/Isolate-state) | SKILL |
| DDD7 | Pre-screen seam reserved for a future automated coverage oracle | ADR-004; SKILL propose step |

## Work completed

- **DISCUSS** (`a4671c6`): persona reuse, JTBD refinement, 4 stories (S1–S4) with elevator pitches +
  ACs, D1–D7, KPIs (K1–K4), DoD, carpaccio slices; SSOT back-propagation (jobs.yaml four-forces,
  new journey yaml).
- **DESIGN** (`044773d`): Option A packaging, ADR-003 (reuse boundaries) + ADR-004 (coverage-
  equivalence claim), component decomposition, Reuse Analysis (zero unjustified CREATE NEW), C4
  System Context + Container diagrams, brief.md SSOT section.
- **DISTILL** (`e1340d2`, review `cd95a3d`): `acceptance.feature` scenario SSOT + 6 golden self-test
  fixtures pinning the safety loop; all self-verified with pytest 9.0.2. Consolidated review
  (Eclipse/Architect/Sentinel) — zero blockers; Sentinel's findings resolved in-wave.
- **DELIVER** (`e6f361a`): shipped `commands/redesign-tests.md` + `skills/redesign-tests/SKILL.md`;
  drove all 6 fixtures through the loop — **27/27 assertions pass** (01→STOP, 02→REVERT, 03→COMMIT
  with claim surfaced, 04→REVERT-on-reject, 05→exactly-4-items/SUT-clean, 06→SKIP).

## Lessons learned

1. **The prose-skill mismatch recurs, and the same adaptation works.** As with `refactor-tests`,
   DISTILL's pytest-bdd/scaffold apparatus and DELIVER's roadmap/crafter pipeline assume application
   code. Both waves were adapted: DISTILL used the plugin's golden-fixture convention; DELIVER
   authored prose directly and validated by dogfooding the fixtures. "Project conventions win."
2. **Behaviour-changing test work needs an oracle beyond green.** The whole feature turns on one
   idea (ADR-004): a green suite cannot prove a behavioural rewrite preserved coverage, so the human
   validates an explicit coverage-equivalence claim. This is the net-new element vs. `refactor-tests`
   and the load-bearing risk mitigation for the human-only oracle.
3. **The "same job, opposite pole" framing kept the SSOT honest.** Registering under the existing job
   forced a back-propagation of its four-forces (anxiety C had *forbidden* unsanctioned behaviour
   change; this feature *sanctions* it). Quoting the original verbatim and noting provenance beat
   silently overwriting.
4. **Harness bugs are not fixture bugs.** The DELIVER drive first "failed" 10/27 — all three causes
   were test-harness artifacts (pycache polluting `git status`, an MSYS path handed to Windows
   Python, an over-broad grep), none a real defect. Fixing the harness gave 27/27. Worth
   distinguishing before touching the artifacts.

## Deferred / follow-ups

- **Automated coverage oracle** — mutation testing (mutmut/Stryker) or deliberate-break-and-confirm,
  slotted at the reserved pre-screen seam. Build once v1 produces real human-review-burden and
  coverage-loss data (empirical over speculative, mirroring `refactor-tests`' deferred critic).
- **S4 flakiness spin-off** — if the N-run stability oracle proves a poor fit for the coverage-
  oriented loop, extract flakiness into its own skill. Its dedicated rewrite fixture is deferred with
  this go/no-go.
- **TS/React self-test fixture** — Python fixtures dogfooded; a `.test.tsx` fixture is the documented
  language gap (same gap `refactor-tests` carries).
- **Shared gated-approval-loop extraction** — with two consumers now (`refactor-tests` +
  `redesign-tests`), ADR-001's deferred shared-module extraction is triggered; revisit by extracting
  from two known-good copies.

## Issues encountered

- None blocking. The consolidated review returned zero blockers; Sentinel's 2 moderate + 2 low
  findings were resolved or accepted in-wave (`cd95a3d`).

## Permanent artifacts

- Architecture: `docs/product/architecture/brief.md` (redesign-tests section),
  `adr-003-redesign-tests-reuse-boundaries.md`, `adr-004-redesign-tests-coverage-equivalence-claim.md`
- Shipped code (prose): `commands/redesign-tests.md`, `skills/redesign-tests/SKILL.md`
- Acceptance suite (ships with the skill): `skills/redesign-tests/acceptance.feature`,
  `skills/redesign-tests/self-test/` (6 fixtures)
- Feature record: `docs/feature/redesign-tests/feature-delta.md`, `slices/`, `distill/red-classification.md`
- Product SSOT: `docs/product/jobs.yaml` (feature registered + four-forces refined),
  `docs/product/journeys/redesign-tests.yaml`

## Version

Plugin `0.7.0` → `0.8.0`.
