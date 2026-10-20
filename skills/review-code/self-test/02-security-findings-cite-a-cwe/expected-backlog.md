# Refactoring Backlog — Priority 1 security items expected

Scope: .

### [R001] CWE-798 — production password assigned in source

- **File**: `ingest.py`
- **Lines**: 13
- **Priority**: 1
- **Smell**: CWE-798
- **Refactoring**: Load from a secrets manager, or the runtime environment where none exists; rotate the leaked value
- **Route**: report only
- **Rationale**: security.md — CWE-798 · v5.0.0 V13
- **Status**: pending

### [R002] CWE-89 — caller's owner formatted into SQL

- **File**: `ingest.py`
- **Lines**: 27-29
- **Priority**: 1
- **Smell**: CWE-89
- **Refactoring**: Parameterized query or the driver's builder
- **Route**: report only
- **Rationale**: security.md — CWE-89, CWE-943 · v5.0.0 V1
- **Status**: pending

### [R003] CWE-338 — reset code drawn from a non-cryptographic RNG

- **File**: `ingest.py`
- **Lines**: 48-49
- **Priority**: 1
- **Smell**: CWE-338
- **Refactoring**: The platform CSPRNG (`secrets`, `crypto.randomBytes`, `SecureRandom`)
- **Route**: report only
- **Rationale**: security.md — CWE-338, CWE-330 · v5.0.0 V11
- **Status**: pending

### [R004] CWE-502 — request body unpickled

- **File**: `ingest.py`
- **Lines**: 61-63
- **Priority**: 1
- **Smell**: CWE-502
- **Refactoring**: A data-only format (JSON) with a schema; `yaml.safe_load`
- **Route**: report only
- **Rationale**: security.md — CWE-502 · v5.0.0 V1
- **Status**: pending

### [R005] CWE-295 — certificate verification turned off

- **File**: `ingest.py`
- **Lines**: 66-69
- **Priority**: 1
- **Smell**: CWE-295
- **Refactoring**: Verify; for a private CA, trust that CA explicitly — here: drop the unverified context, which turns certificate checking off
- **Route**: report only
- **Rationale**: security.md — CWE-295, CWE-297 · v5.0.0 V12
- **Status**: pending

### [R006] CWE-297 — hostname verification turned off with it

- **File**: `ingest.py`
- **Lines**: 66-69
- **Priority**: 1
- **Smell**: CWE-297
- **Refactoring**: Verify; for a private CA, trust that CA explicitly — here: drop the unverified context, which also turns hostname checking off
- **Route**: report only
- **Rationale**: security.md — CWE-295, CWE-297 · v5.0.0 V12; one item per id that fires
- **Status**: pending

### [R007] CWE-78 — shell string built from an issue title

- **File**: `ingest.py`
- **Lines**: 72-75
- **Priority**: 1
- **Smell**: CWE-78
- **Refactoring**: Argument list, no shell (`subprocess.run([...])`, `execFile`)
- **Route**: report only
- **Rationale**: security.md — CWE-78, CWE-77 · v5.0.0-1.2.5
- **Status**: pending

### [R008] CWE-1427 — issue body in a prompt that holds a shell

- **File**: `ingest.py`
- **Lines**: 80-81
- **Priority**: 1
- **Smell**: CWE-1427
- **Refactoring**: Read it in a context with no tools (Dual LLM); fix the plan before reading it (Plan-Then-Execute)
- **Route**: report only
- **Rationale**: security.md — CWE-1427 · LLM01:2025
- **Status**: pending

### [R009] CWE-250 — triage agent granted a bare shell to apply a label

- **File**: `ingest.py`
- **Lines**: 81
- **Priority**: 1
- **Smell**: CWE-250
- **Refactoring**: The narrowest grant that does the job (`Bash(git log:*)`, not `Bash`)
- **Route**: report only
- **Rationale**: security.md — CWE-250 · LLM06:2025
- **Status**: pending

### [R010] CWE-78 — model reply run in a shell

- **File**: `ingest.py`
- **Lines**: 82
- **Priority**: 1
- **Smell**: CWE-78
- **Refactoring**: Treat model output as untrusted input: the injection rows above apply — here: argument list, no shell, chosen from a fixed set of label commands
- **Route**: report only
- **Rationale**: security.md — CWE-78, CWE-94, CWE-79, CWE-22 · LLM05:2025
- **Status**: pending
