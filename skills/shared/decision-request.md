# Pose a Decision Request

Shared standard for the moment a command stops and needs a call only the human can make — a blocker, an
architectural choice, which option to take on an issue, whether an irreversible action is sanctioned.

Consumers are listed in `skills/shared/README.md`, derived by
`tests/test_shared_fragment_registry.py`, and deliberately not repeated here.

Three failures are being prevented, and all three ship a question the reader cannot act on: **a bare
list** (options render, framing absent), **a jargon wall** (the reader must decode the question before
answering it), and **a buried ask** (correct wording, no signal — a *placement* defect, not a wording
one).

## Order of emission

Emit in this order, then call `AskUserQuestion`:

1. **Context** — whatever background, evidence or internal detail the reader may want. Optional.
2. **A marker line** — a horizontal rule, so the ask's start is unmissable.
3. **One line naming what this interrupted.** Once for the turn. Counted.
4. **What is being decided.** One sentence. Counted.
5. **What turns on it** — what actually changes depending on the answer. Counted, and never omitted.
6. **The tool call.** Nothing between the framing and the call, and nothing after it.

**Items 4 and 5 repeat, as a pair, once per question.** A turn putting three questions to the reader is
three decisions, and each one needs its own statement of what is being decided and its own statement of
what turns on it. Item 3 is not repeated — one line naming the interruption serves the turn.

Three questions framed by one decision-and-consequence pair is two unframed decisions, whatever the
total length. Getting this wrong is not a length defect and no ceiling catches it.

Context goes **above**, not below. The tool call renders the options and blocks, so anything emitted
after it arrives only once the answer is already given, where it cannot be opted into. Anything emitted
between the framing and the call reconstructs the buried-ask failure out of sanctioned parts.

Write items 3–5 so they read cold, to someone who was doing something else a second ago and does not
share the loaded context.

## The ceiling

**Two limits, both 200 words, both hard.** Over is a failure, not a warning.

- **The framing — 200 words.** Items 3, 4 and 5 together.
- **Each question — 200 words.** One question's own text plus its option labels and descriptions,
  counted per question and never summed across them. A turn putting three questions to the reader is
  three decisions; capping their total would penalise batching the reader benefits from.

Whitespace-separated tokens — `wc -w` semantics. **Outside both counts:** the context block (item 1),
the marker, and any per-option preview or mock-up pane. A preview is shown beside the options rather
than read as part of them, so it may carry the tokens the ask may not, and it may never be the only
place a consequence is stated.

**Outside the count is not a licence to be long.** A preview is bounded the way the context block is —
short enough that the option text beside it is still readable. There is no countable limit for either.
Unbounded detail was struck from this standard once already; it must not come back through the pane.

**One combined limit was tried and refuted by measurement.** A single 200 spanning the framing and every
option cannot be met: the three real requests this standard was written from measure 564, 324 and 441
words against it. A framing of 143 words plus nine options under one 200-word limit leaves six words per
option — so the only way to comply was to delete the cost statements *Options* below requires. Measured
apart the same requests are modest: framings of 143, 142 and 148, and twenty options between 24 and 66.
Only the sum was impossible. The corpus behind both numbers is in the self-test register.

When a count is exceeded, cut in this order: **trim** option descriptions — never below the sentence
naming that option's cost — then the number of options, then split into a smaller decision. **Never cut
items 3–5 to fit.** A ceiling that evicts *what turns on it*, or the cost that makes an option a real
choice, is being applied backwards.

## The context block

Put every token the ask may not contain here: file paths, issue numbers, label names, internal
identifiers, evidence, command output.

**It is bounded in practice, not unbounded.** Length above the ask pushes the framing further from the
prompt, and past some length that is the buried-ask failure with extra steps. There is no countable
limit — keep it short enough that the framing is still on screen with the options. This is the accepted
cost of placing context above, chosen over an on-request pointer (which risks the reader never seeing
evidence that would have changed the answer) and over writing it to a file (which nobody opens).

