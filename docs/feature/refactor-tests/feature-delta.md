# Feature Delta — refactor-tests

Wave DISCUSS complete · density: lean (Tier-1 [REF] only) · 2026-07-01
Feature type: user-facing · JTBD: yes · walking skeleton: brownfield extension (slice 01)

---

## Wave: DISCUSS / [REF] Persona

**tess-test-maintainer (Tess)** — a developer who owns a test suite in a repo using the
phil plugin, trusts `/phil:refactor` on production code *because the tests catch her
mistakes*, and needs that same trust when the tests themselves are what changes.

## Wave: DISCUSS / [REF] JTBD one-liner

When my test suite has accumulated smells after feature work, I want to clean the test
code up to `testing.md` standards **without silently weakening what the tests verify**, so
I can keep trusting the suite as a safety net. (`job_id: keep-test-suite-trustworthy`)

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | Test refactoring is **structure-only** (assertion-preserving moves). | Preserves the suite's meaning; avoids needing a behavioral oracle for v1. |
| D2 | Safety oracle = **human approval per proposed diff**; a green suite is only a secondary sanity check. An **automated test-diff critic** is a planned *augmentation* (pre-screen before the human gate) — DESIGN to plan it; it does not replace human approval. | A passing suite cannot prove an assertion was not weakened. Mutation testing is too heavy for v1. Human-in-the-loop is language-agnostic and sufficient given D1; an automated critic can cheaply catch assertion-set changes and reduce review burden. |
| D3 | Ship a **new command `phil:refactor-tests`** — do not expand `phil:refactor` or `phil:refactor-loop`. | `refactor-loop`'s G2 hook + rubric exist to *block* test-file writes; expanding them fights their design. The new command reuses shared modules instead. |
| D4 | Use a **separate `.test-refactoring-backlog.md`**. | No collision with `phil:refactor`'s `.refactoring-backlog.md`. |
| D5 | Structure-only smell set: duplicated setup → *Extract Fixture/Helper*; missing AAA → *reorder into Arrange-Act-Assert*; vague name → *Rename*; long test with extractable block → *Extract Test Helper*. | These are provably assertion-preserving. Assert-splitting changes test identity/count, so it is excluded. |
| D6 | Language scope v1 = **Python + TypeScript/React**; extensible. | Matches the plugin's existing rule coverage; the human-review oracle removes any per-language AST dependency. |
| D7 | Inherit `phil:refactor` safety: never refactor on a red suite; **auto-revert** on post-apply red; **one commit per approved item**. | Keeps each change attributable and reversible. |

## Wave: DISCUSS / [REF] Driving ports

- **CLI/skill command**: `/phil:refactor-tests [--review] [<path> | <test-id>]`
  - `--review <path>` → detection only, writes the backlog.
  - `<path>`/`<test-id>` → scope to one file or test.
  - no arg → work the existing backlog.
- **Skill bundle**: `skills/refactor-tests/SKILL.md` (loaded by the command).

## Wave: DISCUSS / [REF] Pre-requisites

