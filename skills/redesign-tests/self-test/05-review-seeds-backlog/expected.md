# Expected outcome — fixture 05 (review seeds the behavioural backlog)

`test_orders_smells.py` contains four behavioural smells, one per test function; `orders.py` is the
SUT and must NOT be flagged.

**Pins:** AC2.1 (detect only in-scope behavioural smells, reusing `review-code` Priority 6), AC2.2
(write `.test-redesign-backlog.md`, a **separate** file from `.test-refactoring-backlog.md`), AC2.4
(detection precision — dogfood KPI ≤20% first-pass false positives).

**How the loop drives it:** run `/phil:redesign-tests --review .`. Apply nothing.

**Expected outcome:** a `.test-redesign-backlog.md` whose items match the four `(smell-family,
rewrite-intent)` pairs in `expected-backlog.md`:

1. implementation-coupling — mock-interaction assertion (`test_place_saves_order`)
2. implementation-coupling — testing private state `_orders` (`test_repo_internal_dict_has_order`)
3. flakiness/determinism — wall-clock dependency (`test_order_year_is_current`)
4. excessive-mocking — mocks the only collaborator (`test_place_everything_mocked`)

**Match criterion:** the four `(smell-family, rewrite-intent)` pairs, one per test function, with
`orders.py` NOT flagged and the backlog written to `.test-redesign-backlog.md` (not the
refactor-tests file). Line numbers may drift ±2 — do not fail on skew alone. Structure-only smells
(duplicated setup, AAA, vague name) must NOT appear — those belong to `refactor-tests`, not here.

**Gate failure (blocks the skill change):** the SUT is flagged; the backlog is written to
`.test-refactoring-backlog.md` (collision with refactor-tests); any structure-only (D5) smell
appears; or a rewrite is applied in review mode.
