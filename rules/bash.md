---
paths:
  - "**/*.sh"
  - "**/*.bash"
---

# Bash and POSIX Shell Guide

Guidelines drawn from the GNU Bash Reference Manual, POSIX.1-2024's Shell Command Language, the Google
Shell Style Guide, the ShellCheck wiki and manual, Greg Wooledge's BashFAQ and BashPitfalls, and Dong et
al., "Bash in the Wild" (ACM TOSEM, 2023). Research:
`docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md` § 1.

This rule owns **how a shell script is written**: whether its failures are checked, how it quotes,
which shell it is written for, and what it cleans up. Neighbouring rules keep what they already own:
`security.md` shell injection (CWE-78) and secrets in a script; `ci-pipelines.md` what a pipeline runs,
including the inline `run:` and `script:` blocks in a CI file, which fall outside this rule's match.
Complement those — do not restate them.

**It applies to** a `.sh` or `.bash` file, and to an extensionless file whose first line is a shebang
naming `sh` or `bash`. The shebang decides the dialect: `#!/bin/bash` and `#!/usr/bin/env bash` are
Bash; `#!/bin/sh` is POSIX `sh`, and a row written for Bash never reaches it. Judge a file with no
shebang by its `# shellcheck shell=` directive and, failing that, as Bash where it ends in `.bash`.
The `paths:` frontmatter cannot express a shebang, so a consumer who copies this rule into
`.claude/rules/` loads it for the extensions alone. A sourced file runs under its caller's options:
read the `set` line of the script that sources it before judging SH-1, SH-2 or SH-11 there.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory and Do not flag —
names the defects a script shows, each by its `SH-n` id. A row is a hazard when a miss changes what
the script does when it runs, and a review files it at Priority 1. A row with no hazard is an idiom: a
cited source names its preferred form, and a review files it at Priority 7. A defect no source names
stays Advisory.
Each row names the ShellCheck check that catches it, where one exists; the review reads and never runs
one. The Principles half is design and yields no finding on its own.

---

## Principles — design, not review criteria

### 1. Check every failure that matters

"Always check return values" (Google). Two mechanisms serve it, and both are sound: `set -euo pipefail`
after the shebang, which stops the script at the first failure, or an explicit `|| exit` or `if !`
on each command whose failure the next step depends on. Wooledge and ShellCheck's own SC2310 page
prefer the explicit form, because Bash suspends `errexit` inside an `if`, a `!`, an `&&` or `||` list
and a command substitution. A script fails this principle when a failure goes unchecked, not when it lacks
`set -e`.

### 2. Write for the shell the shebang names

Bash and POSIX `sh` are different languages. `[[ ]]`, `local`, arrays and the `function` keyword are
Bash. POSIX leaves `[[` and `local` unspecified, and dash — `/bin/sh` on Debian and Ubuntu — rejects
`[[ ]]`, arrays and `function`, though it runs `local`. `pipefail` entered POSIX in 2024, yet dash
and macOS's `sh` adopted it late, so a portable script does without it. Choose the shebang first, then write to it.

### 3. Quote every expansion unless splitting is the point

The shell splits an unquoted `$var` or `$(cmd)` on whitespace and globs the pieces. Quote it. Build a
command line from parts in an array, and expand it as `"${args[@]}"`.

### 4. Remove what the script creates

A temp file, a lock or a background process outlives a script that exits early. Register its removal
with `trap … EXIT` as soon as it exists.

### 5. Shell is for small glue

"Shell should only be used for small utilities or simple wrapper scripts" (Google). Dong et al. found
that a Bash script's error-proneness rises with its size. Past about a hundred lines, or once the
control flow stops being straightforward, the script is a program and belongs in a language with data
structures and tests.

---

## Always-flag — objective defects

Name each finding by its `SH-n` id. Where a defect fits two rows, file the more specific: an unchecked
`cd` is SH-5, never also SH-1. File SH-1 once per script, its Lines listing each unchecked command,
because one `set -euo pipefail` fixes them all; file SH-2 once per pipeline. A defect that is also an
injection path is `security.md`'s CWE-78 alone.

