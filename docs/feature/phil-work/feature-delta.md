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
