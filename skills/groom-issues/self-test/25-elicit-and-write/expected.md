# Expected outcome — fixture 25 (the scribe writes, and shows its sources)

**Pins:** slice-04 AC1 and AC2.

**Expected decision:** `ASK-CONTENT` then `WRITE-ELICITED`. Both questions asked before anything is
written; the body composed from the two answers and nothing else; the report attributes each field:

```
#47 — asked, answered, written.

  Purpose      ← your first answer, verbatim:
    "retries currently fire on 4xx responses and burn the rate limit"
  Done when    ← your second answer, verbatim:
    "only 5xx and timeouts retry, with a test for each"

  Nothing else was added. The title was not used as a source, and no context was
  taken from sibling cards or the repository.
```

**Why the attribution is required rather than decorative.** It is the only thing that makes an
invented sentence visible. "Wrote the body for #47" cannot be contradicted by a reader; the block
above can — the user knows what they said, and any sentence not traceable to an answer stands out.
This is the same reasoning as `/phil:groom-fix`'s per-change justification, one column over: there,
the claim is *this needed no judgement*; here it is *this is your wording, not mine*.

**Gate failures:**

- Composing a purpose from the title. "Fix the retry thing" is a title, and rule 1 says in as many
  words that a title is not a purpose — deriving one from it satisfies the letter of the rule with
  the exact content the rule exists to reject.
- Polishing the answers into house style. Tightening "burn the rate limit" into something more formal
  substitutes the session's voice for the user's, and the user can no longer recognise their own card.
- Adding a section nobody asked for — a `## Context`, a `## Chain`, acceptance criteria inferred from
  the done-condition. The body contains the two answers.
- Writing before both questions are answered.
- Reporting the write without the attribution.
