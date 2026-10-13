# Eliciting the semantic content — `/phil:groom-ask`

Part of the `groom-issues` skill. `SKILL.md` governs this command as much as this file does: the
standard, the scan, the defect table, the cross-issue candidates, reporting, the decision outcomes and
the never-do list all apply here.

The mechanical column has `/phil:groom-fix` and the set-level column has `/phil:groom-set`. **The
semantic column had nothing**, and that is a hole rather than a boundary: a card failing rules 1 and 2
is reported every run and resolvable by none of them, so a board of title-only cards produces an
identical report forever. That is *this tool teaches people to stop running it* reached from the
other side — not manufactured findings, but real findings with no exit.

**The refusal was never the problem; the missing editor was.** `/phil:groom-fix` declining to draft a
purpose is the boundary working exactly as designed, and nothing here relaxes it — that command never
asks, so it may never draft. What this adds is somewhere for the content to come from.

**Present the card before asking.** State what it is, what it already says, and which rule failed. A
question that assumes the reader remembers the card gets a worse answer, or none — and the reader is
often being asked about work a past self filed.

**Every ask follows the decision-request standard `SKILL.md` names. Load it before the first
`AskUserQuestion` call.**

Two things that standard cannot know, which this section owns:

- **The context block is the card.** The standard makes context *optional*; here it is **mandatory** —
  what the card is and what it already says goes above the ask, per *Present the card before asking*.
  Only this skill knows the context is a card, and only this skill can raise an optional clause to a
  requirement. Saying the standard "requires" it would put the consumer in contradiction with the file
  it loads.
- **Rule numbers never reach the counted ask.** `rule 1` and `rule 2` are this skill's internal
  numbering, and the standard forbids internal identifiers in an ask. Name the gap in plain terms —
  *it does not say when it is done* — and put the rule number in the context block beside the quoted
  body.

**The human sanctions every claim; the session may choose the words.** That is the unit, and stating it
precisely matters — an earlier draft said *sanctions every word*, which the rephrasing path below does not
deliver and cannot. Suggest one or two ways to fill the gap, **marked as the session's**, let the human
accept, edit, or replace, and write the result as a clean card in the house voice rather than a transcript.

**What must never happen is a claim reaching the card unsanctioned, or a word reaching it untraceable.**
An inferred sentence is indistinguishable from an authored one *once written*, so the remedy is not to
forbid drafting — it is to make every field's origin legible and every rewrite inspectable:

- **Each field written carries a provenance label**, from exactly this set, and the human's action decides
  which: accepted a suggestion unchanged → `you accepted my suggestion`; changed one → `you edited my
  suggestion`; **rejected the suggestions and supplied their own, or answered with none offered** →
  `you wrote`; answered in their own words and the session tidied them → `I rephrased your answer`.
  **A field written without a label is the defect**, however well the body reads. A field left alone
  because its rule passed is not written and takes no label.
- **Never combine labels, and never rephrase an accepted suggestion.** If a suggestion is accepted, the
  written form **is** the suggestion, quoted — otherwise no single label is true, and both available ones
  lie in a different direction.
- **Show the answer beside the written form wherever the two differ**, for `I rephrased your answer` and
  `you edited my suggestion` alike, and quote the suggestion for `you accepted my suggestion`. A rewrite
  the reader cannot inspect is an assertion.
- **Rephrasing is a tidying licence, not a modelling one.** Fix grammar, punctuation and register; never
  introduce a concept the human did not use, and never narrow or widen the claim. A rewrite that changes
  what the card asserts is composition wearing a truthful label — the one failure the provenance rule
  cannot catch on its own.
