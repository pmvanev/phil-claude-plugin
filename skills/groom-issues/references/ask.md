# Eliciting the semantic content — `/phil:groom-ask`

Part of the `groom-issues` skill. `SKILL.md` governs this command as much as this file does: the
standard, the scan, the defect table, the cross-issue candidates, reporting, the decision outcomes and
the invariants all apply here.

**This command is the semantic column's exit.** Without it, a card failing rules 1 or 2 is reported
every run and resolved by nothing. `/phil:groom-fix` still drafts nothing: it never asks, so it may
never draft. This command asks, so it may.

**Present the card before asking.** State what it is, what it already says, and which rule failed. The reader is
often being asked about work a past self filed.

**Every ask follows the decision-request standard `SKILL.md` names. Load it before the first
`AskUserQuestion` call.**

Two things that standard cannot know, which this section owns:

- **The context block is the card.** The standard makes context *optional*; here it is **mandatory** —
  what the card is and what it already says goes above the ask, per *Present the card before asking*.
  This skill raises the standard's optional clause to a requirement; the standard itself does not
  require it.
- **Rule numbers never reach the counted ask.** `rule 1` and `rule 2` are this skill's internal
  numbering, and the standard forbids internal identifiers in an ask. Name the gap in plain terms —
  *it does not say when it is done* — and put the rule number in the context block beside the quoted
  body.

**The human sanctions every claim; the session may choose the words.** Suggest one or two ways to fill the gap, **marked as the session's**, let the human
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

  The tidying licence above is that standard restricted to a rewrite; naming it adds no licence.
- **An accept must name the suggestion or restate its text.** A bare affirmation — "ok", "sure", "yep",
  "sounds right", "that works" — is never an accept. This holds **even when only one suggestion was
  offered**: the reply may mean only *I have read the question*.
- **A reply that is neither an accept, an edit, a replacement, nor a decline is unanswered.** Ask once
  more, naming what is still needed. **After a second unanswered ask, treat it as a decline** — say so,
  write nothing, record nothing. Two asks is the limit.

**A rule that passed is never rewritten.** The session may rephrase what it elicited; a purpose that
already satisfies rule 1 is out of reach, however much tidier it could be.

**Ask only what the scan reported missing.** Rules 1 and 2 fail independently, so derive the questions
from the findings — one question per missing rule, and none for a rule that passed. Asking for a
purpose a card already states invites overwriting prose that passes. Wound: on this repo's board
(2026-08-14) three cards failed rule 2 and none failed rule 1; fixture `30` pins it.

**The options are the suggestions, and free text is the escape hatch.** The other three commands ask
only for consent; this one asks what an issue is *for*.

**One card per invocation.** No batch, no apply-to-all. The content differs every time, and a bulk
offer would collect one answer and write it as though it were several.

**A partial answer is written partially.** One field given and one withheld writes the one given, and
says which is still missing. **Offering** the withheld half is permitted, as a visible, refusable
suggestion; *supplying* it because the body looks nearly done is not.

**Report provenance per field**, with the answer beside the written form wherever they differ. It is
what makes an unsanctioned sentence visible.

**Re-read immediately before writing, and refuse a body that moved**, per `SKILL.md`; the text at risk
here is prose a human wrote. Report what moved and hand back **both the answers and any draft**.

**A decline writes nothing and records nothing.** No body, no label, no comment, no note. Say at the decline
that the finding returns next run.
