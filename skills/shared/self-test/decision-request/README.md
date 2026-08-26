# `decision-request` — Acceptance Self-Test

The **standard** is the software under test, not a program. `skills/shared/decision-request.md` says how
a command must pose a question it cannot answer itself, and every one of its failure modes is silent: a
question with no framing looks *concise*, a question written in the project's own vocabulary looks
*precise*, and a well-worded question buried at the end of a report looks like *thorough work*. Each is
indistinguishable from success at a glance, which is why the standard is never changed and eyeballed — it
is changed and regression-tested here.

Driven by `tests/test_decision_request_fixtures.py`.

## Outcomes

`CONFORMS` · `CONFORMS (partial)` · `BARE-LIST` · `JARGON-WALL` · `BURIED-ASK` · `OVER-CEILING`

**`CONFORMS (partial)` is not a softer pass.** A fixture with no recorded emission is evaluated by two
of the four checks — placement and framing-presence cannot run without tags — so its empty finding set
means *nothing that was measured failed*, which is a different claim from fixture 05's. Both used to
render as bare `CONFORMS`, and the caveat lived fifty lines below the table.

A fixture declares a **primary** outcome — the mode it exists to pin — and the **exact set** of findings
it produces. The set is what the suite asserts. Real asks are rarely single-mode: three of the six fail
three or four ways at once, and a test that accepted "some finding fired" would pass with two checks
broken.

## Every fixture is a recording

No fixture here is invented. Each is a real decision request emitted in this repo's own sessions,
extracted verbatim from the session log named in its `manifest.json` alongside the timestamp, so anyone
can re-extract it. The region tags described below are the only addition.

That was a choice, not a convenience: a synthetic ask is written by whoever is also writing the
standard, so it demonstrates the standard's intent rather than testing it. The corpus — 72 real asks,
134 questions — was reachable, so it was used.

## What the fixtures pin

| Fixture | Situation | Pins | Expected |
|---|---|---|---|
| `01-the-ask-that-shipped/` | this feature's own DISCUSS elicitation — three decisions at once, one of them about the ceiling itself (**walking skeleton**) | slice-01 AC1, S1-AC2; the instance that **refuted** the combined limit at 564 words | `CONFORMS` — partial: no emission, so 2 of 4 checks ran |
| `02-the-bare-list/` | a real irreversible-action confirmation behind a 16-word lead-in; the options carry the whole decision | S3-AC1, slice-02 AC1 | `BARE-LIST` `JARGON-WALL` `BURIED-ASK` |
| `03-the-jargon-wall/` | a real four-part wave elicitation written in card numbers, job ids, persona filenames and command names | S3-AC2, slice-02 AC2, **C2** | `JARGON-WALL` `BARE-LIST` `BURIED-ASK` |
| `04-the-buried-ask/` | conforming wording — all three elements, no vocabulary, both counts met — at the end of a report and a six-row table, no separator | S3-AC3, slice-02 AC3, **[D9]** | `BURIED-ASK` — alone |
| `05-the-context-block/` | a real ask that genuinely needed its evidence: 53 words of context above a marker line, carrying a path the ask may not; **three questions, three tagged pairs** | S2-AC1/AC3/AC4, slice-02 AC8, **[D5]** | `CONFORMS` |
| `06-over-the-ceiling/` | the worst single question in the repo's history — 266 words with its options | slice-02 AC6, the red instance for the **repaired** ceiling | `OVER-CEILING` `BARE-LIST` `JARGON-WALL` `BURIED-ASK` |

## The two sharpest fixtures

**`04` is the one the slice was built to obtain.** Slice 02's brief allowed for the possibility that
"correct wording, wrong placement" could not be expressed as a fixture at all, in which case [D9] was a
sentence rather than a clause. `04` is a real ask that fails on placement **and nothing else**, so the
clause stands. `test_placement_is_isolated_by_exactly_one_fixture` asserts that isolation by name: widen
any other check and that test goes red, which is the intended alarm.

**`01` is the one that cost a locked decision.** Filed in slice 01 as the conforming baseline at 143
words, it measures **564** under the count slice 01 actually shipped. It was not the ask that was wrong.

## The emission format

Wording and the count can be read from the ask text alone. **Placement cannot** — a check needs to know
where the framing begins, and nothing in raw output says so. Measured across the 72-ask corpus, the
paragraph immediately before the call runs 82 words or fewer in 70 of them, so position does not reveal
it either.

