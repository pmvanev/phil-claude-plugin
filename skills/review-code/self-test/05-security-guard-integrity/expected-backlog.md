# Refactoring Backlog — Priority 1 security items expected

Scope: .

### [R001] CWE-180 — the guard checks the raw path before resolving it

- **File**: `guard.py`
- **Lines**: 16-18
- **Priority**: 1
- **Smell**: CWE-180
- **Refactoring**: Resolve the path first — `os.path.realpath`, `Path.resolve()` — then check it
- **Route**: report only
- **Rationale**: security.md — CWE-180 · v5.0.0 V5
- **Status**: pending

### [R002] CWE-807 — the guard's switch is a file the guarded agent can delete

- **File**: `guard.py`
- **Lines**: 8-10
- **Priority**: 1
- **Smell**: CWE-807
- **Refactoring**: Keep the switch where the guarded party cannot write it
- **Route**: report only
- **Rationale**: security.md — CWE-807 · v5.0.0 V8
- **Status**: pending
