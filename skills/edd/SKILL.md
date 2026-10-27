---
name: edd
description: Skill bundle for phil:edd command — Expectation-Driven Development, after Andrea Laforgia's protocol. Captures intent as expectations checked for coverage, size and risk; delegates the build to nwave or phil:work; gathers executed evidence for every expectation, from someone other than the builder, unless the developer trusts the tests for the checkable ones or spot-checks one no agent can run; has an independent adversary review the work; puts evidence and findings to the developer to accept, reject, challenge or stop; then pins every accepted expectation with a test and reviews and repairs the code with this plugin's own skills.
---

# EDD — Expectation-Driven Development

Run Andrea Laforgia's Expectation-Driven Development protocol over a developer's intent: write the
**expectations**, hand the build to the fitting engine, gather **executed evidence** that each one
holds, and put that evidence to the developer, who decides. The protocol's source:
<https://a4al6a.substack.com/p/expectation-driven-development-a>.

This is the **expectation-driven sibling to `phil:work`**, the general contractor for invisible work
(preserve behaviour and hit a checkable goal). Each step reads the standard it applies, where it
applies it.

> **The full flow.** CAPTURE (intent → expectations, checked for coverage, size and risk) → CLASSIFY
> (which kind of evidence) → OPT-OUT (trust the tests for the checkable ones this run?) → BUILD
> (delegate to one engine, inherit its oracle) → EVIDENCE (executed, producer ≠ builder, for every
> expectation not opted out) → REVIEW (an independent adversary, its findings judged) → ADJUDICATE
> (the developer accepts, rejects, challenges or stops) → STABILIZE (pin each accepted expectation;
> review the code) → FINDINGS (clear each blocking finding) → REPAIR (the advisories, by their owners)
> → DOCUMENT (every run that built).

---

## The two lines to hold

1. **A green suite the builder wrote is not proof.** Every expectation gets executed evidence by
   default, with two exceptions, each the developer's call and each recorded explicitly: they may
   trust the tests for a run's checkable expectations, and they may spot-check by hand an expectation
   no agent can run here, or one the agent has twice failed to run. Leave both calls to the developer.
2. **Someone other than the builder grades the work.** Evidence an agent returns must be **executed**
   (a real run or render captured verbatim, not a description) and produced by an agent that is
   **not** the builder; the **developer** adjudicates. A hand spot-check is the one description
   allowed: the developer's own observation, never an agent's.

---

## Every ask

Every question this skill puts to the developer — CAPTURE's confirmation, OPT-OUT, BUILD's
cannot-meet, EVIDENCE's spot-check, ADJUDICATE, FINDINGS, REPAIR's offer, and DOCUMENT's apply and
fitness asks — follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.
Load it before the first ask. On top of that standard:

- **Every ask offers `stop`.** A stop before BUILD starts ends the run and writes nothing; a stop once
  BUILD has started writes the trail as it stands and reports the run not done.
- **Unanswered.** An ambiguous or empty reply is unanswered, and two consecutive unanswered asks end
  the run, reported not done. This overrides the standard's "treat it as a decline", which means
  nothing for most of these asks. OPT-OUT alone treats an ambiguous reply as a no.
- **Caps.** Every "second" cap in this skill — a second red oracle, narrated return, cannot-run, fix
  round, prose fix round, reject or challenge — means the second and every one after it.
- **Free text is the developer's.** Every free-text answer is recorded labelled `you wrote` — a
  reject's reason, a challenge's scenario, a waiver's or a drop's reason, a reworded expectation, a
  spot-check's observation. An answer that needs words — a challenge's scenario, a reject's or a
  waiver's reason — comes through the ask's "Other" field or one follow-up ask; an empty follow-up is
  unanswered.
- **The developer's words stay theirs.** Quote a `you wrote` line word for word in the context block;
  in the counted ask, describe it in plain terms, so a path or identifier in it never trips the ask's
  rules.

---

## Parse the argument

| Pattern | Action |
|---|---|
| `"<intent>"` | Run CAPTURE on the intent, then the flow below. |
| No argument | Ask for an intent. No-argument **resume** of an in-flight loop does not exist. |

Derive a kebab-case `<slug>` from the intent for the trail path `docs/edd/<slug>/`. Create it only when
DOCUMENT writes the trail, once BUILD has started.

---

## CAPTURE — intent → expectations

