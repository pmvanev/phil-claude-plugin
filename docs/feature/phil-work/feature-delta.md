# Feature Delta — phil-work

Wave-by-wave record for `/phil:work` — a wave-based orchestrator for invisible (non-user-facing) technical initiatives. Density: **lean** (Tier-1 [REF] only; no Tier-2 expansions rendered).

Source brief: `docs/superpowers/specs/2026-07-13-phil-work-design.md`.

---

## Wave: DISCUSS / [REF] Persona

**quinn-codebase-steward** (Quinn) — developer responsible for a codebase's health and structure, doing invisible technical work (refactor, re-architecture, migration, cleanup, perf/dependency). SSOT: `docs/product/personas/quinn-codebase-steward.yaml`.

## Wave: DISCUSS / [REF] JTBD one-liner

`deliver-invisible-work-with-discipline` — When I have technical work the end user never sees, I want the same disciplined, multi-wave, test-backed workflow nwave gives features, so I can carry it through safely and leave a decision trail. SSOT: `docs/product/jobs.yaml`.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = infrastructure/tooling (developer-facing CLI+skill). Rationale: matches `refactor-tests`/`redesign-tests` classification; JTBD still applies (real persona).
- **[D2]** JTBD mandatory — not the infrastructure-only escape valve. Rationale: `/phil:work` has observable output; reviewer would reject infra-only.
- **[D3]** General-contractor model: the orchestrator discusses, plans, and gates, then **delegates execution to existing tactical skills** (`refactor-loop`, `refactor`, `extract-method`, `review-code`, `clean-comments`, `redesign-tests`, `refactor-tests`) and shares existing rules. It does not re-implement execution. Rationale: the user's "piece it together from what I've already written"; avoids duplicating nwave/tactical logic; mirrors nwave's orchestrator+specialists shape.
- **[D4]** Verification spine = **preservation floor (always) + declared initiative goal (per initiative)**. Both gate every wave. The preservation-floor **oracle is artifact-type-aware** (see D9): the executable test/self-test suite where one exists, else the human-approval diff oracle as fallback; hardened to characterization-tests-intact (or self-test-scenarios-intact) in slice 03. Rationale: the ATDD analog for work with no user story.
- **[D5]** Scope = broad (all invisible technical initiatives). Explicitly OUT: user-facing features (nwave owns those) and one-shot tidyups a single tactical skill already handles.
- **[D6]** Delivered as **5 thin end-to-end slices**; slice 01 is the walking skeleton. Rationale: Phase 1.5 scope assessment = OVERSIZED (4 signals).
- **[D7]** FRAME carries an **off-ramp**: if a single tactical skill would suffice, recommend running it directly and exit — no ceremony. Rationale: directly answers anxiety B (overhead for small work).
- **[D8]** A per-initiative **documentation trail** (frame, roadmap, decisions, progress, evolution) is a required output. Exact namespace/schema (`docs/work/<initiative>/` vs. reuse `docs/feature/`) is **deferred to DESIGN**.
- **[D9]** Target artifacts are frequently **prose** — Claude Code skills, rules, agents, commands — not executable code, and `/phil:work` itself is built as prose (a command + `SKILL.md`, possibly agents/rules). Consequences: (a) **"tests when warranted" means acceptance / self-test harnesses** (as in `skills/refactor-tests/self-test/`, `skills/redesign-tests/self-test/`), not unit tests of code; (b) the **preservation-floor oracle** is the self-test/acceptance harness where one exists, and the **human-approval diff oracle** (`refactor-tests`, ADR-002 — apply move, pause for IDE diff review, commit/revert) as fallback where no executable oracle exists; (c) **goal metrics generalize** to prose-checkable forms (self-test passes, no dead links / broken skill refs, valid frontmatter, file under N lines, cites a required source). Rationale: user correction (2026-07-13) — this plugin's initiatives, and this feature's own build, are prose-first; refines the "suite green" phrasing in the source brief.

