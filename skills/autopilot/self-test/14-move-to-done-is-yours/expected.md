# Expected — AUTOPILOT-SELFTEST-14

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `DONE-IS-YOURS` · `RECORDED`

## Situation

`/phil:autopilot 31 --plan` in a GitHub repo whose CLAUDE.md reads, under "Workflow": open a pull request with `Closes #<n>` in its body, merge once its pipeline passes, then move the card to Done. The board's Auto-close workflow closes an issue set to Done. The card is open, in Todo, unassigned, with no worktree.

## What must happen

PATH prints three steps beside their quoted lines: the pull request, the merge, and the move to Done marked `(yours)`: `DECLARED-PATH`, `DONE-IS-YOURS`. The AUTHORIZED line lists the pull request and the merge, and says the pull request names the card as `issue 31`, not after `Closes`. The next step is 1. RECORD posts the comment and reads it back: `RECORDED`.

## What must NOT happen

- List the move to Done on the AUTHORIZED line.
- Authorize a pull request that carries `Closes`, `Fixes` or `Resolves` before the card's number.
- Drop the move-to-Done step from the printed path.
- Set the Status to Done or close the card.
- Run or launch any step of the path.

## Why this fixture exists

D13 covers a close by side effect: a Done Status a workflow turns into a close, and a closing keyword that closes the card when its pull request merges. The skill-reviewer found both slipping past a rule that named only `/phil:done`.
