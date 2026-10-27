# Feature Delta — edd-article-alignment (`/phil:edd`, revised)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF|WHY|HOW]` sections. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (job revised), `docs/product/journeys/edd-loop.yaml`
> (journey revised), `docs/product/personas/avery-expectation-owner.yaml` (mental model extended).
> Board: a checklist item on issue 38, by the developer's choice (2026-10-27).
> Build path: DISCUSS only — the deliverable is prose (CLAUDE.md, edd-loop DDD8).

---

## Wave: DISCUSS / [REF] Source

Andrea Laforgia, *Expectation-Driven Development: A Validation Framework for the Age of AI Agents*
(2026-03-21) — <https://a4al6a.substack.com/p/expectation-driven-development-a>. The author calls it
a proposal: "I haven't battle-tested EDD on a real project."

The article's protocol, in its order: **write expectations → hand them over → request executed
evidence → review adversarially → challenge and iterate → stabilize → archive.**

`/phil:edd` as shipped (edd-loop, 2026-07-15) keeps the article's evidence rule but departs from it in
five places:

| # | Article | `/phil:edd` today |
|---|---|---|
| 1 | Every expectation is proven by executed scenarios the human challenges | Checkable expectations go to the engine's tests; only the qualitative residue gets evidence |
| 2 | Review is adversarial: do the numbers add up, were the edge cases run, what input breaks it, what is missing | A two-way accept/reject; no way to ask for more scenarios |
| 3 | Capture covers happy path, past edge cases, non-functional requirements and must-not-happen; one expectation per breath; ordered by risk | Capture splits the intent into expectations, with no coverage, sizing or risk guidance |
| 4 | Expectations plus evidence are archived as a living record | The trail exists only when the qualitative gate ran |
| 5 | Stabilize turns expectations into automated tests, the regression alarm | Tests come first, inside the engine; nothing pins an accepted qualitative output |

Separately, `/phil:edd` cites `rules/coding.md`, `rules/testing.md` and `rules/architecture.md` in
one sentence that no step applies, and names no writing standard and no review, refactor or prose
skill. Issue 38 states the trap: a workflow "that name-drops rules and changes no behaviour would
clear the bar and fix nothing."

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `avery-expectation-owner` (extended — see SSOT).
- **JTBD one-liner:** *Prove that AI-built work meets my intent — every expectation, checkable or
  not — with executed evidence I challenge and adjudicate, built, tested and recorded to this
  plugin's own standards, with a short path when I choose to trust the tests.*
- **Job ID:** `prove-qualitative-expectations-with-evidence` — revised in place, id kept so edd-loop's
  traceability holds. The id now undersells the scope; renaming it is out of scope (see below).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** developer tool, user-facing — the user invokes `/phil:edd` and reads its output.
- **Brownfield revision** of a shipped skill: `skills/edd/SKILL.md`, `commands/edd.md`,
  `agents/edd-evidence-producer.md`, `skills/edd/self-test/`, `tests/test_edd_skill.py`.
- **Research depth:** lightweight — happy path plus the error paths below.

## Wave: DISCUSS / [REF] Locked decisions

D1–D3 were put to the developer on 2026-10-27 and answered; the rest follow from those answers and
the article.

