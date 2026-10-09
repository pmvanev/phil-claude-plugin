# Test Redesign Backlog

Generated: {date}
Scope: --review .

## Summary

- **Total items**: 1
- **Implementation-coupling**: 1
- **Excessive-mocking**: 0
- **Flakiness/determinism**: 0

## Backlog

### [RD001] Implementation-coupling — asserts save() was called on the owned repository

- **File**: `test_orders_boundaries.py`
- **Lines**: 12-15
- **Priority**: 2
- **Smell**: Implementation-coupling — Overspecified Software
- **Rewrite intent**: use the real `InMemoryOrderRepo`; assert `repo.get("A1")` holds the placed order
- **Status**: pending
