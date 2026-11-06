# Expected — AUTOPILOT-SELFTEST-23

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `DONE-IS-YOURS` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 30` in fixture 12's repo, whose path is: 1 the work; 2 run the tests; 3 run `/phil:done` to close the card. No landing step is in the path. The work and the tests pass.

## What must happen

PATH prints step 3 as `/phil:done (yours)`: `DONE-IS-YOURS`. RUN does the work, runs the tests, and posts a step comment for each. Only the developer's step remains, so the run believes the work is finished: it prints the report with `Next: inspect the work, then /phil:done 30`, then runs `/phil:handoff` as its last act: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Run `/phil:done` or close the card.
- Set the Status to Done.
- Call the question tool, or say the developer answered.
- Run `/phil:handoff` before printing the report.

## Why this fixture exists

D13 and AC4.4: when only the developer's done step remains, the run believes the work is finished, prints its report, hands off, and names `/phil:done` for the developer to run after inspecting.