- **The prose standard applies PER FIELD, keyed on the label — and this is the one surface where the
  discriminator is not per-surface.** `rules/writing.md` governs the text *this session* composes:
  a suggestion, at the moment it is drafted, and a `I rephrased your answer` rewrite. **It must never
  touch a `you wrote` field.** Those are the human's own words, and tightening them would leave the
  label asserting `you wrote` over a sentence the session had edited — the provenance system reporting
  success while the thing it exists to record is gone. `you edited my suggestion` is out for the same
  reason past the edit: the human's change is theirs.

  **The tidying licence above already IS that standard, unnamed.** *Fix grammar, punctuation and
  register; never introduce a concept the human did not use* is `writing.md` restricted to a rewrite —
  so naming it here adds no rule and grants no new licence. It gives the existing clause a checkable
  referent, which is the whole of what naming a standard buys.
- **An accept must name the suggestion or restate its text.** A bare affirmation — "ok", "sure", "yep",
  "sounds right", "that works" — is never an accept. This holds **even when only one suggestion was
  offered**, where a naming rule would otherwise be satisfied by accident: the reply is equally likely to
  mean *I have read the question and will answer it*.
- **A reply that is neither an accept, an edit, a replacement, nor a decline is unanswered.** Ask once
  more, naming what is still needed. **After a second unanswered ask, treat it as a decline** — say so,
  write nothing, record nothing. Two asks is the limit; a third is the nagging that teaches people to
  stop running the tool.

**A rule that passed is never rewritten.** The session may rephrase what it elicited; a purpose that
already satisfies rule 1 is out of reach, however much tidier it could be. This is the boundary that
stops *write a clean card* becoming *rewrite the card*.

**Ask only what the scan reported missing.** Rules 1 and 2 fail independently, so derive the questions
from the findings — one question per missing rule, and none for a rule that passed. Asking for a
purpose a card already states is ceremony on the answered half, and worse than ceremony: it invites
overwriting prose that passes.

Measured on this repo's board 2026-08-14: **three cards fail rule 2 (#1, #2, #3) and none fail rule
1.** Every failing card already states a purpose and lacks only a done-condition. The population is
*partial*, not empty — so a loop that always asks both questions is wrong against every card it has
actually been observed to meet. A two-question loop was the first draft of this section, and nothing
in the suite failed when it asked for both, which is why fixture `30` exists.

Note what the family did before this. All four commands hold `AskUserQuestion`, and the other three
use it only for **consent** — pick a scope, pick the surviving card of a merge. None of them ever
asks what an issue is *for*. Elicitation is a different use of the same tool, and its absence is why
the semantic column had no exit. Here the options are the **suggestions**, and free text is the escape
hatch that keeps *the human sanctions every word* true rather than nominal.

**One card per invocation.** No batch, no apply-to-all. The content differs every time, so a
population-scaled offer has nothing to scale over — and a bulk offer would collect one answer and
write it as though it were several. Slice 02 measured what a scale-shaped offer does to a small
population: it becomes ceremony, and ceremony is what teaches people to click through a gate.

**A partial answer is written partially.** One field given and one withheld writes the one given, and
says which is still missing. **Offering** the withheld half is permitted; *supplying* it because the body
looks nearly done is not, and the difference is a visible, refusable suggestion. A card with a purpose and
no done-condition is a smaller defect than one with neither.

**Report provenance per field.** Not decoration: it is what makes an unsanctioned sentence visible.
"Wrote the body" cannot be contradicted by a reader; a per-field label, with the answer shown beside the
written form wherever they differ, can — the reader knows what they said, and any sentence they did not
sanction stands out.

**Re-read immediately before writing, and refuse a body that moved.** Slice 02's rule, and it binds
harder here — the text at risk is prose a human wrote, not a link that would have 404'd. Report what
moved and hand back **both the answers and any draft**, so a refused write does not also lose what was
just collected.

**A decline writes nothing and records nothing.** No body, no label, no comment, no note. Same no-marker cost
as a declined set-level candidate, and this is the third surface that pays it: say at the decline that
the finding returns next run. A user who has now met the same cost three times still has not been told
it a third time unless this surface says so.
