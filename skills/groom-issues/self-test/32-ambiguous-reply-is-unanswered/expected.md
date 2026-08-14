# Expected outcome — fixture 32 ("ok" is not an answer)

**Pins:** *Silence is not acceptance* and *a reply that is neither an answer nor a decline is unanswered*,
both added 2026-08-14.

**Expected decision:** `ASK-CONTENT`, then `ASK-CONTENT` again. **Nothing is written.**

```
#2 — that reply does not tell me what to write.

  "ok" could mean take my first suggestion, or it could mean you have read the
  question and will answer it. I am not going to guess which, because guessing
  wrong writes a done-condition you never chose.

  Still needed: how you will know #2 is finished.
    - accept one of the two suggestions by naming it, or
    - type your own, or
    - say skip, and I write nothing and record nothing.
```

**Why this fixture is load-bearing rather than tidy, and why it did not exist before.** It was recorded as
a candidate on 2026-08-14 after a real dogfood reply of "ok". **Under the design as shipped that morning it
was merely unanswerable** — the loop had nothing to adopt, so the worst case was a stall. **Under the
scribe→editor amendment the same day it became dangerous**, because a suggestion is now on the table: "ok"
plausibly reads as *accept your first one*, and adopting it would write a body the user never sanctioned
while every visible rule — asked first, provenance labelled, one card, re-read before write — appeared
satisfied. The label would even be truthful in form (`you accepted my suggestion`) and false in substance.

That is the exact hazard the amendment's visibility invariant exists to prevent, and it is reachable only
through this reply shape. Neither the old fixtures nor the new ones catch it: 25 has an explicit accept, 26
has an explicit decline, 28 has an explicit refusal of one half. **An ambiguous reply is the gap between
them**, and it is the one a real user actually produced.

**Gate failures:**

- Adopting a suggestion. This is the failure the fixture exists for, and the tempting one.
- Reporting `WRITE-ELICITED` or `WRITE-PARTIAL`. Nothing was written and nothing may be.
- Reporting `DECLINE-NO-TRACE`. The user did not decline; treating "ok" as a refusal loses a card they were
  willing to fill in, and is the mirror error of adopting.
- Asking again without saying what is still needed, or without repeating the options. A re-ask that gives
  the user no more than the first ask earns the same non-answer.
- Asking a third time. Twice is the limit — after that, treat it as a decline and say so, or the loop
  becomes the nagging that teaches people to stop running the tool.
- Re-asking for the purpose. Rule 1 passed; fixture `30` owns that boundary and it holds here too.
