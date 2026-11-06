# Expected outcome — fixture 10 (shell findings cite an SH row)

A release script and its helpers:

- `deploy.sh`, a Bash script with no `errexit`;
- `lib/paths.sh`, a sourced file with neither shebang nor directive;
- `lib/log.sh`, a sourced library that carries a `# shellcheck shell=bash` directive;
- `ci-entry.sh`, a deliberate POSIX `sh` entry point with `set -eu`;
- `rotate-logs.sh`, a Bash script that checks each step itself instead of setting `-e`;
- `check-services.sh`, a Bash script with `set -euo pipefail`, meant to report every service that is
  down;
- `bin/healthcheck`, an extensionless POSIX script that uses `[[ ]]`.

It holds nine defects, each on a line an Always-flag row of `rules/bash.md` describes, beside four
decoys that the rule's Do-not-flag list clears. `test_scripts.py` is green: every script parses under the
shell its shebang names.

**Pins:**

- `review-code` gathers `.sh` files and the extensionless `bin/healthcheck` by its shebang, and checks
  them against `bash.md` as well as `security.md`.
- It names each finding by the row's `SH-n` id and takes the row's Preferred form as its fix.
- It files a hazard row at Priority 1 and every other row at Priority 7.

Before the rule existed, a review checked these files against `security.md` alone and filed none of
them.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the nine items in `expected-backlog.md`. An item
matches on the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this code's one change. Order is not checked.

1. **SH-1** (Priority 1) — `deploy.sh` checks none of `mktemp`, `latest_tag`, `build`, `cp` or the
   upload, and each feeds the next. One item for the script.
2. **SH-2** (Priority 1) — `latest_tag` pipes `curl` into `jq` with no `pipefail`, so a failed request
   yields an empty tag.
3. **SH-3** (Priority 1) — `local version=$(aws …)` returns `local`'s status, not the call's.
4. **SH-4** (Priority 1) — `cp $built` splits and globs the path.
5. **SH-5** (Priority 1) — `build` runs `tar` wherever `cd "$BUILD_DIR"` left it.
6. **SH-9** (Priority 1) — `bin/healthcheck` is `#!/bin/sh` and uses `[[ ]]`, which dash rejects.
7. **SH-11** (Priority 1) — `check-services.sh` calls `check` as a bare command under `errexit`, so
    the first service that is down ends the run and the rest go unchecked.
8. **SH-6** (Priority 7) — `deploy.sh` tests `[ -z "$bucket" ]` in a Bash script.
9. **SH-7** (Priority 7) — `build` assigns `artifact` without `local` and reads it only inside.

**Hard assertions (any failure blocks the skill change):**

- **No item files a decoy as its defect:**
  - `git ls-files | wc -l` in `ci-entry.sh`: a POSIX `sh` script owes no `pipefail`, and `[ ]` and
    `set -eu` there are complete.
  - `gzip --` in `rotate-logs.sh`: a Bash script without `set -e` that checks every command whose
    failure matters.
  - `head -n 1` in `rotate-logs.sh`: a pipeline ending in a reader that closes early, where `pipefail`
    would fail on SIGPIPE.
  - `lib/log.sh`: a sourced library carrying a `# shellcheck shell=bash` directive needs no shebang.
- **No item flags a script merely for lacking `set -e`.** SH-1 names unchecked commands, and
  `rotate-logs.sh` has no SH-1 item.
- **The unchecked `cd` is one SH-5 item**, never also listed under SH-1.
- **SH-1 is one item**, not one per command.
- Every hazard item carries `Priority: 1` and `Route: report only`; every other item carries
  `Priority: 7` and ``Route: `/phil:refactor` ``.

**Not a failure:**

- an Advisory question, where a file shows its subject — the `mktemp -d` with no `trap`, and
  `lib/paths.sh` with neither a shebang nor a directive, are both Advisory now;
- line numbers within ±2, and SH-1's Lines given as a list.

**Driven 2026-11-06** against this working tree's `SKILL.md`, by a fresh agent that read only the
fixture's scripts and test, the rules and the skill, before SH-11 (then SH-12) and `check-services.sh` existed, and before the evidence check moved the
temp-file row and the library clause to Advisory. It
filed all ten items the fixture then held, with the expected rows, priorities and fixes, and no decoy.
Its extras:

- an Advisory question on CI running no ShellCheck, which is allowed;
- a Priority 6 item on the fixture's own test, which looped inside `all()` and is now parametrized.

It also found that `ci-entry.sh` called `deploy.sh --dry-run`, which ignores its arguments; the entry
point now runs the tests instead.
