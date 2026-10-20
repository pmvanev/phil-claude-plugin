# Refactoring Backlog — Priority 1 security items expected

Scope: .

### [R001] CWE-78 — hook runs the model's reply in a shell

- **File**: `board_sync.py`
- **Lines**: 11-13
- **Priority**: 1
- **Smell**: CWE-78
- **Refactoring**: Treat model output as untrusted input: the injection rows above apply — here: argument list, no shell, chosen from fixes the hook already knows
- **Route**: report only
- **Rationale**: security.md — CWE-78, CWE-94, CWE-79, CWE-22 · LLM05:2025; a hook grants more than the model's own grant
- **Status**: pending

### [R002] CWE-1427 — label names in a prompt that holds a shell

- **File**: `board_sync.py`
- **Lines**: 16-19
- **Priority**: 1
- **Smell**: CWE-1427
- **Refactoring**: Read it in a context with no tools (Dual LLM); fix the plan before reading it (Plan-Then-Execute)
- **Route**: report only
- **Rationale**: security.md — CWE-1427 · LLM01:2025; forge metadata is untrusted
- **Status**: pending

### [R003] CWE-250 — a bare shell granted to group labels

- **File**: `board_sync.py`
- **Lines**: 19
- **Priority**: 1
- **Smell**: CWE-250
- **Refactoring**: Only the tools the task needs; a shell or a write bounded by a hook that allows its exact commands or paths and refuses the rest
- **Route**: report only
- **Rationale**: security.md — CWE-250 · LLM06:2025
- **Status**: pending

### [R004] CWE-1427 — label names written verbatim into CLAUDE.md

- **File**: `board_sync.py`
- **Lines**: 35-36
- **Priority**: 1
- **Smell**: CWE-1427
- **Refactoring**: Render it as inert data — an allow-listed character set, a length cap, no newlines, backticks or marker text — or keep it out and record only ids
- **Route**: report only
- **Rationale**: security.md — CWE-1427 · LLM01:2025; an instruction file is a prompt every later session reads
- **Status**: pending