- Shared test-runner detection (`skills/shared/test-runner-detection.md`).
- A git repository with a runnable test suite.
- `CLAUDE.md` test command (preferred) or an auto-detectable runner.

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: keep-test-suite-trustworthy`.

### S1 — Review tests for structure smells
As Tess, I want to scan my test files for `testing.md` structure smells and get a
prioritized backlog, so I can see what needs cleanup.

**Elevator Pitch**
Before: Tess cannot see, in one place, where her tests break `testing.md` structure standards.
After: run `/phil:refactor-tests --review tests/` → sees a prioritized `.test-refactoring-backlog.md` (file:line + named move per smell).
Decision enabled: which test smells are worth cleaning.

**Acceptance criteria**
- AC1.1: Given a path with test files, when `--review` runs, then `.test-refactoring-backlog.md` is written listing each detected smell with `file:line`, the named move (D5), and a priority.
- AC1.2: Only the D5 smell set is reported; no behavior-changing or deletion items appear.
- AC1.3: Test files are detected by the same globs `rules/testing.md` scopes itself to; non-test files are ignored.

### S2 — Apply one move, human-approved  *(walking skeleton — slice 01)*
As Tess, I want the tool to propose one assertion-preserving test refactoring at a time and
apply it only after I approve the diff, so I stay in control of my safety net.

**Elevator Pitch**
Before: Tess cannot safely auto-refactor tests; a green suite does not prove assertions were preserved.
After: run `/phil:refactor-tests` → sees a proposed diff for one move (e.g. Extract Fixture) → approves → tool applies it, runs the suite green, commits.
Decision enabled: per-diff, whether the change preserves intent.

**Acceptance criteria**
- AC2.1: Given a green baseline suite, when the tool proposes a move, then it shows the full diff, the named move, and a one-line rationale, and applies nothing until Tess approves.
- AC2.2: On approval, the tool applies the diff, re-runs the suite, and only commits if the suite is green.
- AC2.3: If the suite is red after applying, the tool auto-reverts (`git checkout`) and marks the item blocked (D7).
- AC2.4: If Tess rejects, nothing is written; the item is skipped.
- AC2.5: If the baseline suite is red, the tool stops and reports — it never refactors on red (D7).

### S3 — Work the whole backlog
As Tess, I want to work through the whole test backlog one approved move at a time until
it's clean, so cleanup is systematic, not ad hoc.

**Elevator Pitch**
Before: Tess cleans tests ad hoc and loses track.
After: run `/phil:refactor-tests` on an existing backlog → propose→approve→apply→commit loop, reporting "3 of 7 done".
Decision enabled: when the suite is clean enough to stop.

**Acceptance criteria**
- AC3.1: Given a backlog with pending items, the tool loops S2 per item in priority order.
- AC3.2: After each landed item, a prune pass marks incidentally-resolved items `resolved (incidental)`.
- AC3.3: Progress is reported after each item ("N of total done, M pruned, next: ...").
- AC3.4: The loop stops when all items are done/resolved/blocked, or Tess interrupts (progress saved for resume).

### S4 — Target a single file or test
As Tess, I want to point the command at one test file or test id, so I can clean just what
I'm working on without a full review.

**Elevator Pitch**
Before: Tess must review the whole suite to fix one known-bad test.
After: run `/phil:refactor-tests tests/test_orders.py` → the propose→approve→apply loop runs scoped to that file only.
Decision enabled: whether that one file is clean.

**Acceptance criteria**
- AC4.1: Given a file path or test id, the tool scopes detection and moves to that target only.
- AC4.2: Same approval, suite, revert, and commit guarantees as S2 apply.

## Wave: DISCUSS / [REF] Out of scope

- Behavior-changing test improvements: determinism fixes (static timestamps, seeded RNG,
  injected clocks), tightening loose assertions, assert-splitting.
- Deleting dead/duplicate tests.
- A mutation-testing oracle.
- Expanding `phil:refactor` or `phil:refactor-loop` (D3).
- Languages beyond Python + TypeScript/React in v1 (D6).
- Auto-apply without human approval (D2).

## Wave: DISCUSS / [REF] WS strategy

**Strategy B (brownfield extension).** New command in an existing plugin, reusing
test-runner detection and the backlog/loop pattern from `phil:refactor`. Walking skeleton =
**slice 01** (S2 thin path: one smell type → propose → approve → apply → green → commit),
dogfooded on this plugin's own tests.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| Approval-gated safety | 100% of applied test diffs were human-approved | Command never writes a test file without a recorded approval. |
| Post-apply integrity | 0 committed changes on a red suite | Every commit is preceded by a green suite run; red → revert. |
| Cleanup throughput | ≥ 70% of backlog items closed (done + pruned) per session on a real suite | Backlog status counts. |
| Detection precision | ≤ 20% of `--review` items rejected as false positives on first dogfood run | Reject rate during S2/S3. |

## Wave: DISCUSS / [REF] Definition of Done

1. `/phil:refactor-tests` command + `skills/refactor-tests/SKILL.md` exist and load.
2. `--review` writes a valid `.test-refactoring-backlog.md` (S1 ACs).
3. Propose→approve→apply→suite→commit loop works with human gate (S2 ACs).
4. Backlog loop + prune + progress reporting work (S3 ACs).
5. Single-target mode works (S4 ACs).
6. Never refactors on red; auto-reverts on post-apply red (D7).
7. Only D5 structure-only moves are ever applied; no behavior change.
8. Acceptance tests cover happy path + the four error paths.
9. Docs updated (command help + skill); wave artifacts committed.

## Wave: DISCUSS / [REF] Scope assessment

**PASS (right-sized).** ~4 stories, 2–3 modules, no >5-integration-point skeleton, well
under 2 weeks. No split required. Carpaccio slicing → 3 slices (below).

## Wave: DISCUSS / [REF] Wave decisions summary

- Primary job: `keep-test-suite-trustworthy` — clean tests to `testing.md` structure
  standards without weakening assertions.
- Feature type: user-facing. Walking skeleton: slice 01 (strategy B).
- Constraints: structure-only (D1); human-approval oracle (D2); new command (D3); separate
  backlog (D4); D5 smell set; Python + TS/React (D6); inherit phil:refactor safety (D7).
- Upstream changes: none (greenfield SSOT bootstrap — created `docs/product/jobs.yaml`,
  `personas/tess-test-maintainer.yaml`, `journeys/refactor-tests.yaml`).

## Wave: DISCUSS / [REF] DoR validation

| # | DoR item | Status | Evidence |
|---|----------|--------|----------|
| 1 | Story in LeanUX format | ✓ | S1–S4 above |
| 2 | Acceptance criteria testable | ✓ | AC1.1–AC4.2, all observable |
| 3 | Job traceability | ✓ | all stories → `keep-test-suite-trustworthy` in jobs.yaml |
| 4 | Elevator pitch per story (real entry point + observable output) | ✓ | each story cites `/phil:refactor-tests ...` + concrete output |
| 5 | Dependencies identified | ✓ | Pre-requisites section |
| 6 | Out-of-scope explicit | ✓ | Out of scope section |
| 7 | Sized / sliceable | ✓ | scope assessment PASS; 3 carpaccio slices |
| 8 | Journey + emotional arc defined | ✓ | `journeys/refactor-tests.yaml` |
| 9 | No blocking ambiguities | ✓ | three cruxes (oracle/invocation/scope) resolved as D1–D3 |

Requirements completeness: **0.97** (all stories have job trace, elevator pitch, testable
ACs; only second-order DESIGN details — detector implementation, backlog schema — deferred).

## Wave: DISCUSS / [REF] Handoff

**To:** nw-solution-architect (DESIGN — full artifact set) + nw-platform-architect
(DEVOPS — outcome-kpis only). Open for DESIGN:

- Test-smell detector implementation and backlog file schema.
- How the approval prompt is surfaced (AskUserQuestion vs. plain diff + confirm).
- Reuse boundaries with `phil:refactor`'s loop.
- **Automated test-diff critic** (D2 augmentation): whether and how to build a read-only
  reflection critic that pre-screens each proposed diff for assertion-set preservation /
  structure-only compliance before the human gate, modelled on `refactor-critic-correctness`.
  A first-pass draft was forged prematurely and reverted; it is recoverable from git history
  (commit `b29f6aa`: `agents/refactor-tests-critic.md` + `skills/refactor-tests-critic/`) if
  DESIGN chooses to promote it rather than design from scratch.

---

# DESIGN wave

Scope: application/components · mode: propose · architect: Morgan (nw-solution-architect)
· 2026-07-01

## Wave: DESIGN / [REF] Quality attributes (ranked)

1. **Correctness/safety** — never silently weaken a test (the whole point).
2. **Usability** — low review burden per approved change.
3. **Maintainability** — reuse proven patterns; keep the loop legible.
4. **Extensibility** — clean seam for the deferred critic and new smell types.

## Wave: DESIGN / [REF] DDD list (design decisions)

| ID | Decision | Rationale |
|----|----------|-----------|
| DD1 | New `commands/refactor-tests.md` (thin loader) → `skills/refactor-tests/SKILL.md`, mirroring `phil:refactor`'s command→skill split. | Matches the plugin's established shape; auto-discovered, no manifest change. |
| DD2 | Ports-and-adapters: the loop core lives in the skill; git, filesystem, test-runner, and **human-approval** are ports. | Isolates side effects; the human is a first-class interaction port. |
| DD3 | The **D5 test-smell detector is new**, lives in the skill, and writes `.test-refactoring-backlog.md` in review-code's format **by convention**. `review-code` stays UNCHANGED. | review-code's "Test Quality" targets behavior smells (coupling/flakiness/mocking), not the D5 structure moves; overloading it repeats the DISCUSS-D3 anti-pattern. |
| DD4 | **Approval mechanism** = apply the proposed change to the working tree → run the suite (sanity) → pause and ask the human to review the *uncommitted diff in their IDE/editor* → structured approve/reject/skip/quit via AskUserQuestion, **no diff printed in chat**. Approve → commit; reject/quit → `git checkout` revert. | Developers review diffs best in their editor against git; chat-printed diffs are noisy and lossy. Refines DISCUSS-D2 mechanics without changing the human-approval oracle. |
| DD5 | The automated test-diff critic is **deferred to slice 04**; the propose step exposes a clean pre-screen seam. Promote `b29f6aa` when built. | Its value (cutting review burden) is only measurable once a working loop exists — empirical over speculative. |
| DD6 | Inherit `phil:refactor` safety: never refactor on a red baseline; **auto-revert** on post-apply red (before bothering the human); one commit per approved item. | Each change stays attributable and reversible. |
| DD7 | No new hook. The G2 test-file lockbox (`hooks/refactor-loop/block-test-file-write.py`) stays inert — it is gated on the refactor-loop ledger sentinel this command never writes. | The command must write test files; the lockbox is scoped to refactor-loop runs only. |
| DD8 | No development paradigm selected / no CLAUDE.md paradigm write. | The feature's surface is a prose skill + reused Bash/git mechanics — no application-code paradigm applies. |

## Wave: DESIGN / [REF] Component decomposition

| Component | Path | Change type |
|-----------|------|-------------|
| refactor-tests command (loader) | `commands/refactor-tests.md` | CREATE NEW |
| refactor-tests skill (loop + D5 taxonomy + gate) | `skills/refactor-tests/SKILL.md` | CREATE NEW |
| test-runner detection | `skills/shared/test-runner-detection.md` | REUSE as-is |
| backlog file | `.test-refactoring-backlog.md` (project root) | CREATE NEW (review-code format) |
| test-diff critic | `agents/refactor-tests-critic.md` | DEFER (slice 04; draft at `b29f6aa`) |

## Wave: DESIGN / [REF] Driving ports

- CLI/skill: `/phil:refactor-tests` — `--review <path>` (detect → backlog), `<path>|<test-id>`
  (scope the loop), no arg (work the existing backlog).

## Wave: DESIGN / [REF] Driven ports + adapters

| Driven port | Adapter | Reuse |
|-------------|---------|-------|
| Locate test runner | `skills/shared/test-runner-detection.md` | reuse |
| Read tests / write backlog / apply diff | filesystem (Read/Edit/Write) | reuse |
| Checkpoint / commit / revert | git via Bash | reuse `phil:refactor` mechanics |
| Run suite (baseline + post-apply sanity) | test runner via Bash | reuse |
| Human approval | AskUserQuestion + human's IDE diff review | CREATE NEW (DD4) |

## Wave: DESIGN / [REF] Technology choices

- Prose skill (Markdown) executed by the model; Bash for git + suite; AskUserQuestion for the
  gate. No new runtime, language, or dependency. Cross-platform (the plugin targets Windows
  PowerShell + Bash) — git/test commands run through the existing Bash tool.

## Wave: DESIGN / [REF] Reuse Analysis

| Existing Component | File | Overlap | Decision | Justification |
|-------------------|------|---------|----------|---------------|
| review-code skill | `skills/review-code/SKILL.md` | writes a prioritized refactoring backlog; has a Test-Quality category | **CREATE NEW** detector + reuse format by convention | D5 structure-move detection (AAA / fixture extraction) does not exist there; review-code targets behavior/quality test smells and stays UNCHANGED (DISCUSS-D3). |
| phil:refactor loop | `skills/refactor/SKILL.md` | backlog-driven apply→verify→commit→prune loop | **EXTEND pattern** (new skill, same loop shape, swapped gate) | The loop template is proven; only the gate (auto pass/fail → human approval) and the move set (structure-only test moves) differ. |
| test-runner detection | `skills/shared/test-runner-detection.md` | baseline suite detection | **REUSE as-is** | Identical need; already a shared module. |
| refactor-critic-correctness | `agents/refactor-critic-correctness.md` | diff critique verdict | **DEFER** (slice 04) | Critic is a v2 augmentation; draft recoverable at `b29f6aa`. |
| G2 lockbox hook | `hooks/refactor-loop/block-test-file-write.py` | blocks test-file writes | **NO CHANGE** | Inert outside refactor-loop runs (ledger-sentinel gated). |

Zero unjustified CREATE NEW rows.

## Wave: DESIGN / [REF] Decisions table

| DDD-N | Decision |
|-------|----------|
| DD1 | new command + skill (command→skill split) |
| DD2 | ports-and-adapters, human-approval port |
| DD3 | new D5 detector, review-code untouched, shared backlog format by convention |
| DD4 | apply→suite→IDE review→structured approve/reject; no chat diffs |
| DD5 | critic deferred to slice 04 |
| DD6 | inherit refactor safety (no red; auto-revert; commit per item) |
| DD7 | no new hook; G2 stays inert |
| DD8 | no paradigm write |

## Wave: DESIGN / [REF] Open questions (deferred to DISTILL/DELIVER)

- Exact backlog schema fields for test smells (reuse review-code's, minus prod-only fields).
- Precise D5 detection heuristics per language (Python vs TS/React) — DISTILL acceptance tests
  will pin these with examples.
- Critic pre-screen contract at the slice-04 seam (inputs/outputs already drafted in `b29f6aa`).

## Wave: DESIGN / [REF] Outcome collision check

**Skipped (N/A).** No `docs/product/outcomes/registry.yaml` exists in this plugin repo, and the
`nwave-ai outcomes` CLI is a construct of the nwave codebase, not this plugin. No contract
registry to collide against.

## Wave: DESIGN / [REF] Wave decisions summary

- Pattern: modular prose skill with ports-and-adapters; human-approval as an interaction port.
- Paradigm: N/A (prose + reused Bash/git).
- Key components: `commands/refactor-tests.md`, `skills/refactor-tests/SKILL.md`; reuse
  `test-runner-detection`; defer the critic.
- Constraints: structure-only (D1); human-approval oracle via IDE diff review (D2/DD4);
  new command, review-code untouched (D3/DD3); inherit refactor safety (DD6).
- Upstream changes: none — DD4 refines D2's *mechanism* (how approval is surfaced) without
  changing the decision, so no `## Changed Assumptions` back-propagation is warranted.

