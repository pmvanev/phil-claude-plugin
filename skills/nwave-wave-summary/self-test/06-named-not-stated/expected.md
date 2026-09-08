# Expected — WSUM-SELFTEST-06

`SUMMARY-RENDERED` · `READ-ONLY`

## What must happen

Every decision is stated in words. The `stated` example is the shape — and it deliberately covers a
**different** decision from the counterexamples, so it demonstrates the form without supplying the answer
to this fixture's own two.

## What must NOT happen

No decision is referred to by position or by location. Both counterexamples are clean by every mechanical
rule: `by_position` and `by_location` contain no path, no bracketed id, no handle and no card number.
They pass the checker and defeat the command's entire purpose.

## Why this fixture exists

**It asserts a gap rather than a capability.** The vocabulary check is necessary and not sufficient: a
summary can satisfy every pattern in `scripts/plain_language.py`, sit inside the ceiling, be entirely
accurate, and still require the reader to open the artifact. Nothing mechanical catches that, so it is a
rule in prose and a fixture here — and the driver asserts the counterexamples genuinely pass the checker,
so the gap is recorded rather than assumed.
