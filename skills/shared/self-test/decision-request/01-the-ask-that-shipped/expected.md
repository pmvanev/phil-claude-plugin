# Expected outcome — fixture 01, the ask that shipped (walking skeleton)

**Expected decision:** `CONFORMS`. **Finding set:** empty.

`ask.md` is the verbatim framing emitted during this feature's own DISCUSS wave on 2026-08-21, before
any artifact was written. It is the baseline the failing fixtures are measured against, and it is
**locked** — edit it and the baseline is gone.

## What slice 02 added, and why it had to

`options.json` — the three questions and nine options from the same call, recovered verbatim from the
session log. Slice 01's reviewer found that this fixture *"could not discriminate because its `ask.md`
contains no options at all"*: it reported 143 words as a full measurement when the count it was filed
against included option text. The options were never lost, only never captured. Now they are.

## What is asserted mechanically

- **Framing 143 words** against a limit of 200.
- **Questions at 145, 127 and 149 words** with their options, each against a per-question limit of 200.
- **Zero forbidden tokens** in the counted ask.

All re-derived on every run; `manifest.json` is documentation and the test is the authority.

**This fixture is what refuted the combined limit.** Under slice 01's single 200 across the framing and
every option, this ask — the one filed as the conforming baseline — measures **564 words**. It did not
become non-conforming; the limit was wrong, and this is the instance that proved it.

## Why placement and framing-presence are not asserted here

`manifest.json` records `emission_file: null` and says so, rather than skipping two checks quietly.
Two reasons, both real:

1. **The ask predates both observables.** The marker line and the three tagged framing elements were
   added after this ask was emitted. Its real emission carried no marker, so tagging it would file the
   conforming baseline as a placement failure on a rule that did not exist when it was written.
2. **Its framing does not decompose into the three regions.** It puts three parallel decisions in one
   paragraph, each stating its own consequence inline — *"which is the actual complaint"*, *"wearing a
   different hat"*, *"the standard becomes advice"*. There is no single `consequence` region to tag.

**The second reason was first written down wrongly, and the correction matters.** This file used to say
the region tags "assume one decision per framing" — a limit of the format. That was the wrong culprit.
The tags were singular because **the standard's items 4 and 5 were singular** ("One sentence") while its
ceiling already sanctioned three-question turns, and nothing reconciled the two. The standard now states
the multi-decision shape and the tags repeat, one pair per question.

What still keeps this fixture emission-less is narrower and real: its framing fuses each decision with
its own consequence inside a single clause — *"maps what happens when the question is malformed, which is
the actual complaint"* — so the pair cannot be separated without rewriting a locked recording.

That mis-diagnosis had a cost. Fixture 05 shipped with one tagged pair for three decisions, so its
`consequence` region held an unrelated *third decision* — in the only fixture standing as the passing
side of two checks. Found by review, not by the suite: the presence check cannot read a region's
content.

## What is asserted by reading, and is not automated

- The framing states what is being decided and what turns on it before any option appears, three times
  over, once per decision.
- Each option names its own cost. Now checkable by eye against `options.json`, which is a gain over
  slice 01's version, where the claim rested on nothing readable.

## Gate failures

- Recording a count and never recomputing it.
- Treating this fixture as proof the ceiling works. **One instance is not a distribution** — and this
  instance is the one that disproved the first version of the limit.
- Adding a forbidden token to `ask.md` to make it read more precisely.
