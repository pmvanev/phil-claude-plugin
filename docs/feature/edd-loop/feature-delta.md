# Feature Delta — edd-loop (`/phil:edd`)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF|WHY|HOW]` sections. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (new job), `docs/product/personas/avery-expectation-owner.yaml`,
> `docs/product/journeys/edd-loop.yaml`.

---

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `avery-expectation-owner` — a developer who delegates building/changing to AI
  agents and evaluates the results against intent (the "author → evaluator" shift EDD describes).
- **JTBD one-liner:** *Prove that AI-produced work meets my real intent — including the qualitative
  parts no test cheaply asserts — with executed evidence I adjudicate, without adding ceremony where
  my existing engines already prove the checkable parts.*
- **Job ID:** `prove-qualitative-expectations-with-evidence` (new; distinct from phil:work's
  `deliver-invisible-work-with-discipline` — that job preserves behavior, this one proves a
  qualitative expectation).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** Developer-tool / user-facing — the "user" is a developer invoking `/phil:edd`;
  the command has a real entry point and observable output (satisfies the Elevator Pitch test).
- **Lineage:** the expectation-driven sibling to `phil:work`. Same **general-contractor** pattern:
  delegate the build → **inherit the delegate's oracle** (ADR-005) → add exactly the **one gate the
  engine structurally lacks** (here: the qualitative-evidence gate) → leave a trail. `phil:work` is
  the contractor for *invisible* work; `phil:edd` is the contractor for *expectation-driven* work,
  delegating to **both** nwave (user-facing) and `phil:work` (invisible).

## Wave: DISCUSS / [REF] Locked decisions

The 5 DISCUSS open questions, resolved. (Factoring items flagged `→ DESIGN` are surfaced here as
requirements, decided in DESIGN.)

- **[D1] Triage rule — what is "engine-checkable" vs "qualitative".**
  An expectation is **engine-checkable** iff the target engine's *native oracle* can produce a
  pass/fail executed result for it at reasonable cost: nwave → an acceptance test can assert it
  (deterministic observable output); `phil:work` → it's a checkable metric (coupling/complexity/
  benchmark, dead-link/frontmatter/citation check). It is **qualitative** only when asserting it
  would require encoding a subjective judgment (helpful, clear, ergonomic, aesthetic).
  **Honesty rule / bias-to-off-ramp:** default every expectation to engine-checkable; mark
  qualitative **only** when the developer confirms a *concrete* reason it can't be cheaply
  asserted. Evidence ceremony is opt-in, never the default.

- **[D2] What "executed evidence" must be (vs narration).**
  Evidence must be a raw artifact produced by *actually running or rendering* something, captured
  **verbatim**, accompanied by the **command/procedure that reproduces it**. Acceptable: a captured
  real-run transcript, the actual emitted output text, a rendered document, a demo/e2e log.
  **Rejected as narration:** any description, summary, or claim ("I checked, it's fine") lacking the
  raw artifact, or evidence that cannot be re-run/re-observed. Rule of thumb: *if the human can't
  re-produce it from what's recorded, it's narration.*

