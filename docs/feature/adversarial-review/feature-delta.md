# Feature Delta — adversarial-review

Single narrative file for the `adversarial-review` feature. DISCUSS Tier-1 `[REF]` sections below;
DESIGN / DISTILL / DELIVER append their own `## Wave:` sections as the feature advances.

---

## Wave: DISCUSS / [REF] Persona

**Rowan — the skeptical delegator/shipper** (`docs/product/personas/rowan-skeptical-delegator.yaml`).
Does work, or delegates it to AI agents, and at the moment of trusting / shipping / marking-done
wants an *independent adversary* to try to break it first. Sibling to Avery (edd): Avery wants
executed evidence handed over so she adjudicates; Rowan wants the *critique itself* performed by a
non-builder.

## Wave: DISCUSS / [REF] JTBD one-liner

`get-independent-adversarial-critique-of-completed-work` — *When I (or an AI agent I delegated to)
have just completed a task and I'm about to trust/ship/call-it-done, I want an independent adversary
to actively try to falsify "done" — splitting hard-checkable from judgment-call, attacking against
my intent and standards, and handing me ranked evidence-bearing findings — so I can catch the flaws
the builder rationalized past, without trusting the builder's self-assessment or reading every line.*

Registered in `docs/product/jobs.yaml`; full dimensions + four forces there.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1] New sibling job, new persona, new journey** (not an extension of edd's job). edd *produces
  evidence for a human to judge*; adversarial-review *does the judging* — a distinct outcome.
- **[D2] Feature type: cross-cutting.** A command + reviewer agent that runs standalone *and*
  composes into `phil:work` / `phil:edd` / `phil:refactor-tests` and ad-hoc workflows.
- **[D3] Walking skeleton: yes.** Thinnest end-to-end slice = standalone adversarial-review of a
  just-completed task.
- **[D4] Research depth: lightweight** (happy path + key error paths).
- **[D5] Intent source is dual:** the host passes intent when composed; it is inferred from the
  conversation/context leading up to the invocation when standalone.
- **[D6] Typed, advisory verdict.** The verdict is a typed schema (like `refactor-critic-correctness`'s
  JSON) so a host can gate on it programmatically; it is always advisory — the reviewer never
  self-adjudicates.

### Load-bearing constraints (C1–C5) — the design is built against soft-critic theatre

Informed by `docs/research-summaries/tri-agent-clarification/` (three-role split, reason-before-verdict,
adversarial persona, author-then-ablate self-tests) and its LLM-Modulo/ABC warnings (a loop is only
as sound as its hardest critic; correlated errors from same-model judging; an unvalidated judge is a
promissory note):

- **C1 INDEPENDENCE.** The reviewer runs in fresh context and is never given the builder's reasoning
  trace (correlated-error avoidance). The orchestrator curates what it sees: artifact + intent +
  standards only. Different-model hardening is deferred to DESIGN.
- **C2 HARD/SOFT SPLIT.** Every review partitions findings into hard-checkable (run the check, or
  inherit the host's oracle — ADR-005 lineage, never re-implement) vs soft (adversarial, labeled).
- **C3 ADVISORY, NEVER SELF-ADJUDICATING.** Findings are input the host command or human gates on;
  the reviewer never declares done.
- **C4 HONESTY LABEL.** When no oracle backs the hard findings, the review is labeled a soft DRAFT
  SIGNAL, never dressed as a sound gate. This is to adversarial-review what the off-ramp is to edd
  and the two-gate spine is to phil:work — the discipline that stops it becoming the theatre it
  exists to prevent (anxiety A).
- **C5 SPAN-AND-EVIDENCE / ANTI-FLATTERY.** No finding without a span + evidence; empty praise is
  coerced to `CANNOT_ASSESS`. Carried verbatim from `refactor-critic-correctness`.

## Wave: DISCUSS / [REF] Driving ports

- **CLI / skill:** `/phil:adversarial-review [target] [--intent "..."]` (standalone).
- **Composition:** invoked by `phil:work` (a review wave / VERIFY input), `phil:edd` (generalizes the
  deferred `edd-evidence-critic` pre-screen), `phil:refactor-tests` (adversarial pre-screen of a diff),
  and ad-hoc Workflow-tool scripts — all consuming the typed advisory verdict.

## Wave: DISCUSS / [REF] Out-of-scope (v1)

- Owning any gate/guard itself — it is advisory only (C3); hosts and humans gate.
- Re-implementing a preservation/behavior oracle — it inherits the host's (ADR-005 lineage).
- Different-model / multi-lens reviewer hardening — a DESIGN decision, not fixed in DISCUSS.
- Fixing or applying findings — it reviews; it does not edit.

## Wave: DISCUSS / [REF] Pre-requisites

- Ecosystem patterns to reuse: `agents/refactor-critic-correctness.md` (verdict schema,
  reason-before-verdict, anti-flattery), `refactor-loop`'s GUARD (severity threshold θ, ranking),
  `skills/shared/test-runner-detection.md` (oracle detection for code targets), ADR-002 (human port),
  ADR-005 (inherit-don't-reimplement oracle lineage).

## Wave: DISCUSS / [REF] Relationship map

| Neighbor | Relationship |
|---|---|
| `edd` (`edd-evidence-critic`, deferred) | adversarial-review is the **general-purpose form** of that narrow pre-screen critic |
| `refactor-loop` (`refactor-critic-correctness`) | adversarial-review **generalizes** it out from behind its test-suite oracle |
| `phil:work` | a **candidate delegate** — a review wave / VERIFY-time adversarial input |
| `refactor-tests` / `redesign-tests` | a **pre-screen** consumer ahead of the human diff gate |

## Wave: DISCUSS / [REF] User stories

Each story traces to `get-independent-adversarial-critique-of-completed-work`.

### US-1 — Standalone honest soft review (slice 01, walking skeleton)
As Rowan, I can point adversarial-review at a just-completed no-oracle artifact and get an
independent, ranked, evidence-bearing critique that is honestly labeled a draft signal.

**### Elevator Pitch**
Before: I just wrote a skill/doc and my only check is the builder's own "looks good to me".
After: run `/phil:adversarial-review skills/foo/SKILL.md` → sees a ranked findings verdict, each with
a span + evidence, labeled `draft-signal (no oracle)`.
Decision enabled: I decide which findings to fix before I trust/ship it — on an independent read, not
self-assessment.

- AC1: verdict overall label is `draft-signal` for a no-oracle target.
- AC2: every finding carries a span + evidence; unsupportable praise is `CANNOT_ASSESS` (C5).
- AC3: no done/not-done adjudication anywhere in the output (C3).

### US-2 — Hard/soft split on a code target (slice 02)
As Rowan, on a code target with a test suite I get a verdict that separates hard-checked findings
(backed by the actual suite result) from soft adversarial ones, labeled a sound gate.

**### Elevator Pitch**
Before: an adversarial review of code can't tell me what's *proven* wrong vs *argued* wrong.
After: run `/phil:adversarial-review --changes` → sees findings each tagged `hard`/`soft`, hard ones
citing the real check result, verdict labeled `sound-gate`.
Decision enabled: I trust the hard findings as verified and weigh the soft ones as judgment.

- AC1: findings tagged `hard`/`soft`; verdict labeled `sound-gate` when a runner is detected.
- AC2: hard findings cite the actual check result, not a prediction.
- AC3: no detectable oracle → degrades to `draft-signal` (C4 regression guard).

### US-3 — A host gates on the verdict (slice 03)
As Rowan, when I run `phil:work` on a prose initiative, its review wave consumes adversarial-review's
typed verdict and routes on it without re-judging.

**### Elevator Pitch**
Before: phil:work's non-test-prose wave has only a raw human-approval diff — no adversarial pre-screen.
After: run `/phil:work "<prose initiative>"` → the review wave shows `adversarial-review: 2 major
findings (draft-signal)` and phil:work routes on the typed verdict.
Decision enabled: I see an independent adversarial read folded into phil:work's gate, deciding
whether the wave proceeds.

- AC1: the host routes using only typed fields (severity, label) — no re-judging (composability proof).
- AC2: a `draft-signal` verdict is never consumed as a passed sound gate (C4 at the boundary).
- AC3: reviewer output is identical standalone vs host-invoked (no special-casing).

## Wave: DISCUSS / [REF] Outcome KPIs

- **KPI-1 (signal):** ≥1 acted-on finding per review that the builder's self-assessment missed,
  on real dogfood targets. Measure: dogfood log of findings → fixes. Target: >0 on each of the 3
  slice dogfood runs.
- **KPI-2 (anti-theatre, hard gate):** 0 reviews where a no-oracle target is labeled `sound-gate`.
  Measure: self-test fixture asserting the label; target: 100% correct labeling (C4).
- **KPI-3 (independence):** 100% of dispatches exclude the builder reasoning trace. Measure:
  self-test on the dispatch contract (C1).
- **KPI-4 (composability):** host routes on the verdict with 0 re-judging steps. Measure: slice-03
  AC1; target: pass.

## Wave: DISCUSS / [REF] Definition of Done (9-item)

1. Command + skill + reviewer agent shipped for slice 01. 2. Typed verdict schema documented.
3. Honesty label (`draft-signal`/`sound-gate`) implemented + self-tested (C4). 4. Independence
curation self-tested (C1). 5. Anti-flattery `CANNOT_ASSESS` coercion self-tested (C5). 6. Advisory
— no self-adjudication anywhere (C3). 7. Self-test golden fixtures (author-then-ablate: deliberately
flawed completed tasks the reviewer must catch). 8. `acceptance.feature` + wave-decisions written.
9. Evolution summary at completion.

## Wave: DISCUSS / [REF] Definition of Ready — validation

- Job traceable ✓ (`get-independent-adversarial-critique-of-completed-work`).
- Persona ✓ (Rowan). Journey ✓ (`adversarial-review.yaml`). Slices ✓ (01–03, briefs written).
- Every story has an Elevator Pitch with a real entry point + observable output ✓.
- ACs testable ✓. Constraints C1–C5 locked ✓. KPIs have numeric/boolean targets ✓.
- Out-of-scope explicit ✓. WS identified (slice 01) ✓.
- Open items handed to DESIGN: different-model/multi-lens hardening (C1 strengthening); verdict
  schema detail; oracle types beyond test-suite; substrate (prose spine vs Workflow cage).

---

## Wave: DESIGN / [REF] DDD list

- **[DDD1] Substrate: prose spine + Task-dispatched reviewer subagent** (not a Workflow cage).
  Single dispatch→verdict, advisory (C3) — no loop/gate to make deterministic. (ADR-010)
- **[DDD2] Reusable unit = `agents/adversarial-reviewer.md`.** One agent, invoked by the standalone
  skill and any future host/workflow, all reading the same typed verdict. The skill is the
  standalone driver; the agent is the composition unit. (ADR-010)
- **[DDD3] Verdict schema pattern-copies `refactor-critic-correctness`**, generalized: `justification`
  first, `findings[]` with `severity/confidence/span/evidence/mechanism`, `CANNOT_ASSESS` coercion;
  +`overall_label: sound-gate|draft-signal` (C4), +per-finding `kind: hard|soft` (C2). No done/not-done
  field (C3).
- **[DDD4] Hard/soft generalized to prose oracles.** Hard = any deterministic check for the target
  (code: test suite/lint/types; prose: self-test pass, dead-link/broken-ref, frontmatter validity,
  file-length, required-citation). `overall_label=sound-gate` iff ≥1 hard oracle backs it. (ADR-011)
- **[DDD5] Reviewer independence v1 = single fresh-context subagent.** Different-model/multi-lens
  panel = documented extension seam (accepted v1 risk: same-model fresh-context isn't full
  independence). (ADR-010 consequences)
- **[DDD6] Standalone flow:** frame → curate independent input (exclude builder reasoning, C1) →
  dispatch → present ranked findings + label to human (ADR-002, advisory). Report by default, no
  trail unless asked (anxiety C). (ADR-010)
- **[DDD7] Composition = documentation only.** Agent publishes the typed `{target,intent,standards}`→
  verdict contract; SKILL documents the Workflow-weaving pattern. **No existing skill edited.** (ADR-010)

## Wave: DESIGN / [REF] Component decomposition

| Component | Path | Change type | Role |
|---|---|---|---|
| Command (thin loader) | `commands/adversarial-review.md` | CREATE NEW | driving port (CLI/skill) |
| Skill spine | `skills/adversarial-review/SKILL.md` | CREATE NEW | standalone driver: frame → curate → dispatch → present |
| Reviewer agent | `agents/adversarial-reviewer.md` | CREATE NEW | the reusable independent critic + typed-verdict contract |
| Self-test fixtures | `skills/adversarial-review/self-test/` | CREATE NEW | author-then-ablate golden bad tasks; C1–C5 regression gate |
| Acceptance scenarios | `skills/adversarial-review/acceptance.feature` | CREATE NEW | behavior spec |

## Wave: DESIGN / [REF] Driving ports

- `/phil:adversarial-review [target] [--intent "..."]` (CLI/skill, standalone).
- The reviewer agent as an invocable unit (Task / Workflow `agent()`) — the composition port,
  documented but unwired in v1.

## Wave: DESIGN / [REF] Driven ports + adapters

- **Independent reviewer** ← Task/Agent subagent (fresh context; curated input excludes builder
  reasoning — C1).
- **Oracle detection/execution** ← `skills/shared/test-runner-detection.md` (code) + prose checks
  (dead-link/frontmatter/length/citation/self-test) — run or inherit, never re-implement (ADR-005).
- **Human presentation** ← ADR-002 port (AskUserQuestion + optional editor review), advisory.

## Wave: DESIGN / [REF] Technology choices

Prose artifacts only (Claude Code plugin) — command + skill + agent markdown, authored per
nw-agent-builder/nw-forge conventions. No code paradigm (paradigm selection N/A; no CLAUDE.md
paradigm write). Oracles are prose-shaped (self-test fixtures, ADR-002 human diff, acceptance.feature).

## Wave: DESIGN / [REF] Decisions table

| DDD | Decision | ADR |
|---|---|---|
| DDD1 | prose spine + subagent substrate | ADR-010 |
| DDD2 | agent is the reusable unit | ADR-010 |
| DDD3 | pattern-copy verdict schema + label + kind | ADR-010/011 |
| DDD4 | hard/soft generalized to prose oracles | ADR-011 |
| DDD5 | single fresh-context reviewer; panel = seam | ADR-010 |
| DDD6 | standalone advisory flow, no default trail | ADR-010 |
| DDD7 | composition doc-only, no host edits | ADR-010 |

## Wave: DESIGN / [REF] Reuse Analysis

| Existing Component | File | Overlap | Decision | Justification |
|---|---|---|---|---|
| refactor-critic-correctness | `agents/refactor-critic-correctness.md` | independent critic; span-evidence schema; anti-flattery; reason-first | **CREATE NEW (pattern-copy)** | different judgment domain (general vs behavior-preservation+rubric); ADR-003 precedent favors pattern-copy over premature shared extraction; schema shape preserved for consistency. **Source unmodified.** |
| refactor-loop GUARD | `skills/refactor-loop/SKILL.md` | severity threshold θ + worst-first ranking | **REUSE (pattern ref)** | prose reference to the same threshold discipline; no code to share. **Source unmodified.** |
| test-runner-detection | `skills/shared/test-runner-detection.md` | code-oracle detection (slice 02) | **REUSE (invoke/include)** | shared read-only helper, called not changed. **Source unmodified.** |
| ADR-002 human port | `docs/product/architecture/adr-002-*.md` | advisory presentation to human | **REUSE (pattern)** | same human-approval port mechanism. |
| edd-evidence-critic (deferred) | `agents/` (planned, not built) | narrow executed-vs-narration pre-screen | **N/A (future note)** | adversarial-reviewer is its general form; recorded as a neighbor, but edd is **not** edited by this feature. |

Zero unjustified CREATE NEW; zero existing skills modified.

## Wave: DESIGN / [REF] Open questions (→ DISTILL/DELIVER)

- Exact typed-verdict JSON field names + the acceptance/self-test fixture set (DISTILL).
- The prose-oracle catalog breadth beyond the WS subset (DISTILL, slice 02+).
- Empirical: does a single fresh-context reviewer produce enough signal, or is the multi-lens
  panel needed sooner than "when composed into a workflow"? (DELIVER dogfood data.)
- Invocation mechanism for the reviewer subagent (Task vs Skill) — settled empirically by the
  slice-01 walking skeleton (mirrors ADR-005's open note).

## Wave: DESIGN / [REF] Changed Assumptions

**Original (DISCUSS, `docs/feature/adversarial-review/feature-delta.md` § slices, 2026-07-15):**
> "**03 — Composition** … one host (`phil:work` review-wave) **gates on the typed verdict
> programmatically**."

**New assumption (DESIGN, 2026-07-15):** v1 is **standalone only and edits no existing skill**.
Composition is delivered as a **documented typed contract + Workflow-weaving pattern**, not host
wiring. Slice 03 is **dropped**; the contract publication rides along in slice 02 (doc-only).

**Rationale:** user direction (2026-07-15) — "design as standalone adversarial-review command/skill,
not touching other commands/skills." This aligns with ADR-008's precedent (edd refused to touch
`phil:work`; extract/wire only when a real second consumer exists). Job traceability and the C1–C5
constraints are unaffected. Upstream note filed at `docs/feature/adversarial-review/design/upstream-changes.md`.
