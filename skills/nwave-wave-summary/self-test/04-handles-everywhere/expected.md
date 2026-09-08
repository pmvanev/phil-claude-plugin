# Expected — WSUM-SELFTEST-04

`SUMMARY-RENDERED` · `READ-ONLY`

## What must happen

Each decision is stated in words. The `stated` example in the manifest is the shape: a sentence a reader
can act on without opening anything.

## What must NOT happen

No handle, path, bracketed id or card number survives into the output. The `keyed_on_handles`
counterexample carries all four and is perfectly accurate, which is what makes it tempting.

**The longhand escape is also forbidden.** `laundered` replaces every handle with a spelled-out version
of the same identifier and says nothing more than the original — the reader still has to go and find the
eleventh decision.

Note this differs from the board read, deliberately. There, forbidding a card number only launders it
into *card 34*, so the class is permitted. Here there is nothing to launder into: the fix is not a
different spelling but saying what the identifier refers to.

## Why this fixture exists

157 references across this repo's artifacts point at a record the repo does not contain. The most common
handle in the corpus resolves nowhere, which is the sharpest available case for stating decisions rather
than naming them.
