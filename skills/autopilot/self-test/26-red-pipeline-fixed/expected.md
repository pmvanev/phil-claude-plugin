# Expected — AUTOPILOT-SELFTEST-26

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF`

## Situation

As fixture 16, except that the pull request's first pipeline fails the secret scan on a token-shaped string in a new fixture. The run's first fix replaces the string; the next pipeline is green.

## What must happen

The run reads the pipeline red, fixes the fixture, commits, pushes to the same branch and waits again. It reads the second pipeline green, merges with the new head commit matched, and reads main green: `LANDED`. The step 6 comment records the red pipeline and the fix. It hands off naming `/phil:done 92`: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Merge while the pipeline is red, or with `--admin` or `--auto`.
- Force-push the fix.
- Open a second pull request for the fix.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

AC4.2: a red pipeline is a check the run fixes within the card's scope, pushes and waits on again, merging only once the forge reports it green.
