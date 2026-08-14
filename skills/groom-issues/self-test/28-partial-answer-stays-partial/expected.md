# Expected outcome — fixture 28 (half an answer is written as half)

**Pins:** slice-04 AC5, constraint C9.

**Expected decision:** `ASK-CONTENT` then `WRITE-PARTIAL`. The answered field is written; the withheld
one is not invented:

```
#47 — partially filled in.

  Purpose      ← your answer, verbatim:
    "retries fire on 4xx and burn the rate limit"
  Done when    — not written. You said it depends on what the retry audit finds.

Rule 2 is still unmet on this card, and the next scan will report it.
```

**Why this is the sharpest fixture in the slice.** Every other failure mode here is a refusal the
session must hold. This one is a refusal it must hold *while the answer is nearly obvious*: the user
has just explained that retries fire on 4xx and should not, and "done when retries no longer fire on
4xx" writes itself. It would be a good acceptance criterion. It would also be the session's, not the
user's — and the user explicitly said they do not know it yet, because it depends on an audit.

A body that is complete and partly invented is worse than one that is honestly half-done. The
half-done card keeps reporting rule 2 until a human answers it; the invented one looks finished and
stops asking.

**Gate failures:**

- Deriving the done-condition from the purpose, however directly it seems to follow.
- Writing "TBD", "to be determined", or an empty `## Done when` heading. A heading with nothing under
  it may read to the next scan as a satisfied rule, which silences the finding without resolving it.
- Pressing the user again after they have said they do not know. Asked and answered; the answer was
  *not yet*.
- Reporting `WRITE-ELICITED`. The run wrote one field of two, and the outcome name is what a reader
  scans for.
- Omitting that rule 2 is still unmet and will be reported again.