- **[D1] Every expectation gets executed evidence by default; the developer may opt out the
  checkable ones for a run.** *(Developer's answer.)* After classification, `/phil:edd` asks once
  whether to trust the engine's tests for this run's checkable expectations. On a yes, those get no
  evidence and the record says so in as many words. Qualitative expectations cannot be opted out, nor
  can an expectation an approval test pins: its first output needs a human read (amended at slice 01
  review, 2026-10-27). Revises edd-loop
  D1 and the off-ramp (see Changed Assumptions).

- **[D2] Serious findings from the plugin's own reviews block done; the developer can waive one by
  name.** *(Developer's answer.)* "Serious" is fixed per source, not judged per run:

  | Source | Runs over | Blocks done | Advises |
  |---|---|---|---|
  | `phil:review-code` | every changed source and test file | Priority 1 (correctness, safety, security); Priority 6 (test quality) on a test that pins an accepted expectation | every other priority |
  | `phil:adversarial-review` | the built work against the expectations | a judge-`confirmed` finding of severity `major` | `minor`, `nit` |
  | `phil:red-team-prose` | every document `/phil:edd` composed | a `[fitness]` finding — the reader cannot use the document | `[tells]`, `[clarity]` |
  | `phil:ux-review` | changed UI files, when the change touches UI | `must-fix` | `consider` |

  A waiver names the finding and the developer's reason, and the record keeps both. An advisory
  finding is offered for repair (D7) and recorded whether taken or not.

- **[D3] The work lives on issue 38 as a checklist item.** *(Developer's answer.)* It is a worked
  example of that card's demand that a standard be *applied*, not cited — a check that fails, a gate
  that blocks, a reviewer that reads it. It settles none of issue 38's larger questions.

- **[D4] Capture follows the article's guidance.** Before confirming the list, `/phil:edd` checks it
  covers the happy path, past edge cases, non-functional requirements and behaviour that must not
  happen; splits any expectation that takes more than one breath to say; expands any too thin to
  test; and orders the list by risk. Evidence, review and challenge then run in that risk order. The
  restatements and suggestions `/phil:edd` composes follow `rules/writing.md`; the developer's own
  wording stays as written.

- **[D5] Classification chooses the kind of evidence, not whether to exit.**
  - **checkable** → the evidence is the scenario actually run: its inputs and the real output, not
    "the tests passed".
  - **qualitative** → the evidence is the thing run or rendered for the developer's taste. The
    honesty rule stays: qualitative only with a developer-confirmed concrete reason, after the
    property-based and approval-test patterns in `rules/test-patterns.md` are ruled out.
  - **not executable in the loop** (the article's third category: rendered UI, a rate-limited API) →
    the producer reports it cannot run it; the developer spot-checks by hand or stops, and the record
    says which.

- **[D6] Evidence stays executed, and the producer stays independent.** edd-loop D2 holds: a
  description, summary or claim with no reproducible artifact is narration — the article's
  "generative evidence" — and is rejected. edd-loop D4 holds: the non-builder producer gathers it.
  This is stricter than the article, which lets the builder produce evidence and lists a second
  auditing agent only as a mitigation.

- **[D7] Adversarial review comes before any verdict, and the developer can challenge.** After the
  evidence is in, `phil:adversarial-review` runs over the built work against the expectations — the
  article's second auditing agent. The developer then sees, per expectation, the evidence, the
  confirmed findings and the article's four challenge questions, and answers one of three ways:
  - **accept** — the expectation is met;
  - **reject** — it is not; the engine changes the thing, then evidence is re-gathered;
  - **challenge** — the evidence is not enough; name the scenario or expectation to add, and new
    evidence is commissioned without a rebuild.

  An ambiguous answer is unanswered; a second unanswered ask blocks done. The developer may stop
  over a standing reject or challenge, and the run is reported **not done**.

- **[D8] Stabilize pins every accepted expectation with a test written to this plugin's testing
  standards.**
  - A checkable expectation is pinned by an automated test that `rules/testing.md` and
    `rules/test-patterns.md` accept.
  - An accepted output too large or too subjective to assert becomes an **approval test**, its
    approved output the evidence the developer just accepted — the first human read has already
    happened. This answers the article's own weakness: old evidence going silent when the feature
    changes.
  - `/phil:edd` writes no test itself. The engine that built writes the pinning tests by default;
    authoring may pick a fresh delegate instead.
  - `phil:review-code` then runs over the changed code and tests. D2's blocking findings must be
    fixed or waived. The rest of its backlog is offered for repair through the plugin's own skills:
    code smells through `phil:refactor` (or `phil:refactor-loop` for a larger change), structural
    test smells through `phil:refactor-tests`, tests coupled to implementation through
    `phil:redesign-tests`, comment findings through `phil:clean-comments`. Each repair runs under its
    own gate; the suite stays green.

- **[D9] The living record is written for every run that built, to this plugin's writing
  standards.** The trail under `docs/edd/<slug>/` and the summary in `docs/evolution/` are written
  whenever the engine built, opt-out runs included. They record expectations, classifications,
  evidence, challenges, verdicts, opt-outs and waivers. Before the trail is written,
  `phil:red-team-prose` reviews every document `/phil:edd` composed — it composes `phil:ai-eos`,
  `phil:eos` (which applies `rules/writing.md`) and `rules/technical-communication.md` — and its
  auto-applicable fixes are applied to composed words only. Two things are never edited:
  - `evidence/` — byte-identical to what the producer captured;
  - the developer's own words — each field carries its provenance, as `phil:groom-ask` does, and only
    composed fields are edited.

  A run that stops at capture, before any build, writes nothing.

- **[D10] The engines stay unchanged.** nwave and `phil:work` are composed as they are (edd-loop
  constraint kept). Every gate above runs in `/phil:edd` after the engine returns, not inside it.

- **[D11] Each standard is applied by a check that fails, not by a citation.** Every new citation and
  gate gets a string-level assertion in `tests/test_edd_skill.py`, watched failing before it passes
  (CLAUDE.md). Self-test fixtures are revised and added for each new decision outcome — but **edd's
  self-test has no driver** (issue 42), so those fixtures gate nothing until one exists. The pytest
  assertions are the only enforcement this feature can claim.

## Wave: DISCUSS / [REF] User stories

### Story 1 — Capture that covers the ground *(slice 01)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I want `/phil:edd` to check my expectations for coverage, size and risk before I
confirm them, so the gaps surface while they are cheap to fill.

### Elevator Pitch
Before: I confirm a list with no edge case, no non-functional requirement and nothing that must not happen, and learn what was missing after the build.
After: run `/phil:edd "<intent>"` → sees the expectations ordered by risk, with a line per missing category — `No expectation covers what must not happen` — and a suggestion for each, marked as a suggestion.
Decision enabled: I fill, decline or reword each gap before anything is built.

**Acceptance criteria**
- AC1.1 — Given an intent with no must-not-happen expectation, when capture runs, then it names that
  category as missing and offers a suggestion labelled as composed, not as mine.
- AC1.2 — Given an expectation stating two behaviours, when capture runs, then it proposes splitting
  it in two.
- AC1.3 — Given a confirmed list, then it is ordered by risk, and evidence, review and challenge run
  in that order.
- AC1.4 — Given an expectation I wrote, then my wording reaches the record unchanged; only composed
  suggestions follow `rules/writing.md`.

### Story 2 — Evidence for every expectation, with an opt-out *(slice 01)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I want executed evidence for checkable expectations too, unless I choose to trust the
tests for this run, so a passing suite the builder wrote is not my only proof.

### Elevator Pitch
Before: checkable expectations go to the engine's tests and never reach me; I trust tests the builder wrote.
After: run `/phil:edd "<intent>"` → sees `Trust the tests for the 4 checkable expectations this run? (no: each gets its scenario run and shown to you)`, then per expectation `EVIDENCE — '<expectation>': <inputs> → <verbatim output> [reproduce: <command>]`.
Decision enabled: I spend review time where my trust in the tests is lowest.

**Acceptance criteria**
- AC2.1 — Given checkable expectations and no opt-out, when evidence runs, then each gets a
  scenario's inputs and verbatim output from the non-builder producer, with its reproduce command.
- AC2.2 — Given an opt-out, then no checkable expectation gets evidence, no qualitative expectation
  is skipped, and the record states which expectations were trusted to the tests.
- AC2.3 — Given evidence that reads "all tests passed" with no scenario output, then it is rejected as
  narration.
- AC2.4 — Given an expectation the producer cannot run in the loop, then I am told so and choose to
  spot-check by hand or stop, and the record says which.

### Story 3 — Adversarial review and challenge before any verdict *(slice 02)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I want an independent adversary to attack the work before I judge it, and I want to
ask for more scenarios rather than only accept or reject, so my verdict rests on evidence I pushed
on.

### Elevator Pitch
Before: I see one piece of evidence and can only accept or reject it.
After: run `/phil:edd "<intent>"` → sees, per expectation, the evidence, `CONFIRMED (major): <finding> — <span>` from the independent reviewer, the four challenge questions, and three answers: accept, reject, challenge.
Decision enabled: I ask for the scenario that would break it before I accept.

**Acceptance criteria**
- AC3.1 — Given gathered evidence, when review runs, then `phil:adversarial-review` runs over the
  built work against the expectations before any verdict is asked for.
- AC3.2 — Given a challenge naming a scenario, then new evidence is commissioned for it and nothing is
  rebuilt.
- AC3.3 — Given a confirmed `major` finding that is neither fixed nor waived, then done is blocked.
- AC3.4 — Given I stop over a standing reject or challenge, then the run is reported not done and the
  record keeps it.

### Story 4 — Stabilize to this plugin's testing and coding standards *(slice 03)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I want every accepted expectation pinned by a test that meets the plugin's testing
standards, and the built code reviewed and cleaned with the plugin's own skills, so the standards I
wrote down are the ones applied.

### Elevator Pitch
Before: the engine's own standards decide test and code quality, and this plugin's rules are cited but never read.
After: run `/phil:edd "<intent>"` → sees `STABILIZE: 6 accepted, 6 pinned (4 tests, 2 approval tests)` then `REVIEW: 1 blocking (Priority 1, src/x.py:42), 5 offered for repair`.
Decision enabled: I fix or waive each blocking finding, and choose which repairs to run.

**Acceptance criteria**
- AC4.1 — Given an accepted expectation with no test pinning it, then done is blocked.
- AC4.2 — Given an accepted qualitative output, then it is pinned by an approval test whose approved
  output is the evidence I accepted.
- AC4.3 — Given a Priority 1 finding, or a Priority 6 finding on a pinning test, then done is blocked
  until it is fixed or I waive it with a reason the record keeps.
- AC4.4 — Given advisory findings, then each is offered to the skill that owns it — `phil:refactor`,
  `phil:refactor-tests`, `phil:redesign-tests` or `phil:clean-comments` — and each repair runs under
  its own gate.
- AC4.5 — Given a change that touches UI, then `phil:ux-review` runs and a `must-fix` blocks done.

### Story 5 — A living record written to this plugin's writing standards *(slice 04)*
`job_id: prove-qualitative-expectations-with-evidence`

As **Avery**, I want the record of every run that built to read clearly, without touching the
evidence or my own words, so a teammate can learn what was expected and how we know.

### Elevator Pitch
Before: the trail exists only when the qualitative gate ran, and the prose `/phil:edd` composes meets no writing standard.
After: run `/phil:edd "<intent>"` → sees `PROSE: 3 composed documents reviewed — 7 fixes applied, 0 fitness findings; evidence/ and your wording untouched` then `Wrote docs/edd/<slug>/ and docs/evolution/<date>-<slug>.md`.
Decision enabled: I share the record as the answer to "what does this do, and how do we know?"

**Acceptance criteria**
- AC5.1 — Given a run that built, opt-out runs included, then the trail and evolution summary are
  written; given a run that stopped at capture, nothing is.
- AC5.2 — Given the composed documents, then `phil:red-team-prose` reviews them before they are
  written, and a `[fitness]` finding blocks done until fixed or waived.
- AC5.3 — Given the written trail, then every file under `evidence/` is byte-identical to the capture.
- AC5.4 — Given a field holding my words, then it carries a `you wrote` label and no fix touched it.
- AC5.5 — Given `skills/edd/SKILL.md` without its `rules/writing.md` citation, then
  `tests/test_edd_skill.py` fails.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| Evidence coverage | 100% of expectations end with evidence, a recorded opt-out, or a recorded hand spot-check | fixture: count per expectation |
| No silent opt-out | 0 opt-out runs whose record omits which expectations were trusted to tests | fixture |
| Pinned expectations | 100% of accepted expectations pinned by a test at done | fixture |
| No standing blocker | 0 runs reported done with an unwaived blocking finding from D2's table | fixture per source |
| Untouched evidence | 100% of `evidence/` files byte-identical to capture | fixture: hash compare |
| Applied, not cited | every new citation and gate fails `tests/test_edd_skill.py` when removed | pytest, watched red first |
| Proportionate opt-out | an all-checkable opt-out run asks exactly one more question than capture | dogfood transcript |

## Wave: DISCUSS / [REF] Out of scope

- Changing nwave or `phil:work` internals (D10), and issue 38's larger questions: which methodology
  owns feature work, and whether nwave stays.
- A driver for edd's self-test fixtures (issue 42).
- Renaming the job id.
- Cross-domain sequencing (edd-loop slice 03), no-argument resume, and an automated verdict — all
  still deferred. `phil:adversarial-review` advises; the developer still decides.
- Extracting the evidence gate into a shared skill (ADR-008 stands).

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:edd "<intent>"`, unchanged.
- **New driven ports:** `phil:adversarial-review` (review), `phil:review-code` (code and test
  review), `phil:refactor`, `phil:refactor-loop`, `phil:refactor-tests`, `phil:redesign-tests`,
  `phil:clean-comments` (repair), `phil:ux-review` (UI), `phil:red-team-prose` (composed prose).
- **Prerequisites:** all of the above ship in this plugin today. `rules/testing.md`,
  `rules/test-patterns.md`, `rules/writing.md`, `rules/technical-communication.md` exist.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

None new. The shipped `/phil:edd` is the skeleton; each slice extends one step of it end to end.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** 5 stories across 4 slices; one skill, one command, one agent revised; nine
existing skills composed, none modified; no new mechanism beyond the gates and their assertions.

## Wave: DISCUSS / [REF] Definition of Done

1. `skills/edd/SKILL.md` runs the article's seven steps in its order, with the opt-out after
   classification.
2. Every story traces to `prove-qualitative-expectations-with-evidence`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Each blocking source in D2's table blocks done in a fixture, and its waiver is recorded.
5. Every accepted expectation is pinned by a test in a fixture.
6. `evidence/` and the developer's words survive the prose review untouched in a fixture.
7. Every new citation and gate has a `tests/test_edd_skill.py` assertion, watched red first.
8. `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` run over the result; `phil:eos` and
   `/phil:harden-instructions` run before the release that ships it.
9. Issue 38's checklist item is ticked with the merging PR named.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | job revised in `jobs.yaml`; all 5 stories carry its id |
| 2 | Persona defined | ✅ | `personas/avery-expectation-owner.yaml`, extended |
| 3 | Journey mapped | ✅ | `journeys/edd-loop.yaml`, revised to the seven steps with error paths |
| 4 | Elevator pitches | ✅ | all 5 stories, `/phil:edd` entry point, observable output |
| 5 | ACs testable | ✅ | Given-When-Then, fixture- or pytest-checkable |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-04` |
| 7 | Walking skeleton | ✅ | the shipped skill (brownfield) |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope Assessment above |

Requirements completeness: every article step and every skill named in the request maps to a
decision and an AC. One open item, the pinning delegate (decided at authoring), is a design choice, not a missing
requirement.

## Wave: DISCUSS / [REF] Changed Assumptions

DISCOVER and DIVERGE never ran; the assumptions changed are edd-loop's DISCUSS and DESIGN decisions.
Those documents stay unedited.

- **edd-loop D1**, `docs/feature/edd-loop/feature-delta.md`:
  > "**Honesty rule / bias-to-off-ramp:** default every expectation to engine-checkable; mark
  > qualitative **only** when the developer confirms a *concrete* reason it can't be cheaply
  > asserted. Evidence ceremony is opt-in, never the default."

  **New:** evidence is the default for every expectation, and opting out is the developer's explicit
  choice per run (D1). The honesty rule survives inside classification (D5). **Why:** the article's
  premise is that a green suite the builder wrote is not proof; the developer chose its default on
  2026-10-27.

- **edd-loop D5**, same file:
  > "**No trail is written for an off-ramp-only run** (no ceremony)."

  **New:** a trail is written for every run that built (D9). **Why:** the article archives every
  expectation; an opt-out recorded nowhere is the silent trust this feature removes.

- **edd-loop DDD2 / ADR-007**, same file:
  > "`/phil:edd` never re-verifies engine-checkable expectations; nwave's AT run and `phil:work`'s
  > preservation+goal gates are the oracle for those."

  **New:** the engine's oracle still proves them, and `/phil:edd` still re-runs no check; it shows the
  developer the scenario run as evidence (D1, D5). **Why:** showing an executed scenario to a human is
  evidence, not re-verification; the oracle's verdict is unchanged.

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 evidence by default with an opt-out · D2 per-source blocking table with named
  waivers · D3 lives on issue 38 · D4 article's capture guidance · D5 classification picks the
  evidence kind · D6 executed evidence, independent producer · D7 adversarial review and challenge ·
  D8 stabilize to the testing standards, review and repair with the plugin's skills · D9 record every
  run that built, composed prose reviewed, evidence and the developer's words untouched · D10 engines
  unchanged · D11 pytest assertions are the enforcement.
- **Requirements summary:** `/phil:edd` follows the article's seven steps; every expectation gets
  executed evidence unless the developer opts out the checkable ones; an independent adversary and
  the developer's challenges precede every verdict; accepted expectations are pinned by tests written
  to `rules/testing.md`; the plugin's review, repair and prose skills run, and their serious findings
  block done.
- **Constraints:** engines unchanged; producer ≠ builder; the developer adjudicates; evidence and the
  developer's words are never edited.
- **Open at authoring** (DESIGN does not run here — CLAUDE.md): who writes the pinning tests (the engine that built, or a fresh delegate); the
  order of `phil:review-code` and the repairs relative to stabilize; how a waiver is recorded; whether
  ADR-007 and ADR-009 are amended or superseded.
- **Upstream changes:** see Changed Assumptions.
