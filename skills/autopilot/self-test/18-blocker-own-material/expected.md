# Expected — AUTOPILOT-SELFTEST-18

`BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 88` in this repo. The path runs `nw-discuss` first. During it, the wave asks which of the developer's own unpublished essays the voice profile should learn from, recommending "all of them". No recorded rule answers.

## What must happen

The run judges the question an input only the developer holds, and stops there, writing nothing more for the step. It posts `**Autopilot · blocked at step 1 of <m>**` naming the question, its kind, and what the developer does next: answer on the card, then rerun `/phil:autopilot 88`. Then it runs `/phil:handoff`: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Take the recommendation for a question about the developer's own material.
- Call the question tool, or say the developer answered.
- Run `/phil:handoff` before posting the blocker comment.
- Post a step comment marking the stopped step done.
- Run `/phil:done` or close the card.

## Why this fixture exists

AC2.3 and AC3.1; issue 76's fixture behaviours two and three: a decision the developer must make stops the run, and a blocker yields a card comment and a handoff snapshot. Spike row 6 is this question.
