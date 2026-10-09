# Expected outcome — fixture 07 (a mock at an unmanaged dependency is behaviour)

`test_orders_boundaries.py` holds two tests with the same shape: each mocks a collaborator and
asserts the call. Only one is a smell.

- `test_place_sends_confirmation` mocks `EmailSender`. The type is owned, but it stands in for an
  email gateway — an unmanaged dependency. The confirmation it receives is what a customer sees, so
  asserting the call **is** asserting the observable outcome. A detector that judges by ownership
  flags it; the rule judges by what the double stands in for.
- `test_place_calls_repo_save` mocks the repository — owned and in-process. Asserting `save()` was
  called is Overspecified Software; the outcome is the order the repository returns.

**Pins:** `rules/test-patterns.md`'s stance — communication-based verification belongs at an unmanaged
dependency. Before the skill read that rule, its implementation-coupling signal named
`mock.x.assert_called` with no exception, so a `--review` would flag both tests and propose rewriting
the correct one to assert on state that holds nothing about the email.

**How to drive it:** run `/phil:redesign-tests --review .` in this directory. Apply nothing.

**Hard assertions (any failure blocks the skill change):**

- **Exactly one item**, for `test_place_calls_repo_save`, filed as implementation-coupling or as
  excessive-mocking — it mocks an in-process collaborator *and* asserts only on the mock, so both
  families fit and either passes.
- **`test_place_sends_confirmation` appears nowhere in the backlog.**
- `orders.py` contributes no item.

Line numbers may drift ±2.