| Id | Violation | Preferred form | Hazard | Linter | Cite |
|----|-----------|----------------|--------|--------|------|
| SH-1 | A Bash script without `errexit` in which a command whose failure the next step depends on goes unchecked | `set -euo pipefail` after the shebang, or `\|\| exit` on that command | hazard | none | Bash manual § 4.3.1; Google, "Return values"; BashFAQ/105 |
| SH-2 | A pipeline in a Bash script with neither `pipefail` nor a `PIPESTATUS` check, which loses the status of every command but the last, where an earlier command can fail (`curl … \| jq …`) | `set -o pipefail`; where an earlier command exits non-zero by design (`grep` matching nothing), test `"${PIPESTATUS[@]}"` on the next line instead | hazard | none | Bash manual § 4.3.1; POSIX.1-2024 `set -o pipefail`; Google, "Checking Return Values"; BashFAQ/105 |
| SH-3 | `local`, `export`, `declare` or `readonly` and a command substitution in one statement: the keyword's status replaces the command's | Declare on one line, assign on the next | hazard | SC2155 | Google, "Use Local Variables"; BashPitfalls, "local var=$(cmd)"; ShellCheck SC2155 |
| SH-4 | A parameter expansion or command substitution left unquoted in a command's arguments, an array assignment, a `[ ]` test or a `for` list | Double-quote it; use `"$@"`; in Bash, build a command line in an array | hazard | SC2086, SC2046, SC2206 | Google, "Quoting"; BashPitfalls, `[ $foo = "bar" ]`; ShellCheck SC2086 |
| SH-5 | `cd` unchecked in a script without `errexit` | `cd dir \|\| exit` | hazard | SC2164 | BashPitfalls, "cd /foo; bar"; ShellCheck SC2164 |
| SH-6 | `[ … ]` or `test` in a Bash script | `[[ … ]]` | — | SC2292 (optional) | Google, "Test, `[ … ]`, and `[[ … ]]`" |
| SH-7 | A variable assigned inside a Bash function without `local`, and read only inside it | `local name` | — | none | Google, "Use Local Variables" |
| SH-8 | An executable file with no shebang, so the shell that invokes it decides how it runs | A shebang naming the shell | hazard | SC2148 | Google, "File Extensions"; ShellCheck SC2148 |
| SH-9 | A `#!/bin/sh` script that uses a Bash feature dash rejects: `[[ ]]`, an array, `function`, or `set -o pipefail` where `/bin/sh` may be an older dash or macOS's `sh` | Write it in POSIX `sh`, or change the shebang to Bash | hazard | SC3010, SC3040 (`pipefail`, through ShellCheck 0.11.0) | POSIX.1-2024 § 2.4; ShellCheck SC3010; ShellCheck issue 2555 |
| SH-10 | A loop over the output of `ls`, or over an unquoted `$(find …)` | A glob (`for f in ./*.log`), or `find … -print0 \| while IFS= read -r -d '' f` | hazard | SC2045, SC2044 | BashPitfalls, `for f in $(ls *.mp3)`; ShellCheck SC2045, SC2044 |
| SH-11 | In a script with `errexit`, a command or function whose non-zero status reports a result rather than a failure — a check that returns 1 — called as a bare command, so the first negative result ends the script | Call it in a condition: `if ! check; then …`, or `check \|\| failed=1` | hazard | none | Bash manual § 4.3.1; BashFAQ/105 |

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides.

- **A script that has outgrown shell.** Google: "If you are writing a script that is more than 100
  lines long, or that uses non-straightforward control flow logic, you should rewrite it in a more
  structured language *now*." Ask whether to rewrite it in Python, and lead with the signal that makes
  it a program: branching state, arrays of records, JSON or CSV parsed in shell, functions that pass
  results through return codes. A long, linear list of commands is the weak case; say so. Length is
  never a defect on its own line.
- **A temp file, temp directory, lock or background process with no `trap … EXIT` to remove it.**
  The usual form is `tmp=$(mktemp)`, then `trap 'rm -f "$tmp"' EXIT`; in a sourced file, remove it on
  every return path instead, since an EXIT trap there replaces the caller's. Dong et al. name resource
  management a common problem, but no source names this form; ask.
- **A `.sh` library with neither a shebang nor a `# shellcheck shell=` directive.** Google gives a
  library no shebang; the directive tells ShellCheck and a reader which shell it is written for
  (SC2148).
- **`local` in a `#!/bin/sh` script** (SC3043): POSIX leaves it unspecified, though dash, BusyBox ash
  and ksh run it. Ask whether the script must run on a shell without it.
- **`trap` with a double-quoted command** (SC2064): its expansions run when the trap is set, not when
  it fires. Sometimes intended; ask.
- **A command substitution used as an argument whose failure matters**, `cmd "$(fetch)"`: the outer
  command runs whatever `fetch` returned (SC2312, opt-in).
- **A function that relies on `set -e` and is called inside an `if`, a `!`, an `&&` or `||` list, or a
  command substitution**, where `errexit` is off for its whole body (SC2310, SC2311, opt-in).
- **`a && b || c` used as if-then-else**: `c` runs when `b` fails too (BashPitfalls). The same holds
  for `… | head || fallback`: the reader's status decides, so the fallback rarely runs.
- **A retry loop that falls through when its retries run out**, with no check after it.
- **`eval`**: Google says to avoid it. Where its input is untrusted, it is `security.md`'s CWE-78
  instead.
- **No ShellCheck in the project's CI.** Raise it only where the review read the CI config. One item
  per project, not per script.

---

## Do not flag

- **A `#!/bin/sh` script** that omits `pipefail`, `[[ ]]` or `local`. `set -eu` there is complete.
- **A Bash script without `set -e`** where every command whose failure matters is checked explicitly.
- **A sourced library with no shebang** that carries a `# shellcheck shell=` directive. Google: a
  library has a `.sh` extension and is not executable.
- **A variable ShellCheck calls unused** (SC2034) that a sourcing script, `envsubst` or a template
  reads.
- **An expansion that cannot split or glob**: `$#`, `$?`, `$$`, `$!`, an arithmetic context, the left
  side of `[[ ]]`, and a variable the script assigns a literal with no space or glob character.
- **Splitting on purpose** over output that cannot glob: `for i in $(seq 1 30)`.
- **A temp file in a sourced file** removed on every return path, where the caller owns the EXIT trap.
- **A pipeline without `pipefail` that ends in a reader closing early** — `head`, `grep -q` — where
  `pipefail` would turn the writer's SIGPIPE into a failure.
- **A row the project's ShellCheck already enforces**: CI runs ShellCheck, and its config enables that
  row's check at the severity its CI reports. Read both: `require-double-brackets` is opt-in, and
  SC2086 is `info`, so `shellcheck -S warning` never reports SH-4's main check. A row whose Linter cell
  reads none never stands down.