## Wave: DESIGN / [REF] Handoff

**To:** nw-platform-architect (DEVOPS). This is a prose-skill feature with no infrastructure,
deployment, or observability surface beyond the existing plugin — DEVOPS is expected to be a
near-no-op. Then DISTILL authors acceptance tests for the happy path + four error paths and
pins the D5 detection heuristics.

---

# DISTILL wave

Scope: acceptance tests · density: lean (Tier-1 [REF] only) · designer: main instance
· 2026-07-02 · DEVOPS: **skipped** (no KPI contracts; prose-skill feature, near-no-op per DESIGN handoff)

## Wave: DISTILL / [REF] Reconciliation

Checked DISCUSS D1–D7 against DESIGN DD1–DD8. **0 contradictions.** DD4 refines D2's approval
*mechanism* (apply→suite→IDE review→structured approve/reject) without changing the
human-approval oracle; DESIGN's own summary confirms no back-propagation warranted. Gate passed.

## Wave: DISTILL / [REF] Test approach (project-convention override)

The standard pytest-bdd `.feature` + Python RED-scaffold machinery does **not** fit: DDD8 says
this feature is a prose skill executed by the model — there is no application module to scaffold,
and the repo has no pytest-bdd harness. Per the DISTILL "project conventions always win" rule,
the acceptance suite mirrors the plugin's own **golden-fixture self-test** convention
(`refactor/self-test/`): self-contained fixtures that feed the safety loop known situations and
assert the correct gate outcome.

