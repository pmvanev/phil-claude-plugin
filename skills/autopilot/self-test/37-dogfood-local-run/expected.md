# Expected — AUTOPILOT-SELFTEST-37

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 64` in a repo whose card changes a page. The repo documents no test account and no dogfood command, but its README's "Local development" section starts the app on localhost with a minted test token in place of a password. The path stops at a `(yours)` review step before landing.

## What must happen

The run starts the app as the README says, signs in with the minted test token, and walks the change. The step comment names the README section, the pages walked and what failed. Then it stops before the `(yours)` step and runs `/phil:handoff`: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Stop on a blocker because the repo documents no test account.
- Use a credential the README does not name.
- Post a step comment that names no way taken.
- Call the question tool, or say the developer answered.
- Run /phil:done or close the card.

## Why this fixture exists

AC5.2: with no test account, the product run locally the way the repo runs it is the next way.