Restate the intent as a list of discrete **expectations**, each a single statement of something the
developer expects to be true when the work is done. Surface qualitative ones explicitly (tone,
clarity, ergonomics, "helpful", "feels X").

Before showing the list, check it the way the article asks:

- **Coverage.** Name each of these categories that no expectation covers, and suggest one for each
  gap:
  - the **happy path**;
  - **past edge cases** — the bugs this area has had before. Ask the developer, or search the
    history (`git log`, the issue tracker, tests that pin old bugs); never invent a past bug;
  - **non-functional requirements** the intent implies — performance, error handling, security, limits;
  - behaviour that **must not happen** — breaking existing behaviour, losing or leaking data, acting
    unasked. An expectation that existing behaviour stays unchanged covers this category.
- **Size.** One expectation is one behaviour the developer could explain to a colleague in a single
  breath. Propose splitting any that takes more than one breath — its parts will classify and route
  differently — and expanding any too thin to test.
- **Risk.** Order the list by risk, worst first, ranked by what a miss would cost: how many users it
  hits, and how hard it is to undo. Evidence and adjudication follow this order, so the developer's
  attention goes where a miss would cost most.

Label every line with its provenance:

- `you wrote` — the developer's words, kept exactly as written; never edit one to fit a standard;
- `composed` — a restatement, suggestion or split this skill wrote;
- `you edited` — a composed line the developer then changed; their edit stands as written.

