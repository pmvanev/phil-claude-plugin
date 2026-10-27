---
name: edd
description: Skill bundle for phil:edd command — Expectation-Driven Development, after Andrea Laforgia's protocol. Captures intent as expectations checked for coverage, size and risk; delegates the build to nwave or phil:work; gathers executed evidence for every expectation, from someone other than the builder, unless the developer trusts the tests for the checkable ones or spot-checks one no agent can run; and puts it to the developer to adjudicate.
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
> expectation not opted out) → ADJUDICATE (the developer) → DOCUMENT (every run that built).

---

## The two lines to hold

1. **A green suite the builder wrote is not proof.** Every expectation gets executed evidence by
   default. Two exceptions, both the developer's call and both recorded in as many words: they may
   trust the tests for the checkable expectations in a run, and they spot-check by hand an
   expectation no agent can run here. Never make either call for them.
2. **Never let the builder grade its own homework.** Evidence an agent returns must be **executed**
   (a real run or render captured verbatim, not a description) and produced by an agent that is
   **not** the builder; the **developer** is the final adjudicator. A hand spot-check is the one
   description allowed: the developer's own observation, never an agent's.

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
halves, which are `composed`. Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing, and
write every composed line to it — active voice, no needless words, one behaviour per line.

Ask the developer to confirm the list under `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`,
with the list itself in the context block, so the counted ask stays under its ceiling. The developer
may confirm, edit, accept or decline each suggestion. Do not proceed until the list is confirmed.

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
developer gives or confirms a **concrete reason**: one that names what about this expectation no
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

The ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`. Name the cost of each
answer: a yes leaves tests the builder wrote as the only proof for those expectations; a no gives
each one its scenario run, shown to the developer. **An ambiguous answer is a no** — this skill
overrides the standard's second ask here, because the safe default needs no answer.

- **No** — every expectation gets evidence.
- **Yes** — checkable expectations get no evidence; the engine's oracle alone proves them. The record
  names every expectation trusted to the tests: mark each of their rows in the classification table
  `trusted to the tests`.

Only checkable rows can be opted out — a row not executable in the loop has no tests to trust. Two
kinds of row cannot be opted out, whatever the answer:

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
stands. A red oracle blocks done: route the failing expectation back to the engine, as a reject
would — and after a second red oracle on the same expectation, put the failure to the developer, who
sends it back again or stops. An approval test still awaiting its first approval is not red: its
first output goes to the developer at EVIDENCE. Record which engine built. The evidence below adds what the oracle cannot give the developer:
the scenario's real inputs and output in front of their eyes.

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
   DELIVER demo, a captured transcript of the behaviour itself — the builder made it — so dispatch the producer to
   re-run its reproduce command and capture what that emits. That costs one run and keeps the
   evidence out of the builder's hands. A test-suite run is not reusable evidence: re-running it
   yields a pass count, which step 3 rejects. (Whether the existing evidence is actually *relevant* is the
   developer's call at ADJUDICATE, not this skill's — if they say it isn't, commission fresh evidence
   and rebuild nothing: the thing itself was never judged.)
2. **Otherwise commission it — from a non-builder.** Dispatch `phil:edd-evidence-producer` (Agent/Task)
   with the `expectation`, its `classification`, the `target` and any `context` its contract names,
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
   Never adjudicate against narration. When re-commissioning, name the scenario to run and send no
   `context`, so the producer runs the behaviour, not the suite. On a second narrated return for the
   same expectation, stop re-commissioning and put both returns to the developer, who names the
   scenario to try, spot-checks it by hand, or stops.
4. **A producer that cannot run it.** A producer that reports it *cannot produce executed evidence*
   has given neither evidence nor narration: report it to the developer rather than re-commissioning,
   since the same run fails the same way, and act on its cause:
   - **the build is missing** — an entry point not found, a build absent: route the expectation back
     to the engine, then gather evidence again; after a second cannot-run for the same build, ask the
     developer to send it back again, spot-check it by hand, or stop;
   - **the environment cannot run it** — a browser, a paid API, a production-only condition: tell the
     developer, who confirms it as a blocker and spot-checks it by hand or stops, as above.

The output, per expectation, is an **executed artifact + its reproduce command**, a recorded opt-out,
or a recorded hand spot-check — ready for the developer.

## ADJUDICATE — the human decides

Put each expectation's evidence to the developer via the human-approval port (AskUserQuestion +
optional review of the artifact in their editor), in risk order. Skip rows trusted to the tests: the
engine's oracle decided them.

**This ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the call.

- **The evidence is the context block, verbatim and unsummarised.** It is the thing being judged, so
  paraphrasing it into the ask both breaks the word limit and replaces what the developer is meant to
  read. The counted ask names the expectation in plain terms and says what accepting commits to.
- **Two verdicts, and neither is a default.** `accept` and `reject` are the verdicts. The ask also
  offers `stop`, and accepts a reply that the evidence does not show the expectation (below). An
  ambiguous reply is unanswered, and a second unanswered ask ends the run, reported not done, rather
  than passing it.

The developer — never this skill, never the producer — renders the verdict: **accept** or **reject**.
A hand spot-check ends in a verdict too: the developer accepts or rejects on what they observed. The
developer's reject outranks a green oracle: the oracle checks what the test asserts, the developer
what they meant.

- **accept** → the expectation is met; record the verdict.
- **reject** → the expectation is **not** met. **Block done.** Route that expectation back to the
  engine to change the thing, then gather evidence again and re-adjudicate. Never move on, never
  drop a rejected expectation, and never report the run done while any expectation stands
  rejected. Grade the final state, not the effort. The developer may stop instead: record the standing
  reject and report the run **not done**.

A reply that the evidence does not show this expectation — the wrong scenario, irrelevant reused
evidence — is not a reject: the thing itself was never judged. Commission fresh evidence and rebuild
nothing. A stop over an unproven expectation is reported not done, the expectation recorded as
unproven.

## DOCUMENT — living documentation (every run that built)

Write the trail under `docs/edd/<slug>/` for every run that built, opt-out runs included — a run
stopped over a standing reject writes the trail too, its verdicts included:

```
docs/edd/<slug>/
  expectations.md   # each expectation + provenance + classification + routing + `trusted to the tests`
  evidence/         # the captured EXECUTED artifacts (verbatim), one per expectation that has one
  verdicts.md       # per expectation: accept/reject, `trusted to the tests`, or a hand spot-check and its verdict + timestamp + evidence reference
