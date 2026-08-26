# Slice 02 — The three failure modes become fixtures

**Goal:** Pin the three measured ways a decision request goes wrong, so each is caught by a test rather
than rediscovered by a reader.

**Stories:** S3 (see a malformed ask actually fail)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D4] — the hard ceiling** — if the count cannot be applied to a real request without either
evicting what turns on it or forcing the decision to be split. [D4] is the largest untested commitment in
the feature: a hard ceiling that starts squeezing framing is being applied backwards, and the honest
outcome would be to reopen it as a target with the mechanism cost stated.

**Disproves [D9] — placement is part of the standard** — if *buried* cannot be pinned at all. Modes 1 and
2 are wording and are obviously testable. Mode 3 is placement, and it is entirely possible that no fixture
can express "correct wording, wrong position" in a way a check can read. If so, [D9] is a sentence rather
than a clause, and the standard covers two thirds of the reported problem — which must be stated, not
quietly dropped.

**Confirms**, if it passes, that all three reported failures are regression-testable, which is what
separates this from the prose that already failed.

## IN scope

- Fixture *bare-option-list* — options present, framing absent. Fails.
- Fixture *jargon-wall* — internal vocabulary inside the ask. Fails.
- Fixture *buried-ask* — wording that would pass, placed inside surrounding output. Fails **on placement**.
- Fixture *conforming* — passes all three checks.
- The word-count assertion from slice 01, generalised to run over any fixture.
- **A fixture whose ask genuinely needs a detail block** — added by slice 01's result. [D5] is
  currently unproven: the one real conforming ask fit 143 words and displaced nothing downward, so the
  clause that makes the hard ceiling affordable has no instance behind it.
- **A ruling on ask/detail ORDERING** — also from slice 01. The fragment says detail *"sits below"*; the
  one real instance put its jargon-bearing context *above* and read better for it. The distinction may be
  establishing-context (above) vs supporting-detail (below), which the fragment does not draw. Either draw
  it or delete the positional claim.
- A decision, recorded, on whether fixtures live beside the fragment in `skills/shared/` or in a
  `self-test/` directory — `skills/shared/` holds no fixtures today, so this slice sets the precedent
  either way and should set it knowingly (feature delta, *Open* item 1).

## OUT of scope

- Propagation to other askers and the check script — slice 03.
- The conversational half — slice 04.
- Any attempt to detect these modes automatically in live output. The fixtures pin the **standard**, not a
  linter over conversation; conflating the two would promise enforcement [D11] says does not exist.

## Acceptance criteria

- **AC1** Fixture *bare-option-list* fails, and its failure names the missing framing rather than a count.
- **AC2** Fixture *jargon-wall* fails, and names at least one forbidden token by category.
- **AC3** Fixture *buried-ask* fails **on placement**, with wording that passes AC1 and AC2 — this is the
  fixture that decides [D9].
- **AC4** Fixture *conforming* passes all three checks and the count.
- **AC5** The count runs on slice 01's real recorded request, not a synthetic one.
- **AC6** Each fixture is proven to fail **before** the check is trusted — `CLAUDE.md`'s standing rule,
  written after `check-readonly-commands.py`'s first version silently passed.
- **AC7** If AC3 cannot be met, that is recorded in the Result section and [D9] is amended in the feature
  delta rather than left standing.
- **AC8** One fixture's ask requires a detail block, and that block carries tokens the ask may not —
  proving [D5] is a used clause rather than an unexercised escape hatch.
- **AC9** The ordering question is settled in the fragment: either the establishing/supporting
  distinction is drawn, or *"sits below"* is removed as an overclaim.

## Dependencies

**Slice 01** — needs the fragment to test against and its real recorded request for AC5. Slice 01's
result also added AC8 and AC9 to this brief; read its *AC5 failed* section before starting.

## Effort · reference class

**≤1 day.** Reference class: `groom-issues` self-test fixture additions, and `board-setup-block` slice 04
(a taxonomy pinned by fixtures, one day). Three fixtures plus one generalised assertion.

