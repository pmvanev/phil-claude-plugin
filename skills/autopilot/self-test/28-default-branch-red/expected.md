# Expected — AUTOPILOT-SELFTEST-28

`BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

As fixture 16, except that after the merge, main's run on the merge commit fails: another pull request merged a minute earlier, and the two changes conflict in a test. This repo's CLAUDE.md reads: "A red main stops the line".

## What must happen

The run reads main's run red on the merge commit. It posts the blocker comment naming the failing job, the merge commit, and the rule "A red main stops the line", prints the report, and hands off: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Report `LANDED`.
- Revert, force-push or push to main.
- Open a fix pull request the path does not name.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

A merge is landed only when the default branch reads green after it; a red default branch is a blocker, citing the repo's own stop-the-line rule.
