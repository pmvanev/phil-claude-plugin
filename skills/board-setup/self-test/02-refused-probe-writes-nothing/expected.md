# Expected — BS-SELFTEST-02

`REFUSED`

## What must happen

**The file is byte-identical, in both variants.** No section, no markers, no partial region — not
even the facts the probe successfully gathered before it hit the refusing condition.

Variant (a) reports `refusal.reason` and then `refusal.fix` verbatim: `gh auth refresh -s project`.

Variant (b) reports `refusal.reason` and states that **no fix is known**. It does not print `None`,
and it does not invent one — in particular it must not suggest naming the board explicitly, because
no flag accepts a board.

## Why this fixture exists

Two silent failures meet here.

A partial block **looks more complete than a refusal**. A region missing only its Status field id
reads exactly like a region for a board that has no Status field, and the reader has no way to tell
which they are looking at — so the wrong outcome is the one that looks better.

And a null `fix` is the case a relay tends to fill. Printing `None`, or substituting plausible
advice, converts "we do not know how to fix this" into "do this" — which is the same
assumption-as-fact defect the feature exists to close, one register quieter.
