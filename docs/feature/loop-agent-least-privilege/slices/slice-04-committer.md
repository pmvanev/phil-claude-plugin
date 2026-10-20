# Slice 04 — The committer

**Goal.** Committing a green refactoring stages only the paths the patch names.

**Story:** US-04 · **Job:** delegate-mechanical-steps-without-handing-over-a-shell

## IN scope
- `agents/refactor-committer.md` (`Read`, `Write`, `Bash`).
- Hook rules: the message file's path pinned for `Read`/`Write`; `git add -- <paths>` with every path
  named in the patch file; `git commit -F <message file>`.
- The commit call passes `agentType`; every diff scan refuses a diff touching the message file.
- Hooks README: the repository's own pre-commit hooks still run its code.

## OUT scope
- Signing, amending or pushing.

## Learning hypothesis
Disproves "the patch bounds the commit" **if** a green refactoring needs a staged path the patch does
not name, such as a file the build regenerates.

## Acceptance criteria
See US-04 in `feature-delta.md`.

## Dependencies
Slice 03 (the patch file).

## Effort / reference class
≤ half a day.

## Production data
A real run with at least one commit, plus a live probe.