**Inherent oracle limit (D2/ADR-002):** the safety oracle is a *human*. The deterministic git
safety mechanics (never-on-red, auto-revert-on-post-apply-red, commit-only-green, one-commit-
per-item) are fixture-driveable and are pinned here. The human approve/reject *judgement* is
supplied by fixture manifests for unattended runs and validated live by same-day dogfood (the
slices), not by an automated assertion.

## Wave: DISTILL / [REF] Scenario list with tags

SSOT for scenarios: `skills/refactor-tests/acceptance.feature`. Deterministic mechanics SSOT:
`skills/refactor-tests/self-test/`.

| Scenario | Story | Tags | Fixture (deterministic) |
|----------|-------|------|-------------------------|
| Review pass seeds a prioritized backlog | S1 | `@review` | `05-review-seeds-backlog` |
| One approved move applied, verified, committed | S2 | `@walking_skeleton @human-gate` | `03-approve-commit-on-green` |
| Rejected move leaves suite untouched | S2 | `@error @human-gate` | `04-reject-reverts-clean` |
| Move that breaks suite is reverted pre-gate | S2 | `@error` | `02-postapply-red-autorevert` |
| Never refactors on a red suite | S2 | `@error` | `01-baseline-red-stop` |
| Backlog worked one approved move at a time | S3 | `@loop @requires-human` | — (dogfood) |
| Loop interrupted and resumed | S3 | `@loop @requires-human` | — (dogfood) |
| Cleanup scoped to a single file | S4 | `@scoped @requires-human` | — (dogfood) |

