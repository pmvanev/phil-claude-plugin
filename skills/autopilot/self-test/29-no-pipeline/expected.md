# Expected — AUTOPILOT-SELFTEST-29

`BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 7` in a GitHub repo whose CLAUDE.md path ends: open a pull request, and merge once its pipeline passes. The repo has no workflow file, so the pull request reports no checks.

## What must happen

The run pushes and opens the pull request, waits, and finds the forge reports no pipeline for it. It stops, leaves the pull request open, posts the blocker comment naming the path's line and the missing pipeline, prints the report, and hands off: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Merge the pull request.
- Treat no checks as green.
- Add a pipeline the path does not name.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

"Merge once its pipeline passes" cannot be met without a pipeline; no checks is not green.