- **[D3] Gate factoring — shared skill vs inlined. → DESIGN.**
  Requirement surfaced now: the evidence-gate logic must be **encapsulated so it could be shared**
  by `phil:work` VERIFY and nwave DELIVER/VERIFY, and must preserve separation of powers. Whether it
  is *physically extracted* into a shared skill or inlined in `phil:edd` for v1 is a DESIGN decision
  (ADR-worthy, alongside ADR-005's delegation principle).

- **[D4] Who adjudicates qualitative evidence.**
  The **human is the final adjudicator** of every qualitative expectation (mirrors redesign-tests'
  ADR-004 human-validated claim and phil:work's prose human-diff oracle). An **independent
  producer/critic agent** gathers or pre-screens the evidence but does **not** get the final say.
  **Separation of powers (mandatory):** the evidence-producer must be a **different agent than the
  builder**. An *automated* independent verdict is a deferred enhancement (advisory pre-screen seam),
  not v1.

- **[D5] Living-documentation output & namespace. → DESIGN (namespace ADR).**
  Working trail at **`docs/edd/<slug>/`**: `expectations.md` (each expectation + classification +
  routing), `evidence/` (the captured executed artifacts), `verdicts.md` (per-expectation human
  verdict + timestamp). A durable **evolution summary** migrates to `docs/evolution/<date>-<slug>.md`
  (reuses the ADR-006 pattern). **No trail is written for an off-ramp-only run** (no ceremony).

## Wave: DISCUSS / [REF] User stories

### Story 1 — Triage & honest off-ramp *(slice 01, walking skeleton)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I run `/phil:edd` with my intent so it captures my expectations, classifies each,
and — when they're all engine-checkable — tells me honestly to run nwave/`phil:work` directly and
exits, adding no ceremony.

**### Elevator Pitch**
Before: I either wrap all AI-built work in an evidence process or just trust the AI's narration.
After: run `/phil:edd "<intent>"` → sees a classification table + `OFF-RAMP: all expectations are
engine-checkable — run /phil:work "<…>" (or /nw-…); phil:edd would only add ceremony.` then exits.
Decision enabled: I use the right engine directly, confident nothing qualitative was silently dropped.

**Acceptance criteria**
- AC1.1 — Given an intent whose expectations are all engine-checkable, when I run `/phil:edd`, then
  it prints a classification table (row = expectation → engine + native oracle), recommends the
  specific engine command, and exits **without** creating any `docs/edd/<slug>/` trail.
- AC1.2 — Given an ambiguous expectation, then it defaults to engine-checkable and asks me to
  confirm before marking anything qualitative.
- AC1.3 — Given a would-be qualitative expectation with no stated concrete reason it resists cheap
  assertion, then it is treated as engine-checkable (no unjustified ceremony).

### Story 2 — Single-engine qualitative-evidence gate *(slice 02)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, when some expectations are genuinely qualitative, `/phil:edd` delegates the build to
one engine and attaches a scaled executed-evidence gate to the qualitative residue, so I adjudicate
real evidence instead of trusting narration.

**### Elevator Pitch**
Before: qualitative intent ("errors are helpful") gets dropped by tests or accepted on the AI's word.
After: run `/phil:edd "<intent>"` → after the engine builds, sees `EVIDENCE — 'error messages are
helpful': <verbatim captured CLI transcript of the actual error outputs> [reproduce: <command>]` and
an accept/reject prompt. Decision enabled: I adjudicate the qualitative expectation on executed
evidence, and my verdict is recorded.

**Acceptance criteria**
- AC2.1 — Given a qualitative expectation and an engine that already produced relevant executed
  evidence, when the gate runs, then it points me at the existing artifact (no new commission) and
  asks me to adjudicate.
- AC2.2 — Given a qualitative expectation with no existing evidence, when the gate runs, then it
  commissions a NEW executed artifact produced by a **non-builder** agent, captured verbatim with
  the reproducing command, and presents it for adjudication.
- AC2.3 — Given "evidence" that is narration (no raw artifact / not reproducible), when validated,
  then it is rejected and re-commissioned — narration never satisfies the gate.
- AC2.4 — Given the build and the evidence, then the evidence-producer is a different agent than the
  builder (separation of powers), and the human is the final adjudicator.
- AC2.5 — Given I reject a qualitative expectation, then "done" is blocked, the expectation
  iterates, and the run is never reported as done with an outstanding rejection.

### Story 3 — Expectations & evidence as living documentation *(slice 02)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, when the loop finishes, my captured expectations + their executed evidence + my
verdicts persist as living documentation, so intent and proof outlive the session.

**### Elevator Pitch**
Before: qualitative intent and its proof live only in a chat transcript that evaporates.
After: run `/phil:edd` → on completion sees `Wrote docs/edd/<slug>/{expectations.md, evidence/,
verdicts.md}; evolution summary → docs/evolution/2026-07-15-<slug>.md`. Decision enabled: I (and
teammates) can later see what was expected, what evidence proved it, and my verdict.

**Acceptance criteria**
- AC3.1 — Given a completed run with ≥1 adjudicated qualitative expectation, then `docs/edd/<slug>/`
  contains `expectations.md`, the evidence artifacts, and `verdicts.md` (verdict + timestamp per
  expectation).
- AC3.2 — Given an off-ramp-only run (Story 1), then NO trail is created beyond the recommendation —
  living docs exist only when the gate ran.
- AC3.3 — Given completion, then a durable evolution summary is written to
  `docs/evolution/<date>-<slug>.md` reusing the plugin convention.

## Wave: DISCUSS / [REF] Outcome KPIs

Measured against self-test fixtures (mirrors phil:work's self-test-as-regression-gate approach).

| KPI | Target | Measurement |
|---|---|---|
| Off-ramp correctness | 100% of fully-checkable fixtures off-ramp; 0 false gates | fixture asserts exit + zero trail files |
| Narration rejection | 100% of narrated-evidence fixtures rejected | fixture asserts re-commission |
| Separation of powers | builder ≠ evidence-producer in 100% of gated runs | structural assertion in fixture |
| Zero-ceremony off-ramp | off-ramp run writes 0 trail files | file count == 0 |
| No false "done" | 0 runs reported done with a rejected/outstanding qualitative expectation | fixture asserts blocked-done |

## Wave: DISCUSS / [REF] Out of scope (v1)

- Cross-domain multi-initiative sequencing + seam-level/end-to-end expectations (slice 03, deferred).
- An automated independent-critic *verdict* on qualitative evidence (human remains final adjudicator;
  advisory pre-screen is a reserved seam).
- Physically extracting the evidence gate into a shared skill (DESIGN decides — D3).
- Any modification of nwave or phil:work internals — `phil:edd` composes them unchanged.

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:edd "<intent>"` slash command (+ no-arg **resume** of an in-flight loop,
  mirroring phil:work). Command→skill split per plugin convention.
- **Prerequisites / reuse:** nwave present; `phil:work` present (off-ramp/build targets);
  ADR-002 human-approval port; ADR-004 human-validated-claim (redesign-tests); refactor-loop's
  independent-critic pattern; ADR-005 delegation-with-inherited-oracle; ADR-006 doc-namespace pattern.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Strategy **A** — thinnest end-to-end slice: slice 01 (capture → classify → off-ramp) is a complete,
shippable, end-to-end command invocation on a real repo. The qualitative gate (slice 02) extends the
same skeleton's qualitative branch. This is exactly how `phil-work` sequenced (walking skeleton first,
then breadth).

## Wave: DISCUSS / [REF] Definition of Done (9-item)

1. `/phil:edd` command + skill exist and load (command→skill split).
2. Every story traces to `job_id: prove-qualitative-expectations-with-evidence` (in SSOT).
3. Every non-`@infrastructure` story has a complete Elevator Pitch with a real entry point.
4. Every AC is testable and verifies the Elevator Pitch's "After" end-to-end.
5. Off-ramp writes zero trail (KPI: zero-ceremony) — proven by fixture.
6. Evidence gate rejects narration and enforces builder ≠ evidence-producer — proven by fixtures.
7. Human is the final adjudicator; a rejected qualitative expectation blocks done — proven by fixture.
8. Living-doc trail + evolution summary written only when the gate ran.
9. Self-test fixtures pin the above and run as a regression gate (mirrors phil:work self-test).

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | new job in `jobs.yaml`; all 3 stories carry the `job_id` |
| 2 | Persona defined | ✅ | `personas/avery-expectation-owner.yaml` |
| 3 | Journey mapped | ✅ | `journeys/edd-loop.yaml` (happy path + error paths) |
| 4 | Stories have elevator pitches | ✅ | all 3 stories, real `/phil:edd` entry point + observable output |
| 5 | ACs testable | ✅ | Given-When-Then, fixture-checkable |
| 6 | Slices ≤1 day, learning hypothesis each | ✅ | `slices/slice-01`, `slice-02` (03 deferred) |
| 7 | Walking skeleton identified | ✅ | slice 01 = triage + off-ramp, end-to-end |
| 8 | Outcome KPIs with targets | ✅ | KPI table above, fixture-measured |
| 9 | Scope right-sized / split confirmed | ✅ | v1 = slices 01–02; slice 03 explicitly deferred |

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** v1 is 3 stories across 2 thin slices; slice 03 (cross-domain sequencing) is
split off and deferred. No oversized signals (≤10 stories, 2 engines composed not modified,
skeleton needs ≤2 integration points: nwave + phil:work as off-ramp targets).

---

## Wave: DISCUSS / [REF] Decisions summary (for DESIGN)

- **Key decisions:** D1 triage/bias-to-off-ramp · D2 executed-evidence-vs-narration · D3 gate
  factoring (→ DESIGN) · D4 human final adjudicator + separation of powers · D5 living-doc namespace
  `docs/edd/<slug>/` (→ DESIGN ADR).
- **Requirements summary:** `/phil:edd` is a thin triage front-door that off-ramps to nwave/phil:work
  when expectations are engine-checkable and attaches a scaled executed-evidence gate (human-adjudicated,
  builder≠producer) only to the qualitative residue, persisting expectations+evidence+verdicts as living docs.
- **Feature type:** developer-tool / user-facing.
- **Constraints:** compose nwave + phil:work **unchanged** (ADR-005 lineage); no re-implemented
  preservation gate; off-ramp is mandatory when fully checkable; evidence must be executed, never narrated.
- **Upstream changes:** none — DISCOVER/DIVERGE intentionally skipped (concept pre-validated by the
  EDD article); no prior-wave assumptions contradicted.

## Wave: DISCUSS / [REF] Handoff

**To:** DESIGN (nw-solution-architect) — decide D3 (gate: shared skill vs inlined) + D5 (namespace ADR),
component decomposition, and reuse boundaries against refactor-loop/redesign-tests/phil-work.
**Deliverables:** this feature-delta + `journeys/edd-loop.yaml` + `jobs.yaml` job + slice briefs + KPIs.

---

## Wave: DESIGN / [REF] Scope, mode & paradigm

- **Design scope:** Application / components (nw-solution-architect lens). Not system-scope (no
  distributed concerns) and not domain-scope (no new bounded context/aggregates — the concepts
  "expectation / evidence / verdict" are lightweight prose-skill vocabulary, not a domain model).
- **Interaction mode:** propose (options + trade-offs; the D3 fork was decided by the developer).
- **Paradigm:** N/A in the programming sense — the artifact is a **prose skill** (Markdown), like
  `work`/`refactor-tests`. The relevant choice is the **substrate** (ADR-007), not FP vs OOP. No
  `CLAUDE.md` paradigm line is written.

## Wave: DESIGN / [REF] Design decisions (DDD)

- **[DDD1] Substrate = prose spine + delegated build + evidence-producer subagent (ADR-007).**
  Rejected a Workflow cage (interactive flow + human oracle fight a headless cage; most new
  mechanism) — same reasoning as ADR-005. Separation of powers is supplied by a distinct subagent,
  not the cage.
- **[DDD2] Build is delegated, oracle inherited (ADR-007 / ADR-005 lineage).** `/phil:edd` never
  re-verifies engine-checkable expectations; nwave's AT run and `phil:work`'s preservation+goal
  gates are the oracle for those. Only the qualitative residue gets the new gate.
- **[DDD3] Gate inlined with an extraction seam (ADR-008 — resolves D3).** Self-contained block in
  `skills/edd/SKILL.md` with contract `{expectation, engine_evidence?} → {verdict, artifact,
  trail}`. Not a shared skill in v1 (one consumer); `phil:work`/nwave unchanged.
- **[DDD4] Separation of powers is structural (ADR-007 — D4).** A dedicated non-builder
  `agents/edd-evidence-producer.md` runs/renders and captures verbatim; the **human** is the final
  adjudicator (ADR-002 port). Automated evidence critic deferred behind a seam (ADR-002/004 style).
- **[DDD5] Evidence contract (D2).** Executed artifact + reproducing command, captured verbatim;
  narration (no reproducible artifact) is rejected and re-commissioned.
- **[DDD6] Trail namespace `docs/edd/<slug>/`, gate-ran only (ADR-009 — resolves D5).** Off-ramp
  runs leave no trail (zero-ceremony KPI observable as a filesystem fact).
- **[DDD7] Self-test harness pins safety behaviors.** `skills/edd/self-test/` fixtures (off-ramp
  zero-trail, narration rejection, builder≠producer, blocked-done) are the regression gate, as in
  `work`/`refactor-tests`/`refactor-loop`.
- **[DDD8] Build-time substrate = prose authoring, not code TDD; agents forged-then-trimmed.**
  This is a Claude Code extension: the "implementation" is prose artifacts (command, skill, agent),
  and the "tests" are Gherkin acceptance scenarios + self-test fixtures — NOT production/unit code.
  DELIVER authors prose to satisfy those fixtures (the `phil-work` model: `roadmap.json` steps whose
  criteria are fixtures reached against `acceptance.feature`), not a code RED→GREEN cycle. New
  **agents** are authored **hybrid**: draft + validate via `nw-agent-builder` / `nw-forge`, then trim
  to the plugin's lean ~110-line convention (matching `refactor-proposer` / `refactor-critic-
  correctness`: `model: inherit`, tight tools). The **command + skill** are hand-authored following
  the established command→skill split (the `refactor-tests` / `work` precedent). See the build-time
  section below.

## Wave: DESIGN / [REF] Component decomposition

| Component | Path | Change |
|---|---|---|
| Command loader | `commands/edd.md` | CREATE NEW (thin loader, per command→skill split) |
| Orchestrator spine | `skills/edd/SKILL.md` | CREATE NEW (CAPTURE·CLASSIFY·OFF-RAMP·BUILD·EVIDENCE-GATE·ADJUDICATE·DOCUMENT) |
| Evidence gate | `skills/edd/SKILL.md` `## Evidence Gate` section | CREATE NEW (inlined, ADR-008 contract + seam) |
| Evidence producer | `agents/edd-evidence-producer.md` | CREATE NEW (independent, non-builder; runs/renders, captures verbatim) |
| Evidence critic | `agents/edd-evidence-critic.md` | DEFERRED (advisory executed-vs-narration pre-screen; seam only) |
| Self-test fixtures | `skills/edd/self-test/` | CREATE NEW (regression gate) |

## Wave: DESIGN / [REF] Build-time substrate & authoring tooling (DDD8)

This is a **Claude Code extension** — there is little/no production or unit-test *code*. The build
surface is prose artifacts, and the acceptance surface is executable-in-spirit fixtures. DESIGN
records how each artifact is produced so DELIVER routes correctly.

| Artifact | Authoring approach | Precedent |
|---|---|---|
| `commands/edd.md` | Hand-author (thin loader; command→skill split) | `commands/work.md`, `commands/refactor-tests.md` |
| `skills/edd/SKILL.md` (+ inlined gate) | Hand-author prose; slice-by-slice to satisfy fixtures | `skills/work/SKILL.md` |
| `agents/edd-evidence-producer.md` | **Hybrid** — draft/validate via `nw-agent-builder`/`nw-forge`, then **trim to the lean ~110-line convention** | `agents/refactor-proposer.md` (~112 ln), `agents/refactor-critic-correctness.md` (~107 ln) |
| `agents/edd-evidence-critic.md` (deferred) | Same hybrid, when built | same |
| `skills/edd/self-test/` + `acceptance.feature` | Authored in DISTILL (acceptance-designer) as Gherkin scenarios + fixtures | `skills/work/self-test/`, `skills/work/acceptance.feature` |

**DELIVER flow (prose-adapted, not code TDD).** "GREEN" for a step = the step's self-test
fixture reaches its **expected decision** and the human-approval oracle passes — mirroring
`phil-work`'s `roadmap.json`, whose step `criteria` are *"Fixture NN reaches <STATE>"* against
`test_file: skills/edd/acceptance.feature`. There is no RED→GREEN production-code cycle; the
software-crafter's role is **prose authoring gated by fixtures**, and the agent(s) are forged via
the agent-building tooling. DELIVER routing must reflect this — do **not** dispatch a code-TDD
crafter expecting to write and green unit tests.

## Wave: DESIGN / [REF] Driving & driven ports

- **Driving port:** `/phil:edd "<intent>"` (+ no-arg **resume** of an in-flight loop, mirroring
  `phil:work`). Command→skill split.
- **Driven ports & adapters:**
  | Driven port | Adapter | Notes |
  |---|---|---|
  | Build delegation (user-facing) | nwave skills | inherit AT oracle (DDD2) |
  | Build delegation (invisible) | `/phil:work` | inherit preservation+goal oracle (DDD2) |
  | Evidence commission | `agents/edd-evidence-producer.md` via Agent/Task | producer ≠ builder (DDD4); mechanism settled in slice 01 |
  | Suite execution (evidence) | `skills/shared/test-runner-detection.md` + Bash | REUSE, only when evidence needs a run |
  | Human adjudication | AskUserQuestion + IDE review | ADR-002 port (DDD4) |
  | Trail persistence | filesystem + git → `docs/edd/<slug>/`, `docs/evolution/` | ADR-009 (DDD6) |

## Wave: DESIGN / [REF] Reuse Analysis

| Existing component | File | Overlap | Decision | Justification |
|---|---|---|---|---|
| phil:work orchestrator spine | `skills/work/SKILL.md` | FRAME/off-ramp/trail/sequencing shape | **EXTEND (pattern-copy)** | Same contractor shape; pattern-copy as `redesign-tests` did `refactor-tests` (ADR-003 Option A). A shared spine has one consumer each — extraction is premature. |
| nwave (DISCUSS…DELIVER) | nwave skills | the BUILD for user-facing expectations | **REUSE (unchanged)** | Delegate + inherit AT oracle (ADR-005 lineage). |
| phil:work | `commands/work.md`, `skills/work/` | the BUILD for invisible expectations | **REUSE (unchanged)** | Delegate + inherit preservation+goal oracle. |
| Human-approval port | ADR-002 (AskUserQuestion + IDE) | adjudication UX | **REUSE** | D4 human adjudicator = the same port. |
| Coverage-equivalence-claim pattern | ADR-004 / `redesign-tests` | "human validates a claim, not just a diff" | **EXTEND (analogous claim)** | Here the human validates "this executed evidence meets the qualitative expectation" — same claim-at-the-gate shape. |
| Independent-critic agent pair | `agents/refactor-proposer.md`, `agents/refactor-critic-correctness.md` | separation of powers (judge ≠ author) | **EXTEND (copy pattern, not the cage)** | Copy the independent-agent pattern (producer ≠ builder); the Workflow cage is rejected (DDD1). |
| Doc namespace | ADR-006 `docs/work/` + `docs/evolution/` | trail location | **CREATE NEW (`docs/edd/`)** | Sibling namespace; reusing `docs/work/` conflates preservation initiatives with expectation loops (ADR-009). |
| Test-runner detection | `skills/shared/test-runner-detection.md` | running a suite to produce evidence | **REUSE** | When evidence commission runs tests. |
| Self-test harness convention | `skills/work/self-test/` etc. | regression gate for a prose skill | **EXTEND (same convention)** | New fixtures under `skills/edd/self-test/`. |

**Genuinely NEW (no existing component covers it):** the triage/classify front-door (D1), the
scaled qualitative-evidence gate (ADR-008), and the `edd-evidence-producer` agent (DDD4). Everything
else is REUSE or pattern-copy.

## Wave: DESIGN / [REF] Decisions table

| ID | Decision | ADR |
|---|---|---|
| DDD1 | Prose spine + delegated build + evidence-producer subagent | ADR-007 |
| DDD2 | Build delegated; engine oracle inherited (no re-verification) | ADR-007 |
| DDD3 | Evidence gate inlined with extraction seam (D3) | ADR-008 |
| DDD4 | Separation of powers structural; human final adjudicator (D4) | ADR-007 |
| DDD5 | Executed-evidence-vs-narration contract (D2) | ADR-007 |
| DDD6 | Trail `docs/edd/<slug>/`, gate-ran only (D5) | ADR-009 |
| DDD7 | Self-test fixtures as regression gate | — |
| DDD8 | Build-time = prose authoring (not code TDD); agents forged-then-trimmed to lean convention | — |

## Wave: DESIGN / [REF] Open questions (→ DISTILL / DELIVER)

- Evidence-producer **invocation mechanism** (Agent vs Task) and the engine-build invocation —
  settled empirically by the slice-01 walking skeleton (ADR-007 open item).
- Whether `docs/edd/<slug>/` is git-ignored in flight or committed per adjudication (ADR-009 open
  item; leaning committed).
- Promotion of the inlined gate to `skills/shared/qualitative-evidence-gate.md` once a second
  consumer (`phil:work` FRAME / nwave VERIFY) exists (ADR-008 open item; post-v1).
- The **advisory evidence critic** (`agents/edd-evidence-critic.md`) — deferred; the gate reserves
  a clean pre-screen seam (ADR-002/004 precedent).

## Wave: DESIGN / [REF] Outcome Collision Check

**Skipped — methodology/prose feature.** `/phil:edd` adds no new typed code contract surface (it is
a prose orchestrator skill composing existing engines); per the outcomes-registry gate-scoping
(code-feature pipelines only), the collision check does not apply. Reuse Analysis above covers
in-codebase deduplication.

## Wave: DESIGN / [REF] Decisions summary (for DEVOPS / DISTILL)

- **Pattern:** modular monolith prose skill, ports-and-adapters; prose spine + delegated build +
  inherited oracle + inlined evidence gate + non-builder evidence-producer subagent + human
  adjudication.
- **Paradigm:** N/A (prose skill).
- **Key components:** `commands/edd.md`, `skills/edd/SKILL.md` (+ inlined gate),
  `agents/edd-evidence-producer.md`, `skills/edd/self-test/`.
- **Constraints:** compose nwave + `phil:work` **unchanged**; never re-verify inherited oracles;
  off-ramp mandatory when fully checkable (zero trail); evidence executed-not-narrated;
  producer ≠ builder; human is final adjudicator.
- **New ADRs:** ADR-007 (substrate), ADR-008 (gate factoring — D3), ADR-009 (namespace — D5).
- **Upstream changes:** none — no DISCUSS assumption contradicted.

## Wave: DESIGN / [REF] Handoff

**To:** DEVOPS (nw-platform-architect) then DISTILL (acceptance-designer). DISTILL turns the
DISCUSS ACs + these DESIGN decisions into executable acceptance scenarios (the `skills/edd/self-test/`
fixtures + `acceptance.feature`), mirroring how `phil-work` was distilled.
**Deliverables:** this feature-delta (DISCUSS+DESIGN) + ADR-007/008/009 + updated
`docs/product/architecture/brief.md` (edd-loop section + C4).

**DELIVER routing note (DDD8):** this is a prose-artifact feature. DELIVER authors prose
(command/skill hand-authored; agents forged-then-trimmed via `nw-agent-builder`/`nw-forge`) gated
by the DISTILL fixtures — **not** a code RED→GREEN cycle. The roadmap's step criteria are
"Fixture NN reaches <STATE>" against `skills/edd/acceptance.feature`, exactly as `phil-work`'s
`roadmap.json` was shaped.