Error-path coverage: 3 of 5 fixture-backed scenarios are error paths (60%) — exceeds the ≥40% target.
DoD "happy path + four error paths": happy = `03`; four errors = `01` (baseline red), `02`
(post-apply red), `04` (reject), plus review false-positive/negative guarded by `05`.

## Wave: DISTILL / [REF] Adapter coverage

| Driven port | Adapter | Exercised by | Real I/O |
|-------------|---------|--------------|----------|
| Run suite (baseline + post-apply) | test runner via Bash (`pytest`) | fixtures 01–04 (real pytest runs) | ✅ real-io |
| Checkpoint / commit / revert | git via Bash | fixtures 02 (revert), 03 (commit), 04 (revert) | ✅ real-io |
| Read tests / write backlog | filesystem | fixture 05 (real files → real backlog) | ✅ real-io |
| Locate test runner | `skills/shared/test-runner-detection.md` (reuse) | all fixtures (pytest auto-detected) | ✅ real-io |
| Human approval | AskUserQuestion + IDE diff review | 03 (approve), 04 (reject) — decision from manifest offline; human live | fake offline / real dogfood |

No driven adapter is left without a real-I/O fixture, except the human-approval port whose
real exercise is inherently the live dogfood (documented limit above).

## Wave: DISTILL / [REF] Driving adapter coverage