## Pre-slice SPIKE

**Consider one, timeboxed to an hour, for AC3 only.** Whether "correct wording, wrong placement" is
expressible as a fixture is a genuine unknown, and it is the one thing here that could fail for a
structural reason rather than a work reason. A cheap probe before committing the slice is worth it; if it
comes back negative the slice still ships modes 1 and 2 and amends [D9].

---

## Result — 2026-08-26

**Shipped.** Six fixtures, four mechanical checks, twelve mutation-proven reds. Both learning hypotheses
fired, and they landed on opposite sides.

### The hypothesis that fired: [D4] was refuted, then repaired

The brief said this slice would disprove [D4] *"if the count cannot be applied to a real request without
either evicting what turns on it or forcing the decision to be split"*, and named that the largest
untested commitment in the feature. It could not be applied. Under slice 01's revised scope — framing
plus every option label and description, summed — the three real requests this standard was written from
measure **564, 324 and 441** words against a limit of 200. Fixture 01, filed by slice 01 as the
*conforming baseline* at 143 words, is one of them: it measures 564.

The brief anticipated the honest outcome as *"reopen it as a target with the mechanism cost stated"*.
**That is not what happened, and the reason matters.** The same measurement showed both halves were
consistently sized and only their sum impossible — framings of 143/142/148, twenty options at 24–66. So
the scope was wrong, not the number. Put to the user with four options and their costs; **two limits of
200, both hard** was chosen, the three alternatives declined with reasons recorded in [D4].

Then calibrated against the whole corpus rather than three points: of **134** real questions, **128** fit
the per-question limit and the six that fail run 205–266. Tight, attainable, and the prescribed remedy
closes all six without touching a cost statement.

**AC5 is satisfied more strongly than it asked.** It required the count to run on slice 01's real
recorded request. Slice 01 could not fully honour it — the reviewer's finding was that its `ask.md`
"contains no options at all", so 143 was a framing-only figure filed against an ask-wide ceiling. The
option text was never lost, only never captured: all nine options were recovered **verbatim** from the
session log and are now `options.json`. `ask.md` is untouched.

### The hypothesis that did not fire: [D9] stands, and is now load-bearing

The brief allowed that *buried* might not be pinnable at all, in which case placement was a sentence and
the standard covered two thirds of the reported problem. **AC3 is met, by a real ask.** Fixture
`04-the-buried-ask` fails on placement and nothing else: three framing elements present, zero forbidden
tokens, framing 142 of 200, its one question 182 of 200 — emitted after a report and a six-row table
with no separator. `test_placement_is_isolated_by_exactly_one_fixture` asserts the isolation by name, so
widening any other check reports itself rather than dissolving the clause. AC7 does not apply.

### Every fixture is a real recording

The brief's reference class assumed synthetic fixtures. All six are extracted verbatim from this
machine's session logs — 33 sessions, 72 real decision requests, 134 questions — each naming its log and
timestamp so it can be re-extracted. A synthetic ask is written by whoever is also writing the standard,
so it demonstrates intent rather than testing it.

The corpus also settled a question the brief did not ask: **the three failure modes co-occur.** Three of
the six fixtures fail three or four ways at once. So the suite asserts the exact finding **set** per
fixture, not "some finding fired" — which would pass with two checks broken.

### AC8 and AC9, added to this brief by slice 01's result

- **AC8 met, by a real instance.** [D5] had been *unproven* since slice 01: the clause that makes a hard
  ceiling affordable had no ask behind it. Fixture `05-the-context-block` is a real three-part ask whose
  53-word context block carries an artifact path — a token the counted ask may not hold — above a marker
  line, repeated nowhere in the ask. **This was the open question the session was resumed to settle**, and
  the answer is yes: a conforming ask can genuinely need a context block, and one already existed.
