# Expected — AUTOPILOT-SELFTEST-20

`CARRIED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `RESUMED` · `HANDED-OFF`

## Situation

`/phil:autopilot 92` again, after fixture 19's run, from the main checkout. The card carries the path comment, step comments for steps 2 and 3, and the blocker comment at step 4; beneath the blocker the developer commented: "the fixture was stale — regenerate it and go on". The path is unchanged.

## What must happen

The claim finds every write made: `CLAIMED`. WORKTREE enters the card's worktree: `UNDERWAY`, `WORKTREE-ENTERED`. The path comment matches on its quoted lines and authorized step numbers, though steps 2 and 3 are now done: `ALREADY-RECORDED`. RUN finds steps 2 and 3 marked done by step comments that quote the same source lines, and starts at step 4: `RESUMED`. The latest step or blocker comment is the blocker, and the developer's later comment answers it. The run regenerates the fixture, re-runs the tests, commits, stops before step 6, and hands off: `CARRIED`, `HANDED-OFF`. The step 4 comment records the answer as the developer's comment, quoted.

## What must NOT happen

- Rerun steps 2 or 3.
- Post a second path comment.
- Ask the blocker's question again.
- Call the question tool, or say the developer answered a question the run decided.
- Run `/phil:done` or close the card.

## Why this fixture exists

AC3.2: the next run resumes at the step that stopped, taking the developer's answer from the card, not at the first.