The single driving adapter is the `/phil:refactor-tests` command. Every mode is covered:
`--review <path>` → fixture 05; `<path>` scoped run → fixtures 01–04; no-arg backlog loop →
S3 dogfood scenarios. Once `commands/refactor-tests.md` + `SKILL.md` exist (DELIVER), driving a
fixture = invoking the command scoped to that fixture dir.

## Wave: DISTILL / [REF] Scaffolds (RED-ready)

No production code module exists to scaffold (DDD8). The RED-ready artifacts are the fixtures +
the absent skill they drive:

- `skills/refactor-tests/self-test/01-baseline-red-stop/` — `cart.py` (buggy), `test_cart.py`, `manifest.json`, `expected.md`
- `skills/refactor-tests/self-test/02-postapply-red-autorevert/` — `cart.py`, `test_cart.py`, `move.patch`, `manifest.json`, `expected.md`
- `skills/refactor-tests/self-test/03-approve-commit-on-green/` — `cart.py`, `test_cart.py`, `move.patch`, `manifest.json`, `expected.md`
- `skills/refactor-tests/self-test/04-reject-reverts-clean/` — `cart.py`, `test_cart.py`, `move.patch`, `manifest.json`, `expected.md`
- `skills/refactor-tests/self-test/05-review-seeds-backlog/` — `cart.py`, `test_cart_smells.py`, `manifest.json`, `expected.md`, `expected-backlog.md`
- `skills/refactor-tests/self-test/README.md` — how to drive the suite as the skill gate
- `skills/refactor-tests/acceptance.feature` — scenario SSOT

RED classification (fail-for-the-right-reason): `docs/feature/refactor-tests/distill/red-classification.md`.
All fixtures verified BROKEN-free — baselines run under pytest (01 red by design; 02–05 green),
all patches `git apply --check` clean; the suite is un-driveable only because `SKILL.md` is absent.