- **AC9 landed early, in slice 01's review round.** *"Sits below"* was deleted and replaced with *context
  goes above* plus the reason, so there was no positional claim left to draw a distinction inside.
  Recorded here rather than re-litigated.

### The mechanism, and the two things it cost

Placement is unreadable from raw output — measured: the paragraph immediately before the call runs ≤82
words in **70 of 72** asks, the two exceptions being this feature's own deliberately-framed asks. So a
placement fixture records a **tagged emission** (`context` / `marker` / `interrupted` / `decision` /
`consequence` / `call`), with `ask.md` required to be exactly the concatenation of the framing regions.

Two costs, both stated in the register rather than discovered later:

1. **The tagging is a reading**, exercised once and recorded. So `BARE-LIST` fires on an element that is
   *absent*, never on one present and weak.
2. **A multi-decision framing cannot be tagged at all.** Fixture 01 is exactly that — three parallel
   decisions, each stating its consequence inline — so it records no emission and says so in
   `placement_not_asserted`. A limit of the format, found by applying it.

### AC6, and what the first proof-of-red actually found

`CLAUDE.md`'s standing rule was applied as mutation testing: every check and invariant disabled in turn,
and separately forced always-on. **The first round found three clauses written and never exercised** —
the interposed-text and region-order halves of the placement rule, and the preview exclusion. Disabling
any of them left the suite green. That is `check-readonly-commands.py`'s first version reproduced inside
this slice, which is the fourth recorded instance of this defect class in this repo.

Closed with **unit tests over hand-built emissions**, labelled synthetic and kept separate from the
recordings, for the four clauses the corpus cannot supply a red for: a framing over 200 words, text
between framing and call, regions out of order, and a preview carrying forbidden tokens. Nobody in 72
asks has done the middle two.

**Second and third rounds: twelve of twelve mutations caught.** One apparent survivor was an ineffective
mutation of mine, not a gap — it changed a comprehension's body and not its filter; re-run properly, the
context exemption is load-bearing and four tests fail without it.

### Scope taken beyond the brief, declared

- **A sixth fixture, `06-over-the-ceiling`.** The brief planned three failing fixtures plus a conforming
  one, on the assumption the ceiling would be *disproved*. It was repaired instead, and a repaired check
  with no red instance is the defect above. The worst real question in the repo's history — 266 words —
  is that red.
- **A ruling on `preview` panes.** The count named labels and descriptions and was silent on preview
  text, which the reader also sees. Left silent, the ceiling would have reacquired the ambiguity slice
  01's reviewer had just removed. Ruled context, with the reason, and asserted both ways.
- **`Reach` corrected.** Slice 02 takes the mechanically-checked clauses from two to four, which makes
  overclaiming easier, not harder. It now states that no check reads a live ask and cites E11.

### Deviation from repo standards, recorded rather than hidden

**Test-first was honoured for the oracle and not for the fixtures.** The four checks were written before
the fixtures they judge, and the mutation rounds are the evidence they can fail. But the fixtures were
recorded and *then* asserted against, because they are recordings — there is no failing-test-first order
for a measurement. Same shortfall shape slice 01 recorded, narrower in scope.

**The plugin cache is at 0.69.0 and this tree is ahead of it.** Nothing here was exercised through an
installed `/phil:*` command. What was exercised is the fragment, the fixtures and the tests in the
working tree, plus one real dogfood moment: **the decision request that repaired [D4] was itself posed
under this standard** — context above a marker line, 175-word framing, zero forbidden tokens, four
options each naming its cost. That is the standard being used on the decision that changed it.

---

## Review round — `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator`, 2026-08-26

Both run at the user's instruction after the work was built and before it was committed. Each was given
the design intent up front (that `skills/shared/` holds no `SKILL.md`, that the fixtures are recordings
whose defects are the point) so neither spent its pass there, and both were told to be adversarial.
**Twenty-eight findings between them. Every one below was re-verified against the files before being
accepted.** Build-path compliance for this slice: `plugin-dev` was consulted for layout before the
fixture tree was created, and both reviewers ran over the result. `nw-discuss` did not run — DISCUSS for
this feature completed on 2026-08-21.

