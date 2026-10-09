# Expected outcome — fixture 01 (test findings name a pattern)

`test_invoice.py` holds three test smells and one correct test. `invoice.py` is the code under test
and is clean.

**Pins:** a Priority 6 finding takes its smell, its fix and its route from `rules/test-patterns.md`'s
Smell Catalogue. Before that rule existed, the backlog's rule that every item name a refactoring from
`refactoring-catalog.md` could not be met by any test finding, because that catalogue holds none.

**How to drive it:** run `/phil:review-code .` in this directory.

**Expected:** a `.refactoring-backlog.md` whose Priority 6 items match the three in
`expected-backlog.md`, on the `(Smell, Refactoring, Route)` triple:

1. **Mystery Guest** — `test_total_matches_recorded_case` reads its inputs and its expected value from
   a file the reader never sees.
2. **Conditional Test Logic** — `test_each_line_contributes_to_total` loops, branches and computes its
   expected values with the code under test.
3. **Sensitive Equality** — `test_invoice_records_customer_and_total` is about the customer and the
   total, and compares `repr()` to get at them.

**Hard assertions (any failure blocks the skill change):**

- **`test_paying_sends_a_receipt` contributes no item.** `ReceiptMailer` is owned, but it stands in
  for the email gateway, an unmanaged dependency; the receipt it is sent is the behaviour, and asserting the call is the right test. Flagging it as
  Overspecified Software or Mock Inside a Boundary is a gate failure.
- Every Priority 6 item carries a **Route** field, and its value is the catalogue row's.
- No Priority 6 item names a refactoring from `refactoring-catalog.md`.

- **No item at Priorities 2–5 names `test_invoice.py`.** A finding in a test file is Priority 6; a
  loop or a literal there reported as Long Function or Magic Number would route to `/phil:refactor`,
  which would extract the expected values the test exists to show.

Items about `invoice.py`, and line numbers within ±2, do not fail the fixture.
