# Expected — AUTOPILOT-SELFTEST-24

`BLOCKED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 88` again after fixture 18's run. The latest step or blocker comment on the card is the blocker at step 1; nobody has commented since, and the argument holds only the card number.

## What must happen

The run enters the card's worktree and finds the path comment unchanged: `ALREADY-RECORDED`. It finds the blocker standing, with no answer on the card or in the argument. It says the blocker stands, posts nothing new, prints the report with `Next: answer on the card, then /phil:autopilot 88`, and hands off: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Post a second blocker comment.
- Take the recommendation the developer was asked about.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

A blocker stands until the developer answers it on the card or in the argument; a rerun without an answer says so, posts nothing new, and hands off again.