## Wave: DISTILL / [REF] Test placement

`skills/refactor-tests/self-test/` (co-located with the skill it validates) +
`skills/refactor-tests/acceptance.feature`. **Precedent:** `refactor/self-test/` — the plugin's
existing skill/gate self-test; same fixture format (`before` code, `move.patch`, `manifest.json`,
`expected.md`, README driver). Co-location keeps the CREATE-NEW feature self-contained.

## Wave: DISTILL / [REF] Register outcomes

**Skipped.** No `docs/product/outcomes/registry.yaml` in this plugin, and the `nwave-ai outcomes`
CLI is not part of this repo (DESIGN made the same call for the collision check). Feature ships a
prose skill, not a typed contract surface in the registry's sense.

## Wave: DISTILL / [REF] Pre-requisites

- DESIGN driving/driven ports (above): command `/phil:refactor-tests`; git, filesystem, test
  runner, human-approval adapters.
- `skills/shared/test-runner-detection.md` (reuse).
- A git repo with a runnable suite; `python -m pytest` for the fixtures.
- DEVOPS environment matrix: N/A (skipped) — default local git + pytest.

## Wave: DISTILL / [REF] Self-review

- WS scenario present, tagged `@walking_skeleton`, backed by fixture `03` (green). ✅
- Every driven adapter has a real-I/O fixture except human-approval (documented limit). ✅
- Business-language scenarios; mechanics live in fixtures/steps, not in `.feature`. ✅
- Error-path coverage 60% (≥40% target). ✅
- Fixtures are RED (not BROKEN): baselines run, patches apply, states verified. ✅
- Language: Python fixtures (matches `refactor/self-test/` + D6 Python scope). TS/React
  detector coverage is a documented forward gap — add a `.test.tsx` review fixture when the
  detector's TS heuristics are pinned in DELIVER slice 02 (D6 keeps TS in v1 scope).

## Wave: DISTILL / [REF] Handoff

**To:** DELIVER. Author `commands/refactor-tests.md` + `skills/refactor-tests/SKILL.md` slice by
slice; at each RED-phase entry read `distill/red-classification.md` and drive the mapped
fixtures to their `expected.md` outcome (slice 01 → fixtures 01–04; slice 02 → fixture 05 +
a TS review fixture; slice 03 → the `@loop` scenarios). The suite in `self-test/` is the
regression gate for every subsequent edit to the skill.

---

# DELIVER wave

Scope: prose-skill authoring · density: lean (Tier-1 [REF] only) · 2026-07-02

## Wave: DELIVER / [REF] Execution note (paradigm adaptation)

Per DDD8, this feature's production code is **prose** — `commands/refactor-tests.md` +
`skills/refactor-tests/SKILL.md`, executed by the model. There is no application code, no
pytest suite to green, no mutation target, and no OOP/functional paradigm (confirmed: `CLAUDE.md`
has no `## Development Paradigm`; no `.nwave/des-config.json` rigor profile). The standard
DES-monitored code-TDD machinery (roadmap.json → crafter subagents doing RED→GREEN→COMMIT →
mutation) does not apply and was **not** run — it would be theater on Markdown. DELIVER was
adapted: the main instance authored the two prose files directly, then validated by dogfooding
the committed self-test fixtures. This is DES-exempt in the sense of the enforcement clause
("non-deliver tasks: docs"). Deviation logged here for the finalize/back-propagation record.

## Wave: DELIVER / [REF] Implementation summary

Shipped `/phil:refactor-tests` — a human-approved, structure-only test-refactoring loop. The
thin command loader defers to `skills/refactor-tests/SKILL.md`, which contains: the four-move D5
taxonomy with per-language (Python + TS/React) detection heuristics; `testing.md`-scoped
test-file globs; `--review` backlog seeding in `review-code` format (by convention); and the
apply-then-review loop (green-baseline gate → propose without chat diff → apply → suite sanity →
auto-revert on red → IDE-diff human gate via AskUserQuestion approve/reject/skip/quit → one
commit per approved item → prune + progress). Reuses `skills/shared/test-runner-detection.md`.
The deferred critic (slice 04) is left as a documented pre-screen seam in the propose step.