Two further rules:

- Items 3–5 must be **answerable without reading the context block.** A consequence stated only in the
  context is a consequence the reader will miss.
- Do not restate progress. Item 3 is one line naming what was interrupted; a summary of the work so far
  is how the buried-ask failure grows back from the inside.

## Forbidden in the counted ask

No internal vocabulary in items 3–5, in option labels, or in option descriptions. In this plugin: no
wave labels, no issue numbers, no slice ids, no decision numbers, no skill names, no command names, no
file or artifact paths.

**The rule is absence, not explanation.** An explained label is still a label the reader has to hold. If
the ask needs the token to make sense, it is written at the wrong altitude — describe the thing, not its
identifier. Name a command in the context block, never in the counted ask.

**This rule is wider than any check of it.** The self-test matches a subset of these tokens, over
recorded fixtures only: it derives this plugin's hyphenated identifiers from disk, and it deliberately
does not match single-word names — `work`, `resume`, `refactor` and `design` are all real names here and
all ordinary English, so matching them failed clean asks on the word "work". A single-word name used *as*
a name is a violation the check cannot see.

## Options

Name each option's cost or risk, not only its benefit. An option list where every entry reads as an
upside makes the trade invisible and pushes the reader onto the ordering.

Put the cost in the option **description**, not the label — a label is short and truncates.

Marking one option recommended is useful and permitted. A recommendation whose cost is not named turns
the ask into a rubber stamp.

Collapse options that differ in wording and not in outcome.

## Do not ask when nothing turns on it

If the answer changes nothing that can be named, do not ask. Decide it, state the assumption, and carry
on. An ask with no stated consequence is a request for reassurance wearing a decision's clothes, and it
teaches the reader to stop reading asks.

## Handling the answer

- **Silence is not consent.** An ambiguous reply — "ok", "sure", "sounds right" — is unanswered. Ask
  once more, naming what is still needed. **After a second unanswered ask, treat it as a decline:** say
  so, and record nothing. Two asks is the limit; a third is nagging, and nagging teaches people to stop
  running the tool. A consumer may impose a tighter cap and must say so where it does.
- **A deferral is recorded as a deferral**, and whatever depended on it is reported as blocked. Never
  promote a deferral to the recommended option.
- **Declining and deferring are first-class.** Do not make them harder to express than answering.

## Reach

**Delivery is deterministic inside a command that references this file; compliance is not.** The
reference guarantees the standard is present, never that an ask obeys it.

Four clauses are mechanically checked, and only **against recorded fixtures** in
`skills/shared/self-test/decision-request/`: the two ceilings; part of the forbidden-vocabulary list;
the **presence** — never the adequacy — of items 3–5, one pair per question; and placement.

Everything else here is checked by nobody, and the list is longer than the checked one: every option
naming its cost, collapsing options that differ only in wording, a recommendation stating its cost, the
context block's practical bound, the preview's, items 3–5 being answerable without the context, not
restating progress, not asking when nothing turns on it, and the whole of *Handling the answer*.

**No check reads a live ask.** None can while asks are emitted untagged: a fixture's regions are tagged
by hand, and position does not identify the framing either — measured across 72 real asks in this repo's
history, the paragraph immediately before the call runs 82 words or fewer in 70 of them. Emitting the
tags in flight would make an ask checkable; that has not been chosen, and it is not claimed here to be
impossible. The fixtures catch a regression in *the standard and in the examples it is measured against*
— never a malformed ask in flight.

Two gaps, both open:

- **Propagation is incomplete.** Most skills holding `AskUserQuestion` do not reference this file — the
  current count is derived in `skills/shared/README.md` rather than stated here, because a number
  written into prose becomes a lie the moment the next consumer is wired. Until that changes, most asks
  in this plugin are governed by nothing.
- **Outside a command, nothing loads this at all.** A decision request in ordinary conversation reaches
  no reference. That gap is real, is not closed by this file, and must not be described as covered. The
  mechanism that might reach it has not been chosen.
