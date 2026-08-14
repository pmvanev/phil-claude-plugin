# Expected outcome — fixture 30 (one finding, one question)

**Pins:** the fold-back of 2026-08-14 — *ask only what the scan reported missing*.

**Expected decision:** `ASK-CONTENT` then `WRITE-ELICITED`. **Exactly one question is asked** — the
done-condition — and the body gains one field:

```
#2 — rule 2 reported. Rule 1 passes; not asked.

  Done when    ← your answer, verbatim:
    "phil:groom-issues reads the families from CLAUDE.md and reports rule 4
     evaluated rather than unevaluated on this board"

  Purpose      — already stated on the card. Not asked, not rewritten.
```

**Why this fixture exists, and why nothing caught it.** The first draft of *Eliciting the semantic
content* said to ask "what the card is for, and how they will know it is done — the two things rules 1
and 2 require", which asks both regardless of what the scan found. Fixtures `25` through `28` all
construct a card with an **empty body** and two findings, so every one of them passes while the loop
asks two questions. The suite could not fail. The gap surfaced only in the slice-04 dogfood, against
the real board, where the observed population turned out to be *partial* rather than empty: three cards
fail rule 2, none fail rule 1. **A two-question loop is wrong against every card the command has
actually been observed to meet.**

This is the same shape as `16` and `23` — a measurement contradicting a brief — and it is the third
time on this feature that the real board disagreed with a constructed population. Keep it measured.
Rewriting this fixture with an empty body would restore the hole it exists to close.

**Gate failures:**

- Asking for the purpose. Rule 1 passed; the question is ceremony, and the answer would replace prose
  that already satisfies the standard.
- Rewriting, tightening, or re-punctuating the existing purpose while writing the done-condition. The
  card's own words are not the session's to edit, and `WRITE-ELICITED` says nothing about them.
- Reporting `WRITE-PARTIAL`. Nothing is partial here: every reported finding was resolved. `28` is the
  partial case — a finding raised and deliberately left unanswered — and conflating the two makes a
  complete run look incomplete.
- Asking both questions and discarding the purpose answer. The waste is invisible in the diff and the
  user was still made to answer for nothing.
- Omitting the line that says rule 1 was not asked. A reader cannot otherwise tell whether the loop
  skipped it by rule or by accident.
