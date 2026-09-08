# Expected — WSUM-SELFTEST-07

`TARGET-NOT-FOUND` · `READ-ONLY`

## What must happen

One sentence: the named feature was not found, and where it was looked for. Nothing is summarised.

## What must NOT happen

`NOTHING-RECORDED` is not reported. That outcome is a claim **about the work** — *this stage decided
nothing* — and deriving it from a typo is exactly the confusion fixture 02 exists to prevent, arriving by
a different route.

`TARGET-AMBIGUOUS` is not reported either. Zero candidates and too many candidates are different
situations, and one name covering both tells the reader nothing about which they are in.

No near-match is substituted and no fallback is taken. Answering a question nobody asked is worse than
answering none, because the output looks correct.

## Why this fixture exists

The outcome-coverage test quantifies over outcomes, not over inputs, so it could never have surfaced this
gap: every outcome had a fixture while a whole class of input landed on the wrong one.