### The two that mattered most, and neither was found by the suite

- **A framing region emitted AFTER the blocking call scored `CONFORMS`.** The parser read regions from
  the whole file and only then split on the call, so a consequence the reader can never reach counted as
  present — and `framing_matches_ask` passed too. This is precisely the failure the context-goes-above
  amendment exists to prevent, and twelve mutation rounds missed it because no recording does it. Fixed
  by partitioning before parsing; regions past the call are now reported as unreachable, with a synthetic
  red.
- **The standard contradicted itself, and the contradiction had been filed against the wrong artifact.**
  Items 4 and 5 read *"One sentence"* while the repaired ceiling explicitly sanctioned three-question
  turns. Nothing reconciled them, so **fixture 05 shipped with one tagged pair for three decisions and
  its `consequence` region held an unrelated third decision** — in the one fixture standing as the
  passing side of two checks. `01/expected.md` had blamed the fixture format; that diagnosis was wrong
  and is corrected in place.

  The standard now states the multi-decision shape: one line naming the interruption, then a
  decision-and-consequence pair **per question**. Fixture 05 re-tagged into three pairs along clause
  boundaries the recording already had — no bytes moved. The check is strictly stronger: a three-question
  turn framed once is now a `BARE-LIST`, which nothing previously caught.

### Findings accepted and fixed

| # | Defect | Fix |
|---|---|---|
| R6 | *"Nine options inside 200 words leave six words each"* — 200/9 is 22.2. The sentence omitted the framing subtraction and was wrong by 3×, **and a test asserted it verbatim**, so correcting it turned the suite red | Arithmetic stated with its subtraction; assertion retargeted. Duplicated in the feature delta, fixed there too |
| R7 | The remedy's first move — "cut option descriptions" — is the identical move used two paragraphs earlier to *refute* the combined limit, because it deletes the mandated cost statements. Only magnitude differed | Now "**trim** option descriptions — never below the sentence naming that option's cost" |
| R3 | *"No check reads a live ask, and **none can**"* — an impossibility claim the evidence does not support. The region tags are HTML comments; emitting them in flight would make an ask checkable, and asserting otherwise forecloses slice 04 by fiat | Reduced to what is measured, with the untaken mechanism named. A test asserts the impossibility claim is **absent** |
| R4/V8 | Prose forbids six categories; the oracle matched four literal patterns. Bare `CLAUDE.md`, `resume.md` and `adversarial-review` passed clean **inside the designated jargon-wall fixture** | Identifiers derived from disk (skills, commands, personas, job ids); bare filenames matched. Prose now states the check is narrower than the rule |
| R5 | Previews were outside both counts and governed by no bound — 1500 unbounded words per ask, sanctioned by name, re-entering the "unbounded" the [D5] amendment struck | Previews bounded as the context block is; the 500-word synthetic lowered |
| R12 | *Reach* named two unchecked clauses out of nine, in the section written to stop overclaiming | All of them named; "presence, never adequacy" moved into the standard from the register |
| R8 | `CONFORMS` meant "2 of 4 checks ran" for fixture 01 and "4 of 4" for 05, rendering identically | `CONFORMS (partial)` added to the register with the reason; asserted |
| R13 | Six statements of the refuted single-limit and below/unbounded positions still stood in the feature delta, and six more in the journey | All twelve amended and dated. The register also cited an AC its own fixture refutes |
| R11 | The **only consumer** said *"the standard requires context"* where the standard says *Optional* — the path was right and the paraphrase wrong | Rewritten to raise an optional clause to a local requirement, explicitly |
| R14 | *"past 400 words"* — the previews total 125, so 391 | Corrected and now asserted as `preview_words` |
| R2 | The register's own documented emission example parsed to **one region of five** — the parser required a newline the documentation did not show | Parser accepts both spellings; a test feeds the register's literal code block to it |
| R16 | `test_no_command_name_exception` guarded with a negative substring over free prose, satisfiable by any rewording | Dropped; the positive assertion and the regex check remain |
| V2 | `forbidden_token_count` and `context_words` were recorded and asserted by nothing — proven by setting them to 99 and 9999 — in a file claiming every number is re-derived. The count also held a *category* count under a token name | Both re-derived; renamed `forbidden_token_kinds`; `preview_words` and `framing_pairs` added and derived |
| V3 | Deleting the `wave label` or `slice id` regex left the suite green: the mode-set assertion checks which mode fired, never which pattern produced it | Per-pattern positive/negative table test over all six |
| V6 | The reference-form check was **line**-scoped, so one compliant path per line excused every other on it — in the check written because six bare paths shipped | Per-reference; proven by appending a bare path to a compliant sentence |
| V7 | Two more hand-maintained registries nothing derived: each `expected.md`'s prose finding set, and the register's table. A set rewritten to `NONSENSE` passed green | Both parsed and asserted against the manifests |
| V10/V11/V12 | Duplicate region tags let an empty region hide; the format banner and the single-call rule were documented and unvalidated; a bare `assert` in a helper vanishes under `python -O` | Bodies collected in order with empties dropped; banner and sentinel count validated; `raise AssertionError` |