## Wave: DISCUSS / [REF] User stories

Every story traces to job `deliver-invisible-work-with-discipline`. One story per slice.

### Story 1 — Walking skeleton (slice 01)
As Quinn, I run `/phil:work` on one initiative and it carries the change end-to-end via one delegated skill, preserving behavior and leaving a decision doc.

**### Elevator Pitch**
Before: I can't run a disciplined, documented, behavior-preserving pass on an invisible initiative without fighting nwave or firing a tactical skill blind.
After: run `/phil:work "extract BillingCalculator from OrderService"` → sees a summary: `goal captured · delegated to refactor-loop · suite green (142 passed) · 1 structural commit · decisions.md written`.
Decision enabled: whether the initiative is done and safe to keep, or needs another pass.

**ACs:** (a) a run on a repo with a passing preservation oracle (self-test/suite, or a clean human-approval baseline) produces confirmed goal + preservation contract, a delegated change, a still-passing oracle, and `decisions.md` — verified on a real initiative; (b) if the oracle fails after delegation (suite red, self-test broken, or diff rejected), the run reports failure and leaves the tree in its last-good state; (c) for an initiative one skill clearly handles, FRAME recommends that skill and exits. *(Oracle selection per D9: executable where it exists, else human-approval diff.)*

### Story 2 — MAP roadmap (slice 02)
As Quinn, I get an editable wave-by-wave roadmap for a multi-step initiative, executed in sequence.

**### Elevator Pitch**
Before: a big initiative is a cliff — I can't see the safe sequence of steps.
After: run `/phil:work "split the God object"` → after FRAME, sees a roadmap: `Wave 1 extract-method → Wave 2 refactor-loop → Wave 3 review-code`, each with its gate, editable before it runs.
Decision enabled: whether the plan is the right sequence, or I reorder/trim before execution.

**ACs:** (a) a real multi-step initiative yields an ordered roadmap (≥2 waves) each naming a delegated skill + gate; developer can edit it; EXECUTE runs waves in order, each ending green with a separate commit; (b) the trail records roadmap + per-wave progress; (c) a wave failing its gate stops the sequence and names the failed wave, tree stays green.

### Story 3 — SAFETY-NET (slice 03)
As Quinn, before any structural cut, the tool ensures the change surface is pinned — characterization tests for code, or captured self-test scenarios / a human-approval baseline for prose — so preservation is enforced, not claimed.

**### Elevator Pitch**
Before: "the suite is green" (or "the skill still reads fine") doesn't prove my thin seam is actually protected.
After: run `/phil:work` on a thinly-covered module or an untested skill → SAFETY-NET reports `seam coverage: thin → pinned current behavior (3 characterization tests / captured self-test scenarios) · baseline good` before EXECUTE touches anything.
Decision enabled: whether it's safe to start cutting, or the seam needs more pinning first.

**ACs:** (a) on a thin seam, SAFETY-NET reports the gap, pins current observable behavior (characterization tests for code; captured self-test scenarios or a recorded human-approval baseline for prose), and records a good baseline before EXECUTE; (b) a deliberately behavior-changing edit is caught by the net (failing self-test or a diff the human rejects) and triggers revert of that wave; (c) a seam with no feasible executable oracle falls back to the human-approval diff gate and is flagged for manual review, not passed silently.

### Story 4 — Initiative-goal gate (slice 04)
As Quinn, I declare a checkable goal metric and the tool gates on it, never claiming done unless it's met.

**### Elevator Pitch**
Before: a refactor can "pass tests" yet miss its whole point, and I only notice later.
After: run `/phil:work "cut OrderService fan-out below 5 deps"` → VERIFY reports `goal: deps 8 → 4 (met) · preservation: suite green`; had it stalled at 6, it reports `goal NOT achieved`.
Decision enabled: whether the initiative actually accomplished its aim, or I keep going.

