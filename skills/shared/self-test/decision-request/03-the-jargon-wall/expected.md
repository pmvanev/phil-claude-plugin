# Expected outcome — fixture 03, the jargon wall

**Primary mode:** `JARGON-WALL`. **Full finding set:** `BARE-LIST`, `JARGON-WALL`, `BURIED-ASK`.

A real four-part wave elicitation, recorded verbatim. Its question text and option descriptions are
written in the project's own vocabulary: a card number, a job id, a persona file name, a command name,
wave names.

## What this fixture proves that a count cannot

**Every one of its four questions is inside the per-question ceiling** — 187, 141, 107 and 100 words
against 200. The worst is at 94% of the limit and still passes. So the vocabulary rule is doing work no
ceiling does: this ask is the right *length* and still unreadable to anyone who was not already holding
the project's internal terms.

C2 is *absence*, not explanation. Several of these tokens are explained in place, at length; an
explained identifier is still an identifier the reader has to hold while deciding.

## Why the other two fire

Its framing is 26 words — a hand-off sentence, with no `decision` and no `consequence` region — so
`BARE-LIST` fires. It has no marker line, so `BURIED-ASK` fires. It carries a real context block of 123
words, and **the tokens in that block are not counted against it**; only the ones in the ask are.

## Gate failures

- Widening `FORBIDDEN` to catch more of this ask's vocabulary. The regex is a floor on a rule the reader
  applies, not the rule itself, and a wider regex would start firing on fixture 05's clean framing.
- Concluding the ceiling is too loose because this passed it. The ceiling and the vocabulary rule answer
  different questions; that is why both exist.
