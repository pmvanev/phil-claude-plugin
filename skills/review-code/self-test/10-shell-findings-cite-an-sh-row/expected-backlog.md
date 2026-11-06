# Refactoring Backlog — shell items expected

Scope: .

## Backlog

### [R001] SH-1 — the deploy steps run unchecked, each feeding the next

- **File**: `deploy.sh`
- **Lines**: 30-34
- **Priority**: 1
- **Smell**: SH-1
- **Refactoring**: `set -euo pipefail` after the shebang, or `|| exit` on that command — here: add `set -euo pipefail` on line 2, so a failed `mktemp`, `latest_tag`, `build` or `cp` stops the upload
- **Route**: report only
- **Rationale**: bash.md — Bash manual § 4.3.1; Google, "Return values"; BashFAQ/105
- **Status**: pending

### [R002] SH-2 — a failed release request yields an empty tag

- **File**: `deploy.sh`
- **Lines**: 15
- **Priority**: 1
- **Smell**: SH-2
- **Refactoring**: `set -o pipefail`; where an earlier command exits non-zero by design (`grep` matching nothing), test `"${PIPESTATUS[@]}"` on the next line instead — here: `set -o pipefail` before `curl … | jq …` in `latest_tag`
- **Route**: report only
- **Rationale**: bash.md — Bash manual § 4.3.1; POSIX.1-2024 `set -o pipefail`; Google, "Pipes"; BashFAQ/105
- **Status**: pending

### [R003] SH-3 — `local` masks the SSM call's status

- **File**: `deploy.sh`
- **Lines**: 19
- **Priority**: 1
- **Smell**: SH-3
- **Refactoring**: Declare on one line, assign on the next — here: `local version`, then `version=$(aws ssm get-parameter …)`
- **Route**: report only
- **Rationale**: bash.md — Google, "Use Local Variables"; BashPitfalls, "local var=$(cmd)"; ShellCheck SC2155
- **Status**: pending

### [R004] SH-4 — the artifact path is split and globbed

- **File**: `deploy.sh`
- **Lines**: 33
- **Priority**: 1
- **Smell**: SH-4
- **Refactoring**: Double-quote it; use `"$@"`; in Bash, build a command line in an array — here: `cp "$built" "$tmp/"`
- **Route**: report only
- **Rationale**: bash.md — Google, "Quoting"; BashPitfalls, `[ $foo = "bar" ]`; ShellCheck SC2086
- **Status**: pending

### [R005] SH-5 — `tar` runs wherever a failed `cd` left it

- **File**: `deploy.sh`
- **Lines**: 25
- **Priority**: 1
- **Smell**: SH-5
- **Refactoring**: `cd dir || exit` — here: `cd "$BUILD_DIR" || exit`
- **Route**: report only
- **Rationale**: bash.md — BashPitfalls, "cd /foo; bar"; ShellCheck SC2164
- **Status**: pending

### [R006] SH-10 — a POSIX script uses `[[ ]]`

- **File**: `bin/healthcheck`
- **Lines**: 6
- **Priority**: 1
- **Smell**: SH-10
- **Refactoring**: Write it in POSIX `sh`, or change the shebang to Bash — here: `if [ "$status" = ok ]; then`
- **Route**: report only
- **Rationale**: bash.md — POSIX.1-2024 § 2.4; ShellCheck SC3010, SC3043; ShellCheck issue 2555
- **Status**: pending

### [R007] SH-6 — `[ ]` in a Bash script

- **File**: `deploy.sh`
- **Lines**: 9
- **Priority**: 7
- **Smell**: SH-6
- **Refactoring**: `[[ … ]]` — here: `if [[ -z "$bucket" ]]; then`
- **Route**: `/phil:refactor`
- **Rationale**: bash.md — Google, "Test, `[ … ]`, and `[[ … ]]`"
- **Status**: pending

### [R008] SH-7 — `build` leaks `artifact` into the script

- **File**: `deploy.sh`
- **Lines**: 24
- **Priority**: 7
- **Smell**: SH-7
- **Refactoring**: `local name` — here: `local artifact` at the top of `build`
- **Route**: `/phil:refactor`
- **Rationale**: bash.md — Google, "Use Local Variables"
- **Status**: pending

### [R009] SH-8 — the temp directory outlives the script

- **File**: `deploy.sh`
- **Lines**: 30
- **Priority**: 7
- **Smell**: SH-8
- **Refactoring**: `tmp=$(mktemp)`, then `trap 'rm -f "$tmp"' EXIT`; in a sourced file, remove it on every return path, since an EXIT trap there replaces the caller's — here: `trap 'rm -rf "$tmp"' EXIT` after `mktemp -d`
- **Route**: `/phil:refactor`
- **Rationale**: bash.md — Dong et al. 2023, "resource management"
- **Status**: pending

### [R010] SH-9 — a sourced file names no shell

- **File**: `lib/paths.sh`
- **Lines**: 1
- **Priority**: 7
- **Smell**: SH-9
- **Refactoring**: A shebang naming the shell; in a sourced library, the directive — here: `# shellcheck shell=bash` on line 1
- **Route**: `/phil:refactor`
- **Rationale**: bash.md — Google, "File Extensions"; ShellCheck SC2148 and manual
- **Status**: pending

### [R011] SH-12 — the first service that is down ends the check

- **File**: `check-services.sh`
- **Lines**: 15
- **Priority**: 1
- **Smell**: SH-12
- **Refactoring**: Call it in a condition: `if ! check; then …`, or `check || failed=1` — here: `check "$url" || failed=1` in the loop, then `exit "$failed"` after it
- **Route**: report only
- **Rationale**: bash.md — Bash manual § 4.3.1; BashFAQ/105
- **Status**: pending
