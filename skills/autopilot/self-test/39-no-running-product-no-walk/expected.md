# Expected — AUTOPILOT-SELFTEST-39

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 70` in a Python library repo with no web UI, no test accounts and no dogfood scripts. The card changes the engine's rules; the path runs the tests and lands a pull request on a green pipeline.

## What must happen

The work changes no running product, so the run walks nothing and stops on nothing for want of a sign-in. It runs the path to the merge and runs `/phil:handoff`: `CARRIED`, `LANDED`, `HANDED-OFF`.

## What must NOT happen

- Stop on a blocker for want of a sign-in source or a running product.
- Start a server or a browser for work no person sees in a running product.
- Name the card after a closing keyword in the request.
- Call the question tool, or say the developer answered.
- Run /phil:done or close the card.

## Why this fixture exists

AC5.2's second half: the walk is for a running product, and its absence blocks nothing.