**ACs:** (a) FRAME captures a checkable goal metric and rejects a vague one (or accepts explicit "preservation only"); (b) VERIFY reports goal-met/not-met with evidence; a behavior-preserving run that misses the goal is reported "not achieved," not "done"; (c) trail shows the metric and its VERIFY reading.

### Story 5 — Breadth + trail (slice 05)
As Quinn, MAP routes each wave to the right tactical skill across initiative types, and VERIFY leaves an evolution record.

**### Elevator Pitch**
Before: my tactical skills are separate tools; nothing picks the right one per step or records the initiative's history.
After: run `/phil:work` on a cleanup and on an extraction → MAP routes each wave (`clean-comments`, `extract-method`, …) and VERIFY writes an evolution summary of what changed, why, and outcome vs goal.
Decision enabled: whether the broad workflow genuinely covers different kinds of invisible work with one spine.

**ACs:** (a) MAP selects and justifies an appropriate skill per wave across ≥2 distinct real initiative types; (b) VERIFY produces an evolution summary + decision/progress trail in the settled namespace; (c) each type's full run ends with both gates green or an honest not-met report.

## Wave: DISCUSS / [REF] Story map

- **Backbone (activities):** Frame the initiative → Plan the waves → Establish the safety net → Execute the waves → Verify & document.
- **Walking skeleton:** Story 1 (slice 01) — thinnest end-to-end path: frame → one delegated skill → preserve → document.
- **Slices:** 01 skeleton → 02 MAP → 03 SAFETY-NET → 04 goal gate → 05 breadth+trail. Briefs: `docs/feature/phil-work/slices/slice-01..05-*.md`.
- **Carpaccio taste tests:** all pass (≤2 new components/slice; skeleton shipped first; each disproves a pre-commitment; real-initiative data required; no scale-only duplicates).

## Wave: DISCUSS / [REF] Prioritization

Order = 01 → 02 → 03 → 04 → 05. Rationale: (1) **learning leverage** — slice 01 tests the riskiest premise first (does the contractor model add value at all?); slice 03 tests anxiety C (is preservation enforceable?) before we depend on it. (2) **dependency chain** — each slice builds on the prior. (3) **dogfood cadence** — every slice is usable on a real plugin initiative the same day it ships.

## Wave: DISCUSS / [REF] Outcome KPIs

- **KPI-1 Preservation integrity:** 100% of runs end with the preservation oracle passing (suite/self-test green, or a human-approved diff) OR an explicit revert; **0** runs leave the tree in a failing or unreviewed state. Measure: run/progress logs across dogfood runs.
- **KPI-2 Goal-gate honesty:** 100% of runs (slice 04+) report goal-met vs not-met from the declared metric; **0** false "done". Measure: `decisions.md` verdict vs recorded metric reading.
- **KPI-3 Net efficacy:** ≥1 injected behavior-changing edit per SAFETY-NET acceptance run is caught by the pinned baseline — a failing characterization test/self-test, or a diff the human rejects (target: 100% of injected regressions caught). Measure: slice-03 acceptance runs.
- **KPI-4 Trail completeness:** 100% of runs produce a trail containing goal, preservation result, and per-wave commits. Measure: file-presence + required-field check.
- **KPI-5 Adoption (value proof):** Quinn/Phil uses `/phil:work` for **≥3** real invisible initiatives within 30 days of slice-05 shipping, instead of ad hoc. Measure: dogfood count.

## Wave: DISCUSS / [REF] Definition of Done (9-item)

1. Story format + job traceability — all 5 stories trace to `deliver-invisible-work-with-discipline`. ✓
2. Acceptance criteria testable — each story's ACs are observable end-to-end. ✓
3. Elevator pitch per story — real command → observable output → decision. ✓
4. Slices ≤1 day, each with learning hypothesis + brief. ✓
5. Every slice ships user-visible value (no infra-only slice). ✓
6. Dependencies identified per slice. ✓
7. Outcome KPIs with numeric targets + measurement method. ✓
8. Out-of-scope explicit. ✓
9. Handoff accepted by DESIGN (nw-solution-architect). ☐ pending

