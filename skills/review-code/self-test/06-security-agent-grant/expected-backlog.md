# Refactoring Backlog — Priority 1 security items expected

Scope: .

### [R001] CWE-250 — a command pattern grants the history reader the whole shell

- **File**: `release_notes.py`
- **Lines**: 6-10
- **Priority**: 1
- **Smell**: CWE-250
- **Refactoring**: Only the tools the task needs; a shell or a write bounded by a hook that allows its exact commands or paths and refuses the rest
- **Route**: report only
- **Rationale**: security.md — CWE-250 · LLM06:2025
- **Status**: pending
