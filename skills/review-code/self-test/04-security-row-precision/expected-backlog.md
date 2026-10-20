# Refactoring Backlog — Priority 1 security items expected

Scope: .

### [R001] CWE-88 — model-composed slug passed to gh as a positional argument

- **File**: `probe.py`
- **Lines**: 11
- **Priority**: 1
- **Smell**: CWE-88
- **Refactoring**: End options with `--`, or reject a leading `-`
- **Route**: report only
- **Rationale**: security.md — CWE-88 · v5.0.0 V1; the script grants `gh`, which the model's grant lacks
- **Status**: pending

### [R002] CWE-943 — owner and name formatted into a GraphQL literal

- **File**: `probe.py`
- **Lines**: 12-13
- **Priority**: 1
- **Smell**: CWE-943
- **Refactoring**: Parameterized query or the driver's builder
- **Route**: report only
- **Rationale**: security.md — CWE-89, CWE-943 · v5.0.0 V1; the earlier call is no guard
- **Status**: pending

### [R003] CWE-1333 — a backtracking path pattern run on text of any length

- **File**: `probe.py`
- **Lines**: 6, 19
- **Priority**: 1
- **Smell**: CWE-1333
- **Refactoring**: Limits at the boundary; a pattern without nested quantifiers, or a linear-time engine — here: cap the question's length before the scan
- **Route**: report only
- **Rationale**: security.md — CWE-1333 · v5.0.0 V2; one defect, the more specific id
- **Status**: pending

### [R004] CWE-636 — the test guard allows the write on an unparseable payload

- **File**: `probe.py`
- **Lines**: 33-36
- **Priority**: 1
- **Smell**: CWE-636
- **Refactoring**: Fail closed: an unexpected path denies
- **Route**: report only
- **Rationale**: security.md — CWE-636 · v5.0.0 V16; the guard is a security control
- **Status**: pending