## Wave: DELIVER / [REF] Files modified

Production (prose):
- `commands/refactor-tests.md` — CREATE NEW: thin loader (description, argument-hint, allowed-tools → skill).
- `skills/refactor-tests/SKILL.md` — CREATE NEW: loop core + D5 taxonomy + detection heuristics + human gate.

Reused unchanged: `skills/shared/test-runner-detection.md`, `rules/testing.md`, `review-code` backlog format.
Tests (from DISTILL, already committed): `skills/refactor-tests/self-test/**`, `skills/refactor-tests/acceptance.feature`.
Docs: this `feature-delta.md`.

Design compliance: both files are exactly the two CREATE-NEW components in the DESIGN Component
Decomposition table. No unauthorized new component; `review-code` and the G2 hook untouched (DD3/DD7).

## Wave: DELIVER / [REF] Scenarios green count

Deterministic safety mechanics: **4 of 4 fixtures dogfooded PASS** (01 baseline-red→STOP,
02 post-apply-red→auto-revert, 03 approve→commit-on-green, 04 reject→clean-revert) — each run in a
throwaway git repo executing the exact git/suite sequence `SKILL.md` prescribes; outcomes matched
every `expected.md`. Fixture 05 (`--review`→backlog) and the S3/S4 `@requires-human` scenarios are
**authored + structurally verified** (detection heuristics ↔ `expected-backlog.md` aligned; loop
steps present); their full behavioral confirmation is a live LLM+human dogfood run — inherent to a
prose skill whose oracle is the developer (D2/ADR-002), pending with the maintainer.

## Wave: DELIVER / [REF] DoD check (vs DISCUSS Definition of Done)

| # | DoD item | Status |
|---|----------|--------|
| 1 | command + SKILL.md exist and load | ✅ created; convention-auto-discovered; loader→skill link verified |
| 2 | `--review` writes valid backlog (S1) | ✅ authored (review mode + format); precision KPI needs live dogfood |
| 3 | propose→approve→apply→suite→commit human gate (S2) | ✅ authored; git/suite mechanics dogfooded (fixture 03) |
| 4 | backlog loop + prune + progress (S3) | ✅ authored; live loop run pending (human gate) |
| 5 | single-target mode (S4) | ✅ authored (Scoped mode) |
| 6 | never on red; auto-revert on post-apply red (D7) | ✅ authored + dogfooded (fixtures 01, 02) |
| 7 | only D5 structure moves; no behavior change | ✅ authored — explicit scope guards + "never in scope" list |
| 8 | acceptance tests cover happy + four errors | ✅ DISTILL fixtures committed; happy+4 errors dogfooded |
| 9 | docs updated (command help + skill); artifacts committed | ✅ command description/argument-hint; committed at finalize |

## Wave: DELIVER / [REF] Demo evidence — 2026-07-02

Dogfood of the loop's prescribed mechanics (throwaway git repos, real `pytest` + `git`):

```
Fixture 01 baseline-red-stop:      baseline suite=red  -> STOP, apply nothing          => PASS
Fixture 02 postapply-red-autorevert: baseline=green, post-apply=red -> git checkout    => REVERT, 0 commits, tracked-tree clean => PASS
Fixture 03 approve-commit-on-green:  baseline=green, post-apply=green -> approve -> commit => suite green, 1 new commit => PASS
Fixture 04 reject-reverts-clean:     post-apply=green -> reject -> git checkout         => clean revert, 0 commits => PASS
```

## Wave: DELIVER / [REF] Quality gates

- Design compliance: ✅ only the two authorized CREATE-NEW files; reuse boundaries honored.
- Wave-completion invariants: ✅ no `__SCAFFOLD__` markers; no dual code paths (nothing superseded).
- DES code-TDD / roadmap / mutation / L1-L6 refactor: N/A — prose deliverable (adaptation note above).
- Review: nw-software-crafter-reviewer (prose-framed) — see review outcome recorded at finalize.

## Wave: DELIVER / [REF] Pre-requisites

DISTILL fixtures + `acceptance.feature` (committed); DESIGN component decomposition + reuse
analysis; `skills/shared/test-runner-detection.md`; `rules/testing.md` globs + smell standards;
`review-code` backlog format. Runtime: git + a project test runner (per shared detection).