## Wave: DISCUSS / [REF] Out-of-scope

- User-facing features — nwave owns those.
- One-shot tidyups a single tactical skill already handles (FRAME off-ramps these).
- A bespoke migration engine — migrations are handled as re-architecture initiatives via delegation.
- An automated goal-metric *inference* engine — the developer declares the metric (slice 04).

## Wave: DISCUSS / [REF] WS strategy

**Brownfield incremental (additive).** The plugin exists; `/phil:work` is added alongside existing skills. Slice 01 is the walking skeleton — the thinnest end-to-end command — and later slices thicken it. Not the env-switching "configurable" strategy (no expansion trigger fired).

## Wave: DISCUSS / [REF] Driving ports

- **Primary:** slash command `/phil:work "<initiative>"` (CLI/skill invocation), loading `skills/work/SKILL.md`.
- Interaction port: `AskUserQuestion` + editor review for FRAME confirmation, roadmap approval, and gate decisions (mirrors `refactor-tests` human-approval port).

## Wave: DISCUSS / [REF] Pre-requisites

- Existing tactical skills: `refactor-loop`, `refactor`, `extract-method`, `review-code`, `clean-comments`, `redesign-tests`, `refactor-tests`.
- Existing rules: `refactoring`, `refactoring-catalog`, `testing`, `architecture`, `coding`.
- Shared: `skills/shared/` test-runner detection; command→skill split convention.
- **Prose-artifact patterns to reuse:** the self-test harness pattern (`skills/refactor-tests/self-test/`, `skills/redesign-tests/self-test/`) and the human-approval diff oracle (ADR-002, `refactor-tests`) — the fallback preservation oracle for prose (D9).
- No prior DISCOVER/DIVERGE wave (feature starts at DISCUSS).

## Wave: DISCUSS / [REF] DoR validation

| # | DoR item | Status | Evidence |
|---|----------|--------|----------|
| 1 | Job traceability | ✓ | All stories → `deliver-invisible-work-with-discipline` |
| 2 | Testable ACs | ✓ | ACs are end-to-end observable on real initiatives |
| 3 | Elevator pitch (real entry point + observable output) | ✓ | `/phil:work "<initiative>"` → summary output per story |
| 4 | Sliced ≤1 day w/ hypothesis | ✓ | 5 slice briefs, taste tests pass |
| 5 | Every slice has user-visible value | ✓ | No infra-only slice |
| 6 | Dependencies identified | ✓ | Per-slice dependency sections |
| 7 | Outcome KPIs w/ targets | ✓ | KPI-1..5 numeric |
| 8 | Out-of-scope explicit | ✓ | Section above |
| 9 | Requirements completeness | ✓ (0.95+) | Spine, gates, ports, docs all specified; only DESIGN-level details (doc namespace) deferred |

## Wave: DISCUSS / [REF] Wave decisions summary

- **Key decisions:** D1–D9 above.
- **Primary job:** carry invisible technical work through with nwave-grade discipline, delegating to existing tactical skills, gated by preservation floor + declared goal.
- **Walking skeleton scope:** slice 01 (frame → one delegated skill → preserve → document).
- **Feature type:** infrastructure/tooling (developer-facing); target artifacts are prose-first (skills/rules/agents/commands) — D9.
- **Constraints established:** must not re-implement tactical execution (D3); must enforce preservation via an artifact-aware oracle — executable self-test/suite or human-approval diff (D4/D9, slice 03); must off-ramp trivial work (D7); separate structural from behavior commits (repo rule).
- **Upstream changes:** none (no DISCOVER to revise).

## Wave: DISCUSS / [REF] Open questions for DESIGN

