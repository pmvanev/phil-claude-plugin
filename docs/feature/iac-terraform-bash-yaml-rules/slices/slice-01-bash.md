# Slice 01 — Shell scripts reviewed by row

**Goal.** `/phil:review-code` names each shell-script defect by its `SH-n` row and fix, and leaves a
POSIX `sh` script's deliberate omissions alone.

**Story:** US-01 · **Job:** catch-infrastructure-and-script-defects-in-review

## IN scope
- `rules/bash.md`, holding:
  - frontmatter, an ownership paragraph (shell injection stays in `security.md`) and Principles;
  - Always-flag rows with `SH-n` ids, hazard marks and ShellCheck codes;
  - Advisory, including the rewrite-in-Python question (D10), and Do not flag (D8).
- `review-code`'s *Language idioms* step names `bash.md` and its match (D9). The review checks
  gathered shell files against it as well as `security.md`.
- Hazard promotion to Priority 1 (D4), stated once in `review-code`, where all four rules can use it.
- A self-test fixture with four or more seeded violations and two or more decoys, one of them a POSIX
  script.
- README Rules list; version bump.

## OUT scope
- Running ShellCheck (D13). Zsh, Fish and PowerShell.

## Learning hypothesis
Disproves "a reviewing rule adds defects a linter misses, without restating the linter" **if** the
dogfood run over the 238 sibling scripts finds nothing beyond ShellCheck's own output. It also disproves
the hazard tier **if** the fixture run files a hazard row at Priority 7, or a decoy at all.

## Acceptance criteria
See US-01 in `feature-delta.md`.

## Dependencies
- Research precursor, Bash section (committed before this slice).

## Effort / reference class
≤ 1 day. Reference class: `security-standards-rule` slice 01 (a new rule plus one `review-code` step).

## Production data
The 238 scripts in `~/Git/ia-gitlab`: 107 without `-e`, 82 without `pipefail`, and three over 900 lines.
This repo's 19 scripts are the ShellCheck-clean control.
