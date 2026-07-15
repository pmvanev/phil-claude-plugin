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
