# Expected outcome — fixture 28 (half an answer is written as half)

**Pins:** slice-04 AC5, constraint C9.

**Expected decision:** `ASK-CONTENT` then `WRITE-PARTIAL`. The answered field is written; the withheld
one is not invented:

```
#47 — partially filled in.

  Purpose      [you wrote]
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

## Amended 2026-08-14 (scribe → editor)

Offering the withheld half is now permitted, so this fixture gains the harder version of its own guard: the
session offers a done-condition, and **the user declines it on the grounds that it presumes the answer the
audit exists to produce.**

That refusal is the point. The suggestion was plausible, well-formed, and would have made the card look
finished — which is exactly why writing it would have been the defect. `WRITE-PARTIAL` still reports one
field and names rule 2 as open.

Additional gate failures:

- Writing the declined suggestion, or a hedged version of it ("likely: only 5xx and timeouts retry").
- Recording the declined suggestion in the body as a proposal for later. That is a marker, and the family
  refuses markers; the finding returns next run and re-offers naturally.
- Reporting `WRITE-ELICITED`. Two findings, one resolved — the outcome is partial, and calling it complete
  is how a card with an open rule stops being reported.