```

and a durable summary at `docs/evolution/<date>-<slug>.md`, creating `docs/evolution/` if absent.
Report a summary naming, per expectation, the verdict and the evidence it rested on — or that it was
trusted to the tests.

A run that stops before BUILD writes **none** of this.

---

## Safety rules

- **Evidence by default.** Every expectation gets executed evidence, except a checkable one the
  developer trusts to the tests and one no agent can run that the developer spot-checks by hand. A
  qualitative expectation, or one an approval test pins, is never trusted to the tests.
- **The honesty rule in CLASSIFY.** Default checkable; mark qualitative, or not executable in the
  loop, only on a developer-confirmed concrete reason or blocker.
- **Inherit, never re-implement.** Delegate the build and inherit the engine's oracle; never
  re-run a check of your own in its place. A red oracle blocks done.
- **Executed evidence, producer ≠ builder, the developer adjudicates.** Narration is never
  evidence — a pass count included; reused evidence is re-run by the producer; a rejected expectation
  blocks done.
- **Every loop ends.** A second red oracle, a second narrated return, a second cannot-run and a
  second unanswered ask each go to the developer or end the run, and the developer may always stop;
  nothing re-commissions or rebuilds forever.
- **Keep the developer's words.** A `you wrote` line is never edited.
- **Report honestly.** Grade the final state, not the effort. Never claim done over an unmet or
  unproven expectation.

---

## Self-test (regression gate)

`skills/edd/self-test/` holds golden fixtures pinning these behaviors: the opt-out covers checkable
expectations only (01), the honesty rule in classification (02), evidence reuse (03), commission from
a non-builder (04), narration rejection (05), blocked-done (06), the trail for every run that built
(07), scenario evidence for a checkable expectation (08), a pass count rejected as narration (09), an
expectation not executable in the loop (10), and capture's coverage, size and risk checks (11).
Whenever this skill, `commands/edd.md`, or `agents/edd-evidence-producer.md` changes, drive the
fixtures per `self-test/README.md` and confirm each produces its `expected.md` decision — every edit
here is non-monotonic, so the skill is changed and regression-tested, never changed and eyeballed.