So a fixture that pins placement records a **tagged** emission:

```markdown
<!-- decision-request-emission:v1 -->
<!-- context -->      …evidence, paths, card numbers — exempt from the vocabulary rule…
<!-- /context -->
<!-- marker -->
---
<!-- /marker -->
<!-- interrupted -->  item 3 — one line naming what this interrupted
<!-- /interrupted -->
<!-- decision -->     item 4 — what is being decided
<!-- /decision -->
<!-- consequence -->  item 5 — what turns on it
<!-- /consequence -->
<!-- call -->
```

`<!-- call -->` is unpaired: it marks where the blocking tool call goes, and **exactly one** must
appear. A region is **absent** when the real emission had no such text — that absence is the observable,
not a formatting choice. Regions are parsed from before the call only: anything tagged after it is
reported as unreachable, because that is what it is.

**The pair repeats.** One `interrupted` for the turn, then a `decision` and a `consequence` **per
question**, alternating. Fixture 05 carries three of each for its three questions. A turn asking three
questions and tagging one pair is three decisions with one framed, and that is a `BARE-LIST`.

`ask.md` must be the tagged framing regions **word for word** (`framing_matches_ask`) — not byte for
byte, because a decision and its consequence can fall either side of a clause break inside one recorded
sentence, as fixture 05's do three times. Comparing word sequences keeps the recording verbatim while
still proving the counted text and the read text are the same text, which is all the invariant is for.

### The tagging is a reading, and that is the format's cost

Assigning a sentence to `decision` rather than `consequence` is judgement. It is exercised once, recorded
in the file, and reviewable — which is better than re-deriving it per run — but it is not a measurement,
and `BARE-LIST` inherits the limit: it fires on an element that is **absent**, never on one that is
present and weak. A `consequence` region reading "this matters" passes.

**Fixture 01 records no emission, and the reason is not the format's fault.** An earlier draft of this
file blamed the region tags for "assuming one decision per framing". That diagnosis was wrong: the tags
were singular because **the standard's items 4 and 5 were singular** while its ceiling already sanctioned
three-question turns, and nothing reconciled them. The standard now states the multi-decision shape and
the tags repeat. What still keeps 01 emission-less is narrower and real: its framing fuses each decision
with its own consequence inside a single clause — *"maps what happens when the question is malformed,
which is the actual complaint"* — so the pair cannot be separated without rewriting a locked recording.

That correction cost a fixture its `CONFORMS`. Fixture 05 shipped with one tagged pair for three
decisions, so its `consequence` region held an unrelated *third decision* — and 05 is the sole green
instance for two of the four checks. Re-tagged into three honest pairs, it conforms again.

## Driving rules

- **Drive the suite whenever `skills/shared/decision-request.md` changes**, and whenever any consumer's
  ask site changes. `pytest tests/test_decision_request_fixtures.py`.
- **A fixture with no emission must say so** in `placement_not_asserted`. A silently skipped check is the
  defect this repo keeps rediscovering.
- **Never edit a fixture to make it pass.** Every one is a recording; the defect is the recording's, and
  fixing it deletes the evidence. Re-tagging a *mis-tagged* region is not editing the recording — the
  bytes do not move.
- **Every mode needs a failing *and* a passing instance.** Asserted by
  `test_every_mode_has_a_failing_and_a_passing_fixture` — a check with no red is
  `check-readonly-commands.py`'s first version, and a check with no green is one stuck on.
- **Every number in a manifest is re-derived, without exception.** Two were not, and both drifted freely:
  `forbidden_token_count` (renamed `forbidden_token_kinds` — it held a category count under a token name)
  and `context_words`. Add a field, add its derivation in the same commit.

## Where the corpus could not supply a red

Eight clauses have no real counter-example, so they are exercised by **unit tests over hand-built
emissions** at the foot of the test file, labelled synthetic:

| Clause | Why no recording exists |
|---|---|
| framing over 200 words | no ask in the corpus has one; the longest recorded framing is 148 |
| text between the framing and the call | nobody has done it |
| framing regions out of order | nobody has done it |
| a framing region **after** the call | nobody has done it — and the oracle scored it `CONFORMS` |
| decision/consequence pairs fewer than questions | every recording either frames every question or frames none |
| a preview pane carrying forbidden tokens | the one fixture with previews already fails the vocabulary rule for its own ask |
| a wrong banner, or two call sentinels | every recording is well-formed |
| a duplicate empty region | ditto |

