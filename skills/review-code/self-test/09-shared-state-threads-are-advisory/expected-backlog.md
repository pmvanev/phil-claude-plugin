# Refactoring Backlog — one race and two Advisory items expected

Scope: .

### [R001] Race — four threads update one dict with no lock in `count_by_carrier`

- **File**: `tally.py`
- **Lines**: 35
- **Priority**: 1
- **Smell**: Race
- **Refactoring**: Guard the shared write with a lock or an atomic, or give each thread its own count and merge once at the end
- **Route**: report only
- **Rationale**: review-code Priority 1, races. `counts.get(...) + 1` then the store is a read-modify-write the threads interleave, so increments can be lost.
- **Status**: pending

### [R002] Advisory — four threads share one dict through a lock; which measurement justified them?

- **File**: `tally.py`
- **Lines**: 15-18
- **Priority**: 1
- **Smell**: Advisory
- **Refactoring**: none — the author decides
- **Route**: report only
- **Rationale**: modern-software-engineering.md — Performance: Concurrency Is Complexity. The threads contend for one lock on every event, and the file shows no measurement that one thread was too slow.
- **Status**: pending

### [R003] Advisory — four threads share one dict in `count_by_carrier`; which measurement justified them?

- **File**: `tally.py`
- **Lines**: 33-35
- **Priority**: 1
- **Smell**: Advisory
- **Refactoring**: none — the author decides
- **Route**: report only
- **Rationale**: modern-software-engineering.md — Performance: Concurrency Is Complexity. The file shows no measurement that one thread was too slow.
- **Status**: pending
