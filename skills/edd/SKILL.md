---
name: edd
description: Skill bundle for phil:edd command — Expectation-Driven Development, after Andrea Laforgia's protocol. Captures intent as expectations checked for coverage, size and risk; delegates the build to nwave or phil:work; gathers executed evidence for every expectation, from someone other than the builder, unless the developer trusts the tests for the checkable ones or spot-checks one no agent can run; has an independent adversary review the work; and puts evidence and findings to the developer to accept, reject, challenge or stop.
---

# EDD — Expectation-Driven Development

Run Andrea Laforgia's Expectation-Driven Development protocol over a developer's intent: write the
**expectations**, hand the build to the fitting engine, gather **executed evidence** that each one
holds, and put that evidence to the developer, who decides. The protocol's source:
<https://a4al6a.substack.com/p/expectation-driven-development-a>.

This is the **expectation-driven sibling to `phil:work`**. `phil:work` is the general contractor for
invisible work (preserve behavior + hit a checkable goal); this is the contractor for
expectation-driven work: **frame the expectations → delegate the build to the fitting engine →
gather executed evidence for each expectation → the developer adjudicates → leave a trail.**

The standards to work under are `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`, `${CLAUDE_PLUGIN_ROOT}/rules/testing.md`, and
`${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`.

> **The full flow.** CAPTURE (intent → expectations, checked for coverage, size and risk) → CLASSIFY
> (which kind of evidence) → OPT-OUT (trust the tests for the checkable ones this run?) → BUILD
> (delegate to one engine, inherit its oracle) → EVIDENCE (executed, producer ≠ builder, for every
> expectation not opted out) → REVIEW (an independent adversary, its findings judged) → ADJUDICATE
> (the developer accepts, rejects, challenges or stops) → FINDINGS (clear each confirmed major) →
> DOCUMENT (every run that built).

---

## The two lines to hold

1. **A green suite the builder wrote is not proof.** Every expectation gets executed evidence by
   default. Two exceptions, both the developer's call and both recorded in as many words: they may
   trust the tests for the checkable expectations in a run, and they spot-check by hand an
   expectation no agent can run here, or one the agent has twice failed to run. Never make either
   call for them.
2. **Never let the builder grade its own homework.** Evidence an agent returns must be **executed**
   (a real run or render captured verbatim, not a description) and produced by an agent that is
   **not** the builder; the **developer** is the final adjudicator. A hand spot-check is the one
   description allowed: the developer's own observation, never an agent's.

---

## Every ask

Every question this skill puts to the developer — CAPTURE's confirmation, OPT-OUT, EVIDENCE's
spot-check, ADJUDICATE, FINDINGS — follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.
Load it before the first ask. On top of that standard:

- **Every ask offers `stop`.** A stop before BUILD ends the run and writes nothing; a stop after BUILD
  writes the trail as it stands and reports the run not done.
- **Unanswered.** An ambiguous or empty reply is unanswered, and two consecutive unanswered asks end
  the run, reported not done — this skill overrides the standard's "treat it as a decline", because a
  decline has no meaning for most of these asks. OPT-OUT alone treats an ambiguous reply as a no.
- **Caps.** Every "second" cap in this skill — a second red oracle, narrated return, cannot-run, fix
  round, reject or challenge — means the second and every one after it.
- **Free text.** An answer that needs words — a challenge's scenario, a reject's reason, a waiver's
  reason — comes through the ask's "Other" field or one follow-up ask; an empty follow-up is
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

Derive a kebab-case `<slug>` from the intent for the trail path `docs/edd/<slug>/` — but do **not**
create it yet (the trail is written only once the engine has built; see DOCUMENT).

---

## CAPTURE — intent → expectations

Restate the intent as a list of discrete **expectations**, each a single statement of something the
developer expects to be true when the work is done. Surface qualitative ones explicitly (tone,
clarity, ergonomics, "helpful", "feels X").

Before showing the list, check it the way the article asks:

- **Coverage.** Name each of these categories that no expectation covers, and offer a suggestion
  for each gap:
  - the **happy path**;
  - **past edge cases** — the bugs this area has had before. Ask the developer, or search the
    history (`git log`, the issue tracker, tests that pin old bugs); never invent a past bug;
  - **non-functional requirements** the intent implies — performance, security, limits;
  - behaviour that **must not happen** — what the change must never do: break existing behaviour,
    lose or leak data, act without being asked. An expectation that existing behaviour stays
    unchanged covers this category.
- **Size.** One expectation is one behaviour the developer could explain to a colleague in a single
  breath. Propose splitting any that takes more than one breath — it will classify and route
  differently — and expanding any too thin to test.
- **Risk.** Order the list by risk, worst first: rank by what a miss would cost — how many users it
  hits, and how hard it is to undo. Evidence and adjudication follow this order, so the developer's
  attention goes where a miss would cost most.

Label every line with its provenance:

- `you wrote` — the developer's words, kept exactly as written; never edit one to fit a standard;
- `composed` — a restatement, suggestion or split this skill wrote;
- `you edited` — a composed line the developer then changed; their edit stands as written.

For a split of a `you wrote` line, keep the original `you wrote` line in the record beside the
halves, which are `composed`; the halves are the live expectations, the original a record of what
the developer said. Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing, and
write every composed line to it — active voice, no needless words, one behaviour per line.

Ask the developer to confirm the list, with the list itself in the context block, so the counted ask
stays under its ceiling. The developer may confirm, edit, accept or decline each suggestion, or stop.
Do not proceed until the list is confirmed.

---

## CLASSIFY — which kind of evidence

Classification decides what the evidence for each expectation must show.

- **checkable** — the target engine's native oracle can produce a pass/fail result at reasonable
  cost:
  - **nwave** (user-facing behavior) → an acceptance test can assert it (deterministic observable
    output: stdout/response/exit code/state).
  - **phil:work** (invisible / developer-facing) → a checkable metric (coupling, complexity, a
    benchmark, a dead-link / frontmatter / citation check).

  Its evidence is the **scenario actually run** — see EVIDENCE.
- **qualitative** — asserting it would require encoding a **subjective judgment** (helpful, clear,
  ergonomic, aesthetic) that no cheap deterministic assertion captures. Its evidence is the thing run
  or rendered for the developer's taste.
- **not executable in the loop** — nothing in this run can exercise it: a rendered UI no agent can
  watch, a rate-limited or paid third-party API, a production-only condition. Its evidence is the
  developer's own spot-check — see EVIDENCE. An expectation the engine's tests can exercise, even
  with part of it mocked, is checkable, not this.

**The honesty rule.** Default every expectation to **checkable**. Mark one qualitative only when the
developer gives a **concrete reason**: one that names what about this expectation no
assertion captures. Ask "what specifically can't a test assert here?" and never supply the reason
yourself. Mark one not executable in the loop only when the developer confirms the concrete blocker —
what stops anything in this run from exercising it. Both other kinds take evidence away from the
default, so neither is this skill's call.

**Test two patterns against a stated reason before accepting it.** Read
`${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` before classifying: it names two patterns that make a
hard-to-assert output checkable. A **property-based test** asserts a rule over generated inputs where
no single example captures it. An **approval test** pins a large output: a human reads it once, and
every later run is a diff. Neither captures a subjective judgment such as "helpful", but both remove
"too large or too varied to assert" as a reason — an expectation either one can assert is checkable.
**An approval test's first approval is still a human read**: name it in the classification table, as
the step that comes before any diff means anything.

