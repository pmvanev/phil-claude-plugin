# Refactoring Backlog — Priority 6 items expected

Scope: .

### [R001] Mystery Guest — expected total lives in a file the test never shows

- **File**: `test_invoice.py`
- **Lines**: 8-11
- **Priority**: 6
- **Smell**: Mystery Guest
- **Refactoring**: Inline the data
- **Route**: report only
- **Rationale**: test-patterns.md — the reader must see cause and effect in the test
- **Status**: pending

### [R002] Conditional Test Logic — loop, branch and computed expectations

- **File**: `test_invoice.py`
- **Lines**: 14-21
- **Priority**: 6
- **Smell**: Conditional Test Logic
- **Refactoring**: Parameterized Test
- **Route**: report only
- **Rationale**: test-patterns.md "No logic in tests" — expected values are literals
- **Status**: pending

### [R003] Sensitive Equality — compares repr() to check customer and total

- **File**: `test_invoice.py`
- **Lines**: 24-26
- **Priority**: 6
- **Smell**: Sensitive Equality
- **Refactoring**: Assert on observable outcome
- **Route**: /phil:redesign-tests
- **Rationale**: test-patterns.md — verify the outcome, not its rendering
- **Status**: pending