A constructed emission is the right input for testing a parser and the wrong input for measuring a
standard. The split is deliberate; collapsing it in either direction loses something.

## The mutation register

Every check and invariant below was disabled — and where meaningful, forced always-on — and the suite
re-run. A row is only complete when the disabling turned the suite **red**.

| # | Clause or invariant | Mutation applied | Caught by |
|---|---|---|---|
| 1 | framing ceiling | `if framing > FRAMING_CEILING` → `if False` | `test_an_over_long_framing_breaches_the_framing_limit` |
| 1b | framing presence — item 3 | `if not _bodies(before, "interrupted")` → `if False` | `test_a_missing_interruption_line_is_named` |
| 2 | per-question ceiling | `g > QUESTION_CEILING` → `g > 10_000` | fixture 06's finding set |
| 3 | per-question ceiling, stuck on | `g > QUESTION_CEILING` → `g > 0` | 01, 04, 05's finding sets |
| 4 | vocabulary rule | filter → `if False` | fixtures 02, 03, 06 |
| 5 | vocabulary rule, widened to the context | counted text += the emission | `test_the_context_block_is_exempt_from_the_vocabulary_rule` |
| 6 | each of the six forbidden patterns | pattern deleted | `test_every_forbidden_pattern_is_independently_failable` |
| 7 | framing presence | `missing = []` | fixtures 02, 03, 06 |
| 8 | framing presence, stuck on | `missing = list(FRAMING_REGIONS)` | 01, 04, 05 |
| 9 | pairs-per-question | one pair accepted for N questions | `test_a_three_question_turn_needs_three_pairs` |
| 10 | placement — marker | `if not marker` → `if False` | fixtures 02, 03, 04, 06 |
| 11 | placement — interposed text | `if trailing.strip()` → `if False` | `test_text_between_the_framing_and_the_call_is_a_placement_defect` |
| 12 | placement — region order | `if ranked != sorted(ranked)` → `if False` | `test_regions_out_of_order_are_a_placement_defect` |
| 13 | placement — regions after the call | parse the whole file, not `head` | `test_framing_emitted_after_the_call_is_unreachable` |
| 14 | preview exclusion | preview text added to the count | `test_a_preview_pane_never_enters_the_count`, `test_a_forbidden_token_in_a_preview_is_not_a_jargon_wall` |
| 15 | coherence of ask and emission | `framing_matches_ask` → `return True` | `test_the_coherence_rule_fires_on_an_inconsistent_fixture` |
| 16 | manifest numbers re-derived | `forbidden_token_kinds`, `context_words` falsified | `test_the_manifest_still_describes_the_files` |
| 17 | the prose registries | a finding set rewritten in `expected.md`; a README row | `test_the_prose_finding_set_matches_the_manifest`, `test_the_register_table_matches_the_manifests` |
| 18 | the documented format | the register's own worked example fed to the parser | `test_the_registers_documented_format_actually_parses` |

**Rows 1b, 6, 13, 16, 17 and 18 exist because earlier rounds of this exercise found them green.** The
first round mutated twelve checks and reported twelve reds; three clauses inside them were written and
never exercised, and the register then claimed full coverage — a compliance claim that reported success by
staying quiet, which is this board's named recurring defect appearing inside the fix for it.

**Mutate the data, not the assertion, for rows 16 to 18.** Those rows *are* assertions over recorded
prose and numbers, so blanking one can only be caught by another check and reads as a false green. The
mutation that proves them is falsifying what they guard: a manifest number set to nonsense, a finding set
rewritten in `expected.md`, a row edited in the table above, a region deleted from the worked example.
The first attempt at this table got that wrong and reported five spurious greens.

**Keep this table in step with the checks.** It is hand-maintained and nothing derives it, which is the
weakness the table itself documents. The honest mitigation: a new check without a row here is a check
nobody has proven can fail.

## What a green run does NOT mean

It does not mean any live ask conforms. **No check here reads live output.** A green run means the
standard and the six recordings it is measured against still agree — that a change to the fragment has
not silently retired a clause. Conformance in flight is unenforced, the fragment's *Reach* section says
so, and slice 03's build check will only ever prove that a skill *loads* the standard.

Nothing about the recordings shows live checking is *impossible*, and the fragment no longer claims it
is: the region tags are HTML comments, so a consumer instructed to emit them would make an ask readable
by a hook. That mechanism has not been chosen, and choosing it is slice 04's question, not this file's.
