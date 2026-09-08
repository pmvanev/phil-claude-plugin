# Expected — WSUM-SELFTEST-14

`TARGET-NOT-FOUND` · `READ-ONLY`

## What must happen

One sentence: the feature has no slice with that number, and here are the numbers it does have.

## What must NOT happen

`NOTHING-RECORDED` is not reported — that is a claim about the work, and the request was simply for
something that does not exist. `TARGET-AMBIGUOUS` is not reported either: none is not too many.

No fallback and no nearest-match. Answering a question nobody asked is worse than answering none.

## Why this fixture exists

Every fixture the slice mode first shipped with expected `SUMMARY-RENDERED`. `test_every_outcome_has_a_fixture`
was satisfied entirely by stage-mode fixtures, so the slice mode had one covered outcome of four and the
suite was green over it.

**That is the second coverage test in this feature to pass over a real gap** — the first quantified over
outcomes while a class of input landed on the wrong one. Both share a shape: a test that quantifies over
one dimension cannot see a gap in another.
