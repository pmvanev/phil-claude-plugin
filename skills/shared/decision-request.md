# Pose a Decision Request

Shared standard for the moment a command stops and needs a call only the human can make — a blocker, an
architectural choice, which option to take on an issue, whether an irreversible action is sanctioned.

The consumers are listed in `skills/shared/README.md` and derived by
`tests/test_shared_fragment_registry.py`. This header does not name them: when the sibling fragment's
header named its own consumers it named one that did not reference it.

Three failures are being prevented, and all three ship a question the reader cannot act on: **a bare
list** (options render, framing absent), **a jargon wall** (the reader must decode the question before
answering it), and **a buried ask** (correct wording, no signal — a *placement* defect, not a wording
one).

## Order of emission

Emit in this order, then call `AskUserQuestion`:

1. **Context** — whatever background, evidence or internal detail the reader may want. Optional.
2. **A marker line** — a horizontal rule, so the ask's start is unmissable.
3. **One line naming what this interrupted.** Counted.
4. **What is being decided.** One sentence. Counted.
5. **What turns on it** — what actually changes depending on the answer. Counted, and never omitted.
6. **The tool call.** Nothing between the framing and the call.

Context goes **above**, not below. The tool call renders the options and blocks, so anything emitted
after it arrives only once the answer is already given, where it cannot be opted into. Anything emitted
between the framing and the call reconstructs the buried-ask failure out of sanctioned parts.

Write items 3–5 so they read cold, to someone who was doing something else a second ago and does not
share the loaded context.

## The ceiling

**200 words, hard.** Over is a failure, not a warning.

**What enters the count:** items 3, 4 and 5 above, plus every option label and option description.
Whitespace-separated tokens — `wc -w` semantics.

**What does not:** the context block (item 1) and the marker.

When the count is exceeded, cut in this order: option descriptions, then the number of options, then
split into a smaller decision. **Never cut items 3–5 to fit.** A ceiling that evicts *what turns on it*
is being applied backwards. A decision too large to frame this way is a decision to split; the split is
the answer, and a longer ask is not.

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
identifier. Name a command in the context block, never in the counted ask; `tests/test_decision_request_fixtures.py`
matches command names on sight and admits no exception.

## Options

Name each option's cost or risk, not only its benefit. An option list where every entry reads as an
upside makes the trade invisible and pushes the reader onto the ordering.

Put the cost in the option **description**, not the label — a label is short and truncates.

Marking one option recommended is useful and permitted. A recommendation whose cost is not named turns
the ask into a rubber stamp: the bare-list failure in a politer register.

Collapse options that differ in wording and not in outcome. Three restatements of one option is a bare
list with extra steps.

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
reference guarantees the standard is present, never that an ask obeys it. Only the ceiling and the
forbidden-vocabulary list are mechanically checked. Everything else — the ordering, the placement, the
option costs, the reply handling — is as unenforced here as anywhere else.

Two gaps, both open:

- **Propagation is incomplete.** One of the six skills holding `AskUserQuestion` references this file.
  Until that changes, most asks in this plugin are governed by nothing.
- **Outside a command, nothing loads this at all.** A decision request in ordinary conversation reaches
  no reference. That gap is real, is not closed by this file, and must not be described as covered. The
  mechanism that might reach it has not been chosen.