- Documentation namespace/schema: `docs/work/<initiative>/` vs. reuse `docs/feature/` (D8).
- How the orchestrator invokes tactical skills mechanically (skill-within-skill vs. agent dispatch vs. command chaining).
- Coverage-thinness detection heuristic for SAFETY-NET (slice 03 spike) — must cover prose artifacts (skills/rules/agents) that have no code coverage.
- Goal-metric taxonomy per work type (coupling, dependency count, benchmark, complexity) **and per prose work type** (self-test passing, dead-link/broken-ref checks, frontmatter validity, file-length, required-citation).
- How FRAME **selects the preservation oracle** per artifact type (executable self-test/suite vs. human-approval diff), and how EXECUTE routes prose refactors to the human-approval-based skills (`refactor-tests`/`redesign-tests`) vs. code skills.

---

## Wave: DESIGN / [REF] DDD list

- **[DDD1]** Application pattern = **modular prose skill, ports-and-adapters** — same as `refactor-tests`/`redesign-tests`. ✓
- **[DDD2]** Orchestration substrate = **hybrid** (ADR-005): a prose spine (`skills/work/SKILL.md`) owns FRAME/MAP/SAFETY-NET-setup/sequencing/VERIFY/trail; each EXECUTE wave delegates to a tactical skill and inherits its gate. Rationale: most faithful to D3 (don't re-implement execution) and D9. ✓
- **[DDD3]** EXECUTE **routing**: code → `refactor-loop` / `refactor` / `extract-method`; prose (skills/rules/agents) → `refactor-tests` / `redesign-tests`; comments → `clean-comments`; MAP survey → `review-code` / `spirit-walk` / hotspot. Routing table lives in `SKILL.md`. ✓
- **[DDD4]** Preservation oracle is **inherited from the delegate**, not re-implemented (realizes D9): code = `refactor-loop`'s deterministic suite gate; prose = `refactor-tests`/`redesign-tests` human-approval diff (ADR-002). `/phil:work` adds only the cross-wave sequencing gate: any delegate failure stops the sequence and leaves the tree last-good — never red, never a faked "done." ✓
- **[DDD5]** Documentation namespace (ADR-006, resolves D8) = `docs/work/<initiative>/` (frame, roadmap, decisions, progress) + evolution summary to `docs/evolution/<date>-<initiative>.md`. ✓
- **[DDD6]** A **self-test harness** (`skills/work/self-test/`) pins the orchestrator's safety-critical behaviors as a regression gate — mirrors `refactor-tests`/`refactor-loop`. Non-negotiable per the repo's prose-skill discipline. ✓
- **[DDD7]** **No new runtime/language** in v1 — prose spine + reused adapters. Delegates bring their own substrate (`refactor-loop`'s JS Workflow cage reused as-is). ✓
- **[DDD8]** FRAME **off-ramp** (realizes D7) is the first FRAME gate: if a single tactical skill suffices, recommend it and exit — no ceremony (answers anxiety B). ✓
- **[DDD9]** **Goal-metric taxonomy** FRAME draws from: *code* — coupling/fan-out, dependency count, cyclomatic complexity, benchmark/latency; *prose* — self-test passes, no dead links/broken skill refs, valid frontmatter, file length, required citation present. Uncheckable goal → FRAME refuses or downgrades to "behavior-preservation only." ✓

## Wave: DESIGN / [REF] Component decomposition

| Component | Path | Change type |
|---|---|---|
| Command loader | `commands/work.md` | CREATE NEW (thin loader, convention) |
| Orchestrator skill | `skills/work/SKILL.md` | CREATE NEW (FRAME·MAP·SAFETY-NET·EXECUTE·VERIFY + routing table) |
| Self-test harness | `skills/work/self-test/` | CREATE NEW (safety-behavior fixtures) |
| Trail schema | `docs/work/<initiative>/{frame,roadmap,decisions,progress}.md` | CREATE NEW (small, prose schema) |
| Evolution summary | `docs/evolution/<date>-<initiative>.md` | REUSE (existing convention) |
| Code-refactor delegate | `skills/refactor-loop` | REUSE (no change) |
| Prose-refactor delegates | `skills/refactor-tests`, `skills/redesign-tests` | REUSE (no change) |
| Simple-refactor delegates | `skills/refactor`, `skills/extract-method`, `skills/clean-comments` | REUSE (no change) |
| MAP survey delegates | `skills/review-code`, `skills/spirit-walk`, nwave hotspot | REUSE (no change) |
| Test-runner detection | `skills/shared/test-runner-detection.md` | REUSE (shared) |

## Wave: DESIGN / [REF] Driving ports

- **Primary:** `/phil:work "<initiative>"` — start a new initiative (loads `skills/work/SKILL.md`).
- **Resume:** `/phil:work` (no arg) — resume an in-flight initiative from its `docs/work/<initiative>/progress.md`.
- **Human interaction port:** `AskUserQuestion` + editor diff review — FRAME confirmation, roadmap approval, and the per-wave human-approval gate for prose (inherited from the delegates).

## Wave: DESIGN / [REF] Driven ports + adapters

| Driven port | Adapter | Notes |
|---|---|---|
| Version control | `git` via Bash | checkpoint / per-wave commit / revert — mostly performed by delegates |
| Filesystem | Read/Write/Edit | read target artifacts; write the `docs/work/` trail |
| Test execution | test runner via Bash | located via `test-runner-detection`; run by the code delegates / self-test |
| Delegation | invoke tactical skill | mechanism (slash-command vs Skill tool vs Task subagent) settled by slice-01 skeleton |
| Human approval | `AskUserQuestion` + IDE | the prose preservation oracle (ADR-002) |

## Wave: DESIGN / [REF] Technology choices

- **Skill/command:** Markdown prose (Claude Code skill), matching all existing `phil:*` skills. No new language runtime in v1.
- **Adapters:** Bash (git + test runner), `AskUserQuestion` (human port), reused `skills/shared/test-runner-detection.md`.
- **Reused substrate:** `refactor-loop`'s JS Workflow cage (`workflows/refactor-loop.js`) — invoked as a delegate, not modified.
- **Paradigm:** not applicable — the orchestrator introduces no production code. When an EXECUTE wave touches target code, it inherits the target repo's paradigm and the plugin's `coding`/`refactoring` rules via the delegate.

## Wave: DESIGN / [REF] Decisions table

| ID | Decision |
|---|---|
| DDD1 | Prose skill, ports-and-adapters |
| DDD2 | Hybrid substrate — prose spine + delegate-owned gates (ADR-005) |
| DDD3 | Per-wave routing to tactical skills |
| DDD4 | Preservation oracle inherited from delegate; only cross-wave sequencing gate is new |
| DDD5 | `docs/work/<initiative>/` + evolution to `docs/evolution/` (ADR-006) |
| DDD6 | Self-test harness as regression gate |
| DDD7 | No new runtime in v1 |
| DDD8 | FRAME off-ramp for trivial work |
| DDD9 | Goal-metric taxonomy (code + prose) |

## Wave: DESIGN / [REF] Reuse Analysis

| Existing Component | File | Overlap | Decision | Justification |
|---|---|---|---|---|
| refactor-loop | `skills/refactor-loop` | code refactor execution + deterministic gate | REUSE (delegate, no change) | its cage IS the code preservation oracle; wrapping beats rebuilding |
| refactor-tests | `skills/refactor-tests` | prose test-structure refactor + human oracle | REUSE (delegate) | carries the ADR-002 human-approval oracle (D9 prose case) |
| redesign-tests | `skills/redesign-tests` | sanctioned test-behavior rewrite + human oracle | REUSE (delegate) | prose delegate for behavior-changing test work |
| refactor | `skills/refactor` | flat-backlog interactive code refactor | REUSE (delegate) | delegate for simple code waves not needing the full loop |
| extract-method / clean-comments | `skills/extract-method`, `skills/clean-comments` | targeted structural moves | REUSE (delegate) | per-wave targeted delegates |
| review-code | `skills/review-code` | smell detection → backlog | REUSE (MAP survey delegate) | seeds the wave roadmap |
| spirit-walk | `skills/spirit-walk` | codebase comprehension | REUSE (MAP survey delegate) | survey of unfamiliar change surface |
| test-runner-detection | `skills/shared/test-runner-detection.md` | locate test runner | REUSE (shared) | baseline + gate |
| command→skill split | `commands/*.md` + `skills/*/SKILL.md` | thin-loader convention | EXTEND (follow convention) | `commands/work.md` + `skills/work/SKILL.md` follow the pattern verbatim |
| self-test harness pattern | `skills/refactor-tests/self-test/` | regression-gate fixtures | EXTEND (follow pattern) | `skills/work/self-test/` mirrors it |
| evolution summary | `docs/evolution/` | durable per-feature summary | REUSE (convention) | VERIFY writes `docs/evolution/<date>-<initiative>.md` |
| **orchestrator loop** (FRAME/MAP/sequence/VERIFY/trail) | — | none — no existing component orchestrates across waves | **CREATE NEW** | this is the feature's reason to exist; no overlap to extend |
| **trail schema** (`docs/work/<initiative>/`) | — | `docs/evolution/` covers durable summaries only | **CREATE NEW** (small) | no existing per-initiative working-trail artifact |

**Zero unjustified CREATE NEW** — both new components have no overlapping existing component to extend.

## Wave: DESIGN / [REF] Open questions (→ DISTILL / DELIVER)

- Exact delegate-invocation mechanism (run slash-command vs Skill tool vs Task subagent) — settled empirically by the slice-01 walking skeleton.
- Coverage-thinness detection for prose artifacts (slice-03 spike).
- Whether MAP's roadmap needs a DAG ledger (like `refactor-loop`) or a flat ordered list suffices — start flat, escalate on evidence.
- Resume semantics across an interrupted multi-wave run (`progress.md` as source of truth).
- Whether `docs/work/<initiative>/` is committed per wave or git-ignored while in flight (leaning committed, matching delegates' per-item commit discipline).

## Wave: DESIGN / [REF] Wave decisions summary

- **Key decisions:** DDD1–DDD9 above; ADR-005 (substrate), ADR-006 (namespace).
- **Architecture summary:** modular prose skill, ports-and-adapters; hybrid substrate — prose spine delegating to gate-owning tactical skills.
- **Paradigm:** n/a (no production code introduced).
- **Key components:** `commands/work.md`, `skills/work/SKILL.md`, `skills/work/self-test/`, `docs/work/<initiative>/` trail.
- **Constraints established:** never re-implement a delegate's gate (ADR-005); preservation enforced by the delegate; cross-wave sequencing gate leaves last-good on any delegate failure; self-test harness required (DDD6).
- **Upstream changes:** none — DESIGN honors DISCUSS D1–D9 without revision (D8 was explicitly deferred to DESIGN and is now resolved by DDD5/ADR-006).
- **Outcome collision check:** skipped — methodology/prose feature, no typed contract surface, no registry in repo.

---

## Wave: DISTILL / [REF] Scenario list with tags

Scenario SSOT: `skills/work/acceptance.feature`. Fixtures: `skills/work/self-test/`. No CI
collector — driven by human/model, exactly as `refactor/self-test/` and
`refactor-tests/self-test/`.

| Scenario | Tags | Fixture |
|---|---|---|
| Refuses an uncheckable goal | `@slice-01 @slice-04 @frame @error` | `01-frame-refuses-vague-goal` |
| Off-ramps a trivial initiative to one skill | `@slice-01 @frame @offramp` | `02-frame-offramp-trivial` |
| Carries one initiative end-to-end via a single delegate | `@slice-01 @walking_skeleton` | `03-walking-skeleton-end-to-end` |
| Routes a code wave to the gated code loop | `@slice-05 @execute @routing` | `04-route-code-to-loop` |
| Routes a prose wave to the approval cleaner | `@slice-05 @execute @routing` | `05-route-prose-to-approval` |
| A failed wave stops the sequence, leaves last-good, not done | `@slice-02 @execute @error` | `06-delegate-failure-leaves-last-good` |
| A missed goal is reported not-achieved, never done | `@slice-04 @verify @error` | `07-verify-reports-goal-not-met` |

Coverage: 4 error/honesty scenarios (`01`, `02`, `06`, `07`) = 57%, above the 40% floor; plus 2
routing-guard scenarios (`04`, `05`); only 1 pure happy path (`03`, the walking skeleton). Fixture
`06` is the safety core (silent-success-over-broken-tree class).

## Wave: DISTILL / [REF] Preservation-oracle coverage (the adapter-coverage analog)

`/phil:work` owns no preservation gate; each is inherited from the delegate (DDD4). This table is
the analog of Mandate 6's adapter coverage — every oracle path has a pinning fixture.

| Oracle path | Owner (delegate) | Pinned by |
|---|---|---|
| Code — test-suite gate | `refactor-loop` (Workflow cage) | `04-route-code-to-loop`, `03` (WS) |
| Prose — human-approval diff (ADR-002) | `refactor-tests` / `redesign-tests` | `05-route-prose-to-approval` |
| Cross-wave sequencing (the only new gate) | `phil:work` itself | `06-delegate-failure-leaves-last-good` |
| Goal-metric gate | `phil:work` FRAME + VERIFY | `01` (declare/refuse), `07` (verify honesty) |

## Wave: DISTILL / [REF] Scaffolds

**No code scaffolds (Mandate 7 N/A).** `/phil:work` is a prose skill; its "implementation" is
`commands/work.md` + `skills/work/SKILL.md`, authored in DELIVER. The RED-ready artifacts are the
self-test fixtures (situation + `expected.md` per fixture). RED-for-right-reason classification:
`docs/feature/phil-work/distill/red-classification.md` (all 7 fixtures `MISSING_FUNCTIONALITY`,
zero BROKEN).

## Wave: DISTILL / [REF] Test placement

`skills/work/acceptance.feature` + `skills/work/self-test/<NN-name>/` — colocated with the skill,
matching `skills/refactor-tests/` and `skills/redesign-tests/` precedent exactly (not `tests/…`;
this repo places a skill's acceptance harness beside the skill).

## Wave: DISTILL / [REF] Driving-adapter coverage

Single driving adapter: the `/phil:work "<initiative>"` slash command (+ no-arg resume). Exercised
end-to-end by the walking-skeleton fixture `03`. No HTTP/hook adapters. (Mechanically driven once
`SKILL.md` exists; RED until then.)

## Wave: DISTILL / [REF] Registrations skipped (methodology-only)

- **Outcomes registry** — skipped (D-6 gate-scoping): prose/methodology feature, no typed contract.
- **Polyglot state-delta port / PBT bootstrap** — skipped: no unit/PBT layer; the harness is
  decision-fixture-driven, not property-based.
- **ATDD Infrastructure Policy** — skipped: no real driven adapters to mechanize; the delegates own
  their own infra.

## Wave: DISTILL / [REF] Pre-requisites

- DESIGN driving port: `/phil:work` command (DDD driving ports).
- Delegates present in-repo: `refactor-loop`, `refactor-tests`, `redesign-tests`, `refactor`,
  `extract-method`, `clean-comments`, `review-code`, `spirit-walk`.
- No DEVOPS environment matrix (wave skipped — prose tool). No SPIKE.

## Wave: DISTILL / [REF] Wave-decision reconciliation

Read DISCUSS D1–D9 + DESIGN DDD1–DDD9. **0 contradictions** — DESIGN honored every DISCUSS decision
and resolved the one deferred item (D8 → DDD5/ADR-006). Reconciliation passed; scenarios written
against a consistent spec.