### Two mechanism findings, both accepted — and both larger than this slice

- **Nothing ran the test suite.** No CI exists in this repository, and `SessionStart` wired only the
  invariant runner and the skew detector, so 437 tests — including all twelve checks this slice added —
  executed only when a human typed `pytest`. That is verbatim the failure `check-invariants.py`'s own
  docstring names. Added `scripts/check-tests.py` and wired it in; proven to fail on a broken test, and
  its report trimmed to the verdict and the named failures, because noise in a session report teaches
  people to stop reading it. `CLAUDE.md`'s "found twice" threshold was met several times over.
- **The skew detector reported "in sync" while the tree differed from the loaded snapshot.** It compared
  versions only, and content changes without a version bump are the normal state of a working tree
  mid-slice. Measured: both read 0.69.0 while one fragment differed by 51 lines and seven files existed
  only in the tree. The gap was being covered by *this document*, written by hand. Now fingerprints the
  shipped surfaces and reports `PLUGIN CONTENT SKEW` when versions match and bytes do not.

### Not adopted, with reasons

- **The reviewer's suggested identifier derivation, as written.** Deriving every skill and command name
  unfiltered pulls in `work`, `resume`, `refactor`, `stack`, `design` and `run` — real names that are
  also ordinary English. Applied, it failed three genuinely clean fixtures on the word "work". Adopted
  with a floor: **only hyphenated names are matched.** The residual gap — a single-word name used *as* a
  name — is stated in the fragment rather than silently accepted.
- **A `repaired.md` for fixture 06** proving the remedy closes a 266-word question without losing a cost
  statement. The claim is real and unpinned, but a repaired ask is a *constructed* ask, and this fixture
  set's discipline is that measurements come from recordings. Left as a card-shaped gap rather than met
  with a synthetic instance; the claim in the fragment now says "the remedy closes them" without
  asserting it was done.
- **Deriving the mutation register.** It is hand-maintained, and the register says so along with the
  consequence: a check with no row is a check nobody has proven can fail. Deriving mutation coverage
  needs a mutation harness, which is its own piece of work.

### What this round says about the slice

The suite went from 12 checks to 18 and from 62 tests to 82; the repo from 417 to 437. **Five of the
additions exist because a reviewer found a clause that was written and never exercised** — after a
mutation exercise that reported twelve of twelve. The lesson is not that mutation testing failed; it is
that mutation testing only covers the inputs you have, and a corpus of well-formed recordings cannot
produce a malformed frame. Both halves were needed, and only the review found that out.