Produce a **classification table**: each expectation → `checkable` (with the engine + its native
oracle, and `approval test` where one pins it), `qualitative` (with the developer's concrete reason),
or `not executable in the loop` (with the developer-confirmed blocker).

> Split within one expectation: if an expectation has a cheaply-assertable core (e.g. "fails with a
> non-zero exit and names the path") plus a wrapper someone offers as qualitative ("...and the
> message is helpful"), propose splitting it in two. The core is checkable; the remainder is
> checkable too unless the developer gives a concrete reason under the honesty rule. The halves are
> `composed`; put them to the developer to confirm and slot them into the risk order.

---

## OPT-OUT — trust the tests for the checkable ones?

Ask once, after the developer has seen the classification table, whether to trust the engine's
tests for this run's **checkable** expectations. Skip the ask when no row can be opted out: nothing
turns on it.

Name the cost of each answer: a yes leaves tests the builder wrote as the only proof for those
expectations; a no gives each one its scenario run, shown to the developer. **An ambiguous answer is
a no** — this skill overrides the standard's second ask here, because the safe default needs no
answer.

- **No** — every expectation gets evidence.
- **Stop** — end the run before anything is built.
- **Yes** — checkable expectations get no evidence; the engine's oracle alone proves them. The record
  names every expectation trusted to the tests: mark each of their rows in the classification table
  `trusted to the tests`.

Only checkable rows can be opted out — a row not executable in the loop has no tests to trust. A row
whose oracle the table cannot name as a concrete assertion cannot be opted out either: the honesty
rule makes it checkable by default, but no test yet proves it. Two more kinds of row cannot be opted
out, whatever the answer:

- A qualitative expectation cannot be opted out: no test asserts it, so the developer's judgment on
  executed evidence is the only proof it has.
- An expectation an approval test pins cannot be opted out: the test has no baseline until a human
  approves its first output, and the builder must not approve its own. Its evidence is that first
  output, put to the developer.

---

## BUILD — delegate to one engine, inherit its oracle

Delegate the actual build to the fitting engine and let its native oracle prove the checkable
expectations:

- **user-facing behavior** → nwave (its acceptance-test run is the oracle);
- **invisible / developer-facing** → `/phil:work` (its preservation floor + checkable goal is the oracle).

This skill runs one engine per run. If the expectations need both, say so and split the intent into
two runs, one per engine, with the developer's agreement; sequencing across engines is not supported.

Run no preservation or acceptance check of your own — that is the engine's job, and its verdict
stands. Capture its run verbatim as `oracle_result` — the output, not the engine's summary of it —
replaced on every rebuild; when the engine returns no oracle run, record that none exists. A red
oracle blocks done: route the failing expectation back to the engine, as a reject would — and after
a second red oracle on the same expectation, put the failure to the developer, who sends it back
again or stops. An approval test still awaiting its first approval is not red: its first output goes
to the developer at EVIDENCE. Record which engine built. The evidence below adds what the oracle
cannot give the developer: the scenario's real inputs and output in front of their eyes.

A rebuild re-runs REVIEW on the whole target — a reject, a red oracle or a FINDINGS fix sends the work
back to the engine — and re-asks every expectation whose evidence the change touched: re-gather that
evidence, review, and put it to the developer again. An accept on evidence the rebuild invalidated no
longer stands. A waiver stands only while its finding's span is unchanged.

## EVIDENCE — executed evidence for every expectation not opted out

Skip every expectation trusted to the tests. Gather evidence for the rest in the risk order CAPTURE
set.

**An expectation not executable in the loop** dispatches nothing: handle it in its place in the risk
order, without reaching the steps below. Commission nothing for it. Tell the developer
the confirmed blocker and ask them to spot-check it by hand or stop. Record which they chose and, for
a spot-check, what they observed, in their own words, labelled `you wrote`. A spot-check goes to
ADJUDICATE like any other evidence.

For every other expectation, do the least that yields real evidence:

1. **Reuse if it already exists.** If the engine already produced relevant executed evidence — a
   DELIVER demo, a captured transcript of the behaviour itself — the builder made it. Dispatch the
   producer (step 2) with that artifact as `context`, to re-run its reproduce command and capture
   what that emits. That costs one run and keeps the evidence out of the builder's hands. A
   test-suite run is not reusable evidence: re-running it yields a pass count, which step 3 rejects.
   (Whether the existing evidence is actually *relevant* is the developer's call at ADJUDICATE, not
   this skill's — if they say it isn't, commission fresh evidence and rebuild nothing: the thing
   itself was never judged.)
2. **Otherwise commission it — from a non-builder.** Dispatch `phil:edd-evidence-producer` (Agent/Task)
   with the `expectation`, its `classification`, the `target`, any named `scenario` and any `context`
   its contract names,
   to actually run or render the thing and capture the raw output **verbatim** with the command that
   reproduces it. The producer is a **different actor than whatever built the thing** — it has no
   Edit or Write tool, and its contract forbids changing what it runs against. This separation of
   powers is non-negotiable; it is the whole reason the gate exists.
   - For a **checkable** expectation, the evidence is one scenario run: its inputs and the verbatim
     output, with the reproduce command.
   - For a **qualitative** expectation, it is the thing run or rendered, captured verbatim.
   - For a checkable expectation an **approval test** pins, it is the test's first output.
3. **Reject narration.** If what comes back (from either path) is a description, a summary, or a
   claim with no reproducible artifact, it is **narration, not evidence** — the article calls it
   *generative* evidence. Reject it and re-commission a real run. A test runner's `"all tests passed"`,
   or a pass count, is narration for this gate: it reports a verdict without showing the behaviour.
   Never adjudicate against narration. When re-commissioning, name the scenario to run as `scenario`
   and send no `context`, so the producer runs the behaviour, not the suite. On a second narrated return for the
   same expectation, stop re-commissioning and put both returns to the developer, who names the
   scenario to try, spot-checks it by hand, or stops.
4. **A producer that cannot run it.** A producer that reports it *cannot produce executed evidence*
   has given neither evidence nor narration: report it to the developer rather than re-commissioning,
   since the same run fails the same way, and act on its cause:
   - **the build is missing** — an entry point not found, a build absent: route the expectation back
     to the engine, then gather evidence again; after a second cannot-run for the same expectation, ask
     the developer to send it back again, spot-check it by hand, or stop;
   - **the environment cannot run it** — a browser, a paid API, a production-only condition: tell the
     developer, who confirms it as a blocker and spot-checks it by hand or stops, as above.

The output, per expectation, is an **executed artifact + its reproduce command**, a recorded opt-out,
or a recorded hand spot-check — ready for the developer.

## REVIEW — an independent adversary attacks the work

Before any verdict, put the built work in front of an adversary — the article's second agent auditing
the first. Read `${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/SKILL.md` and compose its agents under
the contract it documents:

1. **Curate the input** as exactly `{ target, intent, standards, oracle_result? }`:
   - `target` — what the engine built: the changed source, test and prose files, and the entry points
     the evidence ran — excluding the engine's own logs, plans, notes and commit messages, which carry
     the builder's reasoning;
   - `intent` — the confirmed expectations, in risk order, each with its classification;
   - `standards` — for code, `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`,
     `${CLAUDE_PLUGIN_ROOT}/rules/testing.md` and `${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`, plus
     `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` when tests changed; for prose,
     `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` and any rule the prose is about;
   - `oracle_result` — the run BUILD captured, inherited, never re-run; omitted when none exists.

   Pass the machine-produced oracle run, never the builder's reasoning, its self-assessment, or a
   claim that the tests pass.
2. **Dispatch `phil:adversarial-reviewer`** (Agent/Task) with that input. It returns a typed verdict;
   rewrite nothing in it.
3. **Verify each finding** by dispatching `phil:adversarial-verifier`, one fresh dispatch per finding,
   with `{ finding, target, intent, standards, oracle_result? }` and without the reviewer's
   justification, confidence or other findings. Keep the findings the judge confirms, applying any
   `corrected_severity`. List separately the refutes the judge marks as could-not-establish with low
   `confidence`. Count the rest of the refutes and drop them.

Route on the typed fields only, and re-judge nothing:

- **The label and verdict lead.** The developer's first ask opens its context block with the
  reviewer's `overall_label` (`sound-gate` or `draft-signal`), its `verdict`, and "raised N, confirmed
  M, refuted K", then the could-not-confirm list. Report `clean` with its label — a draft signal is not
  a verified pass — and `cannot-assess` as exactly that, never as approval.
- **Severity after the judge's `corrected_severity`.** A judge-confirmed `major` finding blocks done
  until the engine fixes it, or the developer waives it by name, with a reason the record keeps — both
  in FINDINGS. A confirmed `minor` or `nit` advises.

Attach a confirmed finding to an expectation only where its `span` or `evidence` names that
expectation's entry point or scenario; the developer sees it in that expectation's ask. Every other
confirmed finding — and every finding on a row trusted to the tests — goes to FINDINGS. The review
advises; the developer still decides every verdict.

## ADJUDICATE — the human decides

Put each expectation's evidence to the developer via the human-approval port (AskUserQuestion +
optional review of the artifact in their editor), in risk order. Skip rows trusted to the tests: the
engine's oracle decided them.

- **The evidence and its attached findings are the context block, verbatim and unsummarised.** They
  are the thing being judged, so paraphrasing them into the ask both breaks the word limit and
  replaces what the developer is meant to read. Open an artifact too long for the context block in
  the developer's editor instead, and say so.
- **Then the article's four challenge questions in the context block**, after the evidence: *Do the
  numbers add up? Were the edge cases actually run? What input would break it? What scenario is
  missing?* They are prompts for the developer's reading, not a separate ask.
- **Four answers, and none is a default.** `accept`, `reject`, `challenge` and `stop` are the answer
  set. Name each answer's cost in its description: accept closes this expectation on this evidence;
  reject costs a rebuild, a re-review and a new round; challenge costs another evidence run and no
  rebuild; stop ends the run not done, with the trail written.

The developer — never this skill, never the producer, never the reviewer — renders the verdict. A hand
spot-check ends in a verdict too: the developer accepts or rejects on what they observed. The
developer's reject outranks a green oracle: the oracle checks what the test asserts, the developer
what they meant.

- **accept** → the expectation is met; record the verdict.
- **reject** → the expectation is **not** met. **Block done.** Take the developer's reason, route the
  expectation back to the engine to change the thing, and follow BUILD's rebuild rule. Never move on,
  never drop a rejected expectation, and never report the run done while any expectation stands
  rejected. Grade the final state, not the effort. The developer may stop instead: the reject stands,
  recorded.
- **challenge** → the evidence is not enough; the thing itself was never judged, so a challenge is
  not a reject. The developer names the scenario to run, or an expectation to add.
  - A challenge commissions evidence for the named scenario and rebuilds nothing. The producer
    receives it as `scenario`; the evidence goes
    through EVIDENCE's steps, and back to this ask with its findings already attached.
  - A challenge on a spot-checked expectation asks the developer to spot-check the named scenario.
  - A challenge that adds an expectation sends it through CLASSIFY, labelled `you wrote`, into its
    place in the risk order; it gets evidence whatever OPT-OUT said, since the opt-out never saw it.
    Before its ask, re-run REVIEW with the added expectation in its intent.
  - A reply that the evidence does not show this expectation — the wrong scenario, irrelevant reused
    evidence — is a challenge: commission fresh evidence and rebuild nothing.
- **stop** → end the run. Record every standing reject, challenge and unproven expectation as it
  stands, write the trail, and report the run **not done**. A stop over an unproven expectation is
  reported not done, the expectation recorded as unproven.

A reject or challenge re-asks only on new evidence. After a second reject or a second challenge on the
same expectation, say so in the next ask and recommend stop; the developer may go on.

## FINDINGS — clear each confirmed major

Once every expectation put to the developer is accepted — rows trusted to the tests are never put —
put each unwaived confirmed `major` to the developer — those attached to an expectation, those on
rows trusted to the tests, and those bearing on none — with its span, mechanism and evidence in the
context block. Three answers, `fix`, `waive` and `stop`, each with its cost:

- **fix** — route the finding to the engine and follow BUILD's rebuild rule; costs a rebuild, a
  re-review and a re-ask of every expectation the change touched.
- **waive** — take the developer's reason; record the finding, the reason and a timestamp. Done is no
  longer blocked by it, while its span is unchanged.
- **stop** — end the run not done, with the finding recorded as standing.

Treat a finding in a later review as the same finding when its span names the same lines and its
mechanism the same defect: it keeps its fix-round count, and a waived one stays waived. After a
second fix round on the same finding, offer only `waive` and `stop`: the engine has failed it twice. List the confirmed `minor` and `nit` findings after the majors; the developer may send any of
them to the engine as a `fix`, and the record keeps each one either way.

## DOCUMENT — living documentation (every run that built)

Write the trail under `docs/edd/<slug>/` for every run that built, opt-out runs included — a run
stopped over a standing reject writes the trail too, its verdicts included:

```
docs/edd/<slug>/
  expectations.md   # each expectation + provenance + classification and its reason or blocker + routing + `trusted to the tests`
  evidence/         # the captured EXECUTED artifacts (verbatim) with their reproduce commands, one per expectation that has one
  verdicts.md       # per expectation: accept, reject, unproven (stopped), `trusted to the tests`, or a hand spot-check and its verdict
                    #   + timestamp + evidence reference; each challenge and the evidence it brought;
                    # the review's label, verdict and raised/confirmed/refuted counts; each confirmed finding,
                    #   and each waiver with its reason and timestamp
```

and a durable summary at `docs/evolution/<date>-<slug>.md`, creating `docs/evolution/` if absent.
Report a summary naming, per expectation, the verdict and the evidence it rested on — or that it was
trusted to the tests.

A run that stops before BUILD writes **none** of this.

---

## Safety rules

- **Evidence by default.** Every expectation gets executed evidence, except a checkable one the
  developer trusts to the tests and one the developer spot-checks by hand because no agent can run it
  here or the agent has twice failed to. A
  qualitative expectation, or one an approval test pins, is never trusted to the tests.
- **The honesty rule in CLASSIFY.** Default checkable; mark qualitative, or not executable in the
  loop, only on a concrete reason the developer gives or a blocker the developer confirms.
- **Inherit, never re-implement.** Delegate the build and inherit the engine's oracle; never
  re-run a check of your own in its place. A red oracle blocks done.
- **Executed evidence, producer ≠ builder, the developer adjudicates.** Narration is never
  evidence — a pass count included; reused evidence is re-run by the producer; a rejected expectation
  blocks done.
- **The adversary advises; the developer decides.** A judge-confirmed `major`, after the judge's
  correction, blocks done until FINDINGS clears it by fix or a named waiver; no reviewer output is ever
  a verdict, and a draft signal is never a verified pass.
- **Every loop ends.** A second red oracle, a second narrated return, a second cannot-run, a second
  fix round and a second consecutive unanswered ask each go to the developer or end the run; every ask
  offers `stop`; a reject or challenge re-asks only on new evidence. Nothing re-commissions or rebuilds
  forever.
- **Keep the developer's words.** A `you wrote` line is never edited.
- **Report honestly.** Grade the final state, not the effort. Never claim done over an unmet or
  unproven expectation.

---

## Self-test (regression gate)

`skills/edd/self-test/` holds golden fixtures pinning these behaviors: the opt-out covers checkable
expectations only (01), the honesty rule in classification (02), evidence reuse (03), commission from
a non-builder (04), narration rejection (05), blocked-done (06), the trail for every run that built
(07), scenario evidence for a checkable expectation (08), a pass count rejected as narration (09), an
expectation not executable in the loop (10), capture's coverage, size and risk checks (11), the
review before any verdict (12), a challenge that rebuilds nothing (13), an unwaived major finding
blocking done (14), and a stop over a standing challenge (15).
Whenever this skill, `commands/edd.md`, `agents/edd-evidence-producer.md`,
`agents/adversarial-reviewer.md` or `agents/adversarial-verifier.md` changes, drive the
fixtures per `self-test/README.md` and confirm each produces its `expected.md` decision — every edit
here is non-monotonic, so the skill is changed and regression-tested, never changed and eyeballed.