When splitting a `you wrote` line, keep the original `you wrote` line in the record beside the
halves: the halves are `composed` and live, the original records what the developer said. Read
`${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing, and write every composed line to it —
active voice, no needless words, one behaviour per line.

Ask the developer to confirm the list, with the list itself in the context block so the counted ask
stays under its ceiling. The developer may confirm, edit, accept or decline each suggestion, or stop.
Proceed only once the list is confirmed.

---

## CLASSIFY — which kind of evidence

Classification decides what each expectation's evidence must show.

- **checkable** — the target engine's native oracle can produce a pass/fail result at reasonable
  cost:
  - **nwave** (user-facing behaviour) → an acceptance test can assert it (deterministic observable
    output: stdout, response, exit code, state).
  - **phil:work** (invisible or developer-facing) → a checkable metric (coupling, complexity, a
    benchmark, a dead-link, frontmatter or citation check).

  Its evidence is the **scenario actually run** — see EVIDENCE.
- **qualitative** — asserting it would encode a **subjective judgment** (helpful, clear, ergonomic,
  aesthetic) that no cheap deterministic assertion captures. Its evidence is the thing run or
  rendered for the developer's taste.
- **not executable in the loop** — nothing in this run can exercise it: a rendered UI no agent can
  watch, a rate-limited or paid third-party API, a production-only condition. Its evidence is the
  developer's own spot-check — see EVIDENCE. An expectation the engine's tests can exercise, even
  with part of it mocked, is checkable.

**The honesty rule.** Default every expectation to **checkable**. Mark one qualitative only when the
developer gives a **concrete reason**: one that names what about this expectation no assertion
captures. Ask "what specifically can't a test assert here?" and leave the reason to the developer.
Mark one not executable in the loop only when the developer confirms the concrete blocker — what
stops anything in this run from exercising it. Both kinds take evidence away from the default, so
neither is this skill's call.

**Test two patterns against a stated reason before accepting it.** Read
`${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` before classifying: it names two patterns that make a
hard-to-assert output checkable. A **property-based test** asserts a rule over generated inputs where
no single example captures it. An **approval test** pins a large output: a human reads it once, and
every later run is a diff. Neither captures a subjective judgment such as "helpful", but both remove
"too large or too varied to assert" as a reason — an expectation either one can assert is checkable.
**An approval test's first approval is still a human read**: name it in the classification table as
the step before any diff means anything.

Produce a **classification table**: each expectation → `checkable` (with the engine, its native
oracle, and `approval test` where one pins it), `qualitative` (with the developer's concrete reason),
or `not executable in the loop` (with the developer-confirmed blocker).

> Split within one expectation: when an expectation has a cheaply assertable core ("fails with a
> non-zero exit and names the path") plus a wrapper someone offers as qualitative ("...and the
> message is helpful"), propose splitting it in two. The core is checkable; the remainder is
> checkable too unless the developer gives a concrete reason under the honesty rule. The halves are
> `composed`; put them to the developer to confirm and slot them into the risk order.

---

## OPT-OUT — trust the tests for the checkable ones?

Ask once, after the developer has seen the classification table, whether to trust the engine's
tests for this run's **checkable** expectations. Skip the ask when no row can be opted out.

Name the cost of each answer: a yes leaves tests the builder wrote as the only proof for those
expectations; a no gives each one its scenario run, shown to the developer. **An ambiguous answer is
a no** — this overrides the standard's second ask, because the safe default needs no answer.

- **No** — every expectation gets evidence.
- **Stop** — end the run before anything is built.
- **Yes** — checkable expectations get no evidence; the engine's oracle alone proves them. The record
  names every expectation trusted to the tests: mark each of their rows in the classification table
  `trusted to the tests`.

Only checkable rows can be opted out: a row not executable in the loop has no tests to trust. A row
whose oracle the table cannot name as a concrete assertion cannot be opted out either: the honesty
rule makes it checkable by default, but no test yet proves it. Two more kinds of row cannot be opted
out, whatever the answer:

- A qualitative expectation cannot be opted out: no test asserts it, so the developer's judgment on
  executed evidence is its only proof.
- An expectation an approval test pins cannot be opted out: the test has no baseline until a human
  approves its first output, and the builder must not approve its own. Its evidence is that first
  output, put to the developer.

---

## BUILD — delegate to one engine, inherit its oracle

Record the commit the build starts from as `base`: STABILIZE reviews every file changed since it.
Delegate the build to the fitting engine and let its native oracle prove the checkable expectations:

- **user-facing behaviour** → nwave (its acceptance-test run is the oracle);
- **invisible or developer-facing** → `/phil:work` (its preservation floor and checkable goal are the
  oracle).

Hand the engine the confirmed expectations, in risk order, as its specification — not the intent they
came from — with the classification table, so it writes the approval tests the table names. Then let
it work uninterrupted. If the engine reports it cannot meet an expectation, put
its explanation to the developer, who may reword it, drop it on the record, or stop. This report
comes before the red-oracle rule: the red oracle an unmet expectation produces goes to the developer
with the engine's explanation, not back to the engine. A reworded expectation is the developer's —
`you wrote`, or `you edited` if it started from a suggestion — goes back through CLASSIFY, gets
evidence whatever OPT-OUT said, since the opt-out never saw it, and the engine continues against the
new wording. A dropped one is recorded as dropped by the developer, with their reason. It never
counts as met, and it does not block done: the developer decided it, and the report names it.

Run one engine per run. When the expectations need both, say so and, with the developer's agreement,
split the intent into two runs, one per engine; this skill does not sequence engines.

Run no preservation or acceptance check of your own — that is the engine's job, and its verdict
stands. Capture its run verbatim as `oracle_result` — the output, not the engine's summary of it —
replaced on every rebuild and every pin commit; when the engine returns no oracle run, record that
none exists. A red oracle blocks done: route the failing expectation back to the engine, as a reject
would — and after a second red oracle on the same expectation, put the failure to the developer, who
sends it back again or stops. An approval test still awaiting its first approval is not red: its
first output goes to the developer at EVIDENCE. Record which engine built. The evidence adds what the
oracle cannot: the scenario's real inputs and output in front of the developer.

Any return to the engine that changes files outside the tests is a rebuild — a reject, a red oracle, a
missing build EVIDENCE found, or a FINDINGS fix. A rebuild re-runs REVIEW on the whole target, replaces
`oracle_result`, and re-asks every expectation whose evidence the
change touched: re-gather that evidence, review, and put it to the developer again. An accept on
evidence the rebuild invalidated no longer stands. Once the developer has adjudicated again, the run
re-enters STABILIZE over everything changed since `base`. A waiver stands only while the content it
waived is unchanged.

## EVIDENCE — executed evidence for every expectation not opted out

Every expectation not trusted to the tests gets executed evidence from the non-builder producer, in
the risk order CAPTURE set — or, for one not executable in the loop, the developer's hand spot-check.
Read `${CLAUDE_PLUGIN_ROOT}/skills/edd/references/evidence.md` before gathering any evidence: it holds
the steps in order — reuse, commission, reject narration, a producer that cannot run — and the
dispatch contract.

## REVIEW — an independent adversary attacks the work

Before any verdict, an independent adversary attacks the built work, and an independent judge
confirms or refutes each of its findings. Read `${CLAUDE_PLUGIN_ROOT}/skills/edd/references/review.md`
before dispatching anything: it holds the curated input, the two dispatches, the routing on the typed
verdict, and where each confirmed finding goes. The reviewer never sees the builder's reasoning, and
each finding gets its own fresh judge. A judge-confirmed `major` blocks done until FINDINGS clears it.
The review advises; the developer decides every verdict.

## ADJUDICATE — the human decides

Put each expectation's evidence to the developer via the human-approval port (AskUserQuestion, plus
optional review of the artifact in their editor), in risk order. Skip rows trusted to the tests: the
engine's oracle decided them.

- **The evidence and its attached findings are the context block, verbatim and unsummarised.** They
  are what the developer judges: a paraphrase in the ask breaks the word limit and replaces what the
  developer must read. Open an artifact too long for the context block in the developer's editor
  instead, and say so.
- **Then the article's four challenge questions in the context block**, after the evidence: *Do the
  numbers add up? Were the edge cases actually run? What input would break it? What scenario is
  missing?* They prompt the developer's reading; they are not a separate ask.
- **Four answers, and none is a default.** `accept`, `reject`, `challenge` and `stop` are the answer
  set. Name each answer's cost in its description: accept closes this expectation on this evidence;
  reject costs a rebuild, a re-review and a new round; challenge costs another evidence run and no
  rebuild; stop ends the run not done, with the trail written.

The developer — never this skill, the producer or the reviewer — renders the verdict. A hand
spot-check ends in a verdict too: the developer accepts or rejects on what they observed. The
developer's reject outranks a green oracle: the oracle checks what the test asserts, the developer
what they meant.

- **accept** → the expectation is met; record the verdict.
- **reject** → the expectation is **not** met. **Block done.** Take the developer's reason, route the
  expectation back to the engine to change the thing, and follow BUILD's rebuild rule. Keep a rejected
  expectation open — only the developer may drop one, at BUILD's cannot-meet ask, on the record — and
  report the run not done while any expectation stands rejected. Grade the final state, not the
  effort. The developer may stop instead: the reject stands, recorded.
- **challenge** → the evidence is not enough; the thing itself was never judged, so a challenge is
  not a reject. The developer names the scenario to run, or an expectation to add.
  - A challenge commissions evidence for the named scenario and rebuilds nothing. The producer
    receives it as `scenario`; the evidence goes through EVIDENCE's steps and returns to this ask with
    its findings already attached; REVIEW does not re-run, since nothing was rebuilt.
  - A challenge on a spot-checked expectation asks the developer to spot-check the named scenario.
  - A challenge that adds an expectation sends it through CLASSIFY, labelled `you wrote`, into its
    place in the risk order; it gets evidence whatever OPT-OUT said, since the opt-out never saw it.
    Before its ask, re-run REVIEW with the added expectation in its intent.
  - A challenge may be a rewording that tightens a vague expectation. The new wording is the
    developer's — `you wrote`, or `you edited` if it started from a suggestion — and goes back through
    CLASSIFY; its earlier evidence no longer stands. It gets evidence whatever OPT-OUT said, and REVIEW
    re-runs with the new wording in its intent, before its next ask.
  - A reply that the evidence does not show this expectation — the wrong scenario, irrelevant reused
    evidence — is a challenge: commission fresh evidence and rebuild nothing.
- **stop** → end the run. Record every standing reject, challenge and unproven expectation as it
  stands, write the trail, and report the run **not done**. A stop over an unproven expectation is
  reported not done, the expectation recorded as unproven.

A reject or challenge re-asks only on new evidence. After a second reject or a second challenge on the
same expectation, say so in the next ask and recommend stop; the developer may go on.

## STABILIZE — pin every accepted expectation, then review the code

The article's stabilize step: turn what the developer accepted into the regression alarm, and hold the
built code to this plugin's standards rather than the engine's. Read
`${CLAUDE_PLUGIN_ROOT}/rules/testing.md` and `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` first.
Read `${CLAUDE_PLUGIN_ROOT}/skills/edd/references/stabilize.md` before pinning anything: it holds the
pin dispatch and its checks, and how to run each review.

- **Pin.** This skill writes no test itself; the engine that built pins every accepted expectation, and
  every row trusted to the tests, with a test. An accepted qualitative output, or one too large to
  assert, is pinned by an approval test whose approved output is the evidence the developer accepted,
  verbatim. An accepted expectation no test pins blocks done.
- **Review the code.** `phil:review-code` runs over every file changed since `base`, pinning tests
  included. On lines changed since `base`, a Priority 1 finding (not an `Advisory` or `LWS-n` item)
  blocks done, as does a Priority 6 finding on a pinning test.
- **Audit the UI.** When the change touches UI files, `phil:ux-review` runs over them; a `must-fix`
  blocks done.

Pinning tests and running a repair are not rebuilds: neither changes what the code does, and each runs
under the suite.

## FINDINGS — clear each blocking finding

Once every expectation put to the developer is accepted — rows trusted to the tests are never put —
and STABILIZE has run, put each unwaived blocking finding to the developer, with its span, mechanism
and evidence in the context block:

- a judge-confirmed `major` from REVIEW — attached to an expectation, on a row trusted to the tests,
  or bearing on none;
- from `phil:review-code`, a Priority 1 finding on a line changed since `base` — not an `Advisory` or
  `LWS-n` item — or a Priority 6 finding on a pinning test;
- a `must-fix` from `phil:ux-review`;
- an accepted expectation, or a row trusted to the tests, that no test pins.

Three answers, `fix`, `waive` and `stop`, each with its cost:

- **fix** — route the finding to the engine and follow BUILD's rebuild rule; costs a rebuild, a
  re-review, a re-ask of every expectation the change touched, and STABILIZE again. A fix whose change
  touches only test and approved-output files is not a rebuild — an unpinned expectation's pin, or a
  weak pinning test split — and STABILIZE re-checks the pins and re-reviews the changed tests. A
  finding from `phil:review-code` or `phil:ux-review` never clears on the engine's word: STABILIZE's
  re-run clears it only when the re-run does not reproduce it.
- **waive** — take the developer's reason; record the finding, the reason and a timestamp. The finding
  no longer blocks done while its span is unchanged.
- **stop** — end the run not done, with the finding recorded as standing.

An accepted expectation spot-checked by hand, which no test can pin here, comes to FINDINGS too, with
only `waive` and `stop`: no fix can pin it, so the developer decides, by name, to finish without one.

Treat a finding in a later review as the same finding when it names the same file, the same mechanism
and the same offending content — never by line numbers, which every fix shifts: it keeps its fix-round count, and a waived one stays waived. After a second
fix round on the same finding, offer only `waive` and `stop`: the engine has failed it twice. List the
confirmed `minor` and `nit` findings from REVIEW after the blockers; the developer may send any of them
to the engine as a `fix`, and the record keeps each one either way.

## REPAIR — the advisories, by the skills that own them

Once FINDINGS has cleared every blocker, offer the advisory findings from `phil:review-code` to the
plugin skills that own them, so line numbers stop moving only after every blocker is settled. Read
`${CLAUDE_PLUGIN_ROOT}/skills/edd/references/repair.md` before offering anything: it holds the grouping,
each skill's argument and gate, and the clean-tree rule. Each repair runs only on the developer's `run`,
and the record keeps every repair offered, run or skipped.

## DOCUMENT — living documentation (every run in which BUILD started)

Write the trail under `docs/edd/<slug>/` for every run in which BUILD started, opt-out runs
included. If that directory already exists, append the date to the slug: never overwrite an earlier
trail; a run stopped over a standing reject writes the trail too, its verdicts included. Compose it and review its
prose before anything is written to disk:

```
docs/edd/<slug>/
  expectations.md   # each expectation + provenance + classification and its reason or blocker + routing + `trusted to the tests`
  evidence/         # the captured EXECUTED artifacts (verbatim) with their reproduce commands, one per expectation that has one
  verdicts.md       # per expectation: accept, reject, unproven (stopped), dropped by the developer (with their reason),
                    #   `trusted to the tests`, or a hand spot-check and its verdict
                    #   + timestamp + evidence reference; each challenge and the evidence it brought;
                    # the review's label, verdict and raised/confirmed/refuted counts; each confirmed finding,
                    #   and each waiver — FINDINGS' or DOCUMENT's fitness — with its reason and timestamp
  stabilize.md      # per accepted expectation and trusted row, the pinning test that pins it, `pinned, not run here`, or `pinned by nothing`
                    #   and why; every phil:review-code and phil:ux-review finding, blocking or advisory, every
                    #   `consider` included; each repair offered, run or skipped
```

and a durable summary at `docs/evolution/<date>-<slug>.md`, creating `docs/evolution/` if absent.

Read `${CLAUDE_PLUGIN_ROOT}/skills/edd/references/document.md` before composing: it holds the standards
to read, how `phil:red-team-prose` runs over the drafts, and what it may touch.

Report a summary naming, per expectation, the verdict and the evidence it rested on — or that it was
trusted to the tests, or dropped by the developer — and the test that now pins it.

A run that stops before BUILD writes **none** of this.

---

## Safety rules

- **Evidence by default.** Every expectation gets executed evidence, except a checkable one the
  developer trusts to the tests and one the developer spot-checks by hand because no agent can run it
  here or the agent has twice failed to. A qualitative expectation, or one an approval test pins, is
  never trusted to the tests.
- **The honesty rule in CLASSIFY.** Default checkable; mark qualitative, or not executable in the
  loop, only on a concrete reason the developer gives or a blocker the developer confirms.
- **Inherit, never re-implement.** Delegate the build and inherit the engine's oracle; run no check
  of your own in its place. A red oracle blocks done.
- **Executed evidence, producer ≠ builder, the developer adjudicates.** Narration is never
  evidence — a pass count included; the producer re-runs reused evidence; a rejected expectation
  blocks done.
- **The adversary advises; the developer decides.** A judge-confirmed `major`, after the judge's
  correction, blocks done until FINDINGS clears it by fix or a named waiver; no reviewer output is a
  verdict, and a draft signal is never a verified pass.
- **Every loop ends.** A second red oracle, narrated return, cannot-run, fix round or prose fix round,
  and a second consecutive unanswered ask, each go to the developer or end the run; every ask offers
  `stop`; a reject or challenge re-asks only on new evidence. Nothing re-commissions or rebuilds
  forever.
- **Pinned, reviewed and repaired to this plugin's standards.** Every accepted expectation is pinned
  by a test the engine writes to `rules/testing.md`, or blocks done — a spot-checked one until the
  developer waives it by name. `phil:review-code`'s Priority 1 findings, its Priority 6 findings on
  pinning tests, and `phil:ux-review`'s `must-fix` findings block done until FINDINGS clears them, a
  fix only on a re-run that does not reproduce the finding. Repairs run after every blocker clears,
  never over a pinning test with a skill that changes what it asserts.
- **Keep the developer's words, and the evidence.** A `you wrote` or `you edited` line stays as the
  developer wrote it, untouched by this skill and by a prose review; every file under `evidence/`
  stays byte-identical to its capture.
- **Compose to this plugin's writing standards.** Every document this skill composes — never the
  evidence — passes `phil:red-team-prose` before it reaches disk; a `[fitness]` finding blocks done
  until rewritten or waived by name.
- **Report honestly.** Grade the final state, not the effort. Report the run not done while any
  expectation is unmet or unproven.

---

## Self-test (regression gate)

`skills/edd/self-test/` holds golden fixtures pinning these behaviors: the opt-out covers checkable
expectations only (01), the honesty rule in classification (02), evidence reuse (03), commission from
a non-builder (04), narration rejection (05), blocked-done (06), the trail for every run that built
(07), scenario evidence for a checkable expectation (08), a pass count rejected as narration (09), an
expectation not executable in the loop (10), capture's coverage, size and risk checks (11), the
review before any verdict (12), a challenge that rebuilds nothing (13), an unwaived major finding
blocking done (14), a stop over a standing challenge (15), an unpinned expectation blocking done
(16), an approval test pinned to the accepted evidence (17), a Priority 1 review finding blocking
done while advisories go to their owners (18), a UI change audited by `phil:ux-review` (19), the
record reviewed with the evidence and the developer's words untouched (20), an engine that cannot
meet an expectation (21), and a challenge that tightens a vague expectation (22).
Whenever this skill, its `references/`, `commands/edd.md`, `agents/edd-evidence-producer.md`,
`agents/adversarial-reviewer.md` or `agents/adversarial-verifier.md` changes, drive the fixtures per
`self-test/README.md` and confirm each produces its `expected.md` decision. Every edit here is
non-monotonic: regression-test each change; never eyeball it.
