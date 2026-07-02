# Test Refactoring Backlog

Generated: {date}
Scope: --review .

## Summary

- **Total items**: 4
- **Extract Fixture/Helper (duplicated setup)**: 1
- **Reorder into Arrange-Act-Assert (missing AAA)**: 1
- **Extract Test Helper (long test)**: 1
- **Rename (vague name)**: 1

## Backlog

### [T001] Duplicated setup — same cart literal built in two tests

- **File**: `test_cart_smells.py`
- **Lines**: 6-13
- **Priority**: 2
- **Smell**: Duplicated setup (D5)
- **Move**: Extract Fixture/Helper
- **Rationale**: `testing.md` — shared arrange belongs in a fixture, not copy-pasted per test. Assertion-preserving.
- **Status**: pending

### [T002] Missing AAA — arrange/act/assert interleaved

- **File**: `test_cart_smells.py`
- **Lines**: 24-30
- **Priority**: 2
- **Smell**: Missing AAA structure (D5)
- **Move**: Reorder into Arrange-Act-Assert
- **Rationale**: `testing.md` — one clear arrange → act → assert flow; the test currently re-arranges mid-test. Reordering preserves the assertions.
- **Status**: pending

### [T003] Long test — repeated per-scenario block

- **File**: `test_cart_smells.py`
- **Lines**: 34-44
- **Priority**: 3
- **Smell**: Long test with an extractable block (D5)
- **Move**: Extract Test Helper
- **Rationale**: `testing.md` — the repeated (build cart → assert total) block extracts to a helper; each assertion is preserved verbatim.
- **Status**: pending

### [T004] Vague name — says nothing about what is verified

- **File**: `test_cart_smells.py`
- **Lines**: 18-19
- **Priority**: 3
- **Smell**: Vague test name (D5)
- **Move**: Rename
- **Rationale**: `testing.md` — a test name should state the behaviour under test; `test_it_works` does not. Rename is assertion-preserving.
- **Status**: pending

---

**Match criterion (see `expected.md`):** the four `(smell, move)` pairs above, one per test
function, with `cart.py` (the SUT) NOT flagged. Exact line numbers may drift ±2 as the file is
edited — do not fail the fixture on line-number skew alone.
