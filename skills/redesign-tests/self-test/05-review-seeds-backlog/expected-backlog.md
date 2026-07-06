# Test Redesign Backlog

Generated: {date}
Scope: --review .

## Summary

- **Total items**: 4
- **Implementation-coupling**: 2
- **Excessive-mocking**: 1
- **Flakiness/determinism**: 1

## Backlog

### [RD001] Implementation-coupling — asserts save() was called, not the observable result

- **File**: `test_orders_smells.py`
- **Lines**: 8-11
- **Priority**: 2
- **Smell**: Implementation-coupling — mock-interaction assertion (review-code P6: "coupled to implementation rather than behavior")
- **Rewrite intent**: use the real `InMemoryOrderRepo`; assert the retrieved order equals the expected fields
- **Status**: pending

### [RD002] Implementation-coupling — reaches into private state `repo._orders`

- **File**: `test_orders_smells.py`
- **Lines**: 16-19
- **Priority**: 2
- **Smell**: Implementation-coupling — testing private state (review-code P6 / testing.md "Testing private methods")
- **Rewrite intent**: assert through the public `repo.get(order_id)` instead of `_orders`
- **Status**: pending

### [RD003] Flakiness — assertion depends on the wall clock

- **File**: `test_orders_smells.py`
- **Lines**: 24-27
- **Priority**: 3
- **Smell**: Flakiness/determinism — depends on `datetime.now()` (testing.md "Achieving Determinism")
- **Rewrite intent**: inject a fixed clock / static timestamp, or drop the time coupling; confirm with N-run stability
- **Status**: pending

### [RD004] Excessive-mocking — mocks the only collaborator and asserts solely on it

- **File**: `test_orders_smells.py`
- **Lines**: 32-36
- **Priority**: 3
- **Smell**: Excessive-mocking (review-code P6 "Excessive mocking" / testing.md anti-pattern)
- **Rewrite intent**: replace the mock with the real `InMemoryOrderRepo`; assert on persisted state
- **Status**: pending

---

**Match criterion (see `expected.md`):** the four `(smell-family, rewrite-intent)` pairs above, one
per test function, with `orders.py` (the SUT) NOT flagged. Exact line numbers may drift ±2 as the
file is edited — do not fail the fixture on line-number skew alone.
