# Expected — START-SELFTEST-11

`LAUNCHED` · `CLAIMED`

## Situation

`/phil:start 93` in a consumer repo whose CLAUDE.md holds a board block and records no build path. The card, in Todo and unassigned, asks to fix one broken link in the README, lists it under *Done when*, and leaves nothing open. The developer answers **start it**.

## What must happen

CLAIM adds nothing the board already holds, writes Status In Progress, assigns the developer, and reads both back: `CLAIMED`. ROUTE reads `inline` — one done-when item, nothing open. On the yes, the run prints its outcome tokens and ends; the session begins the fix, and no skill is invoked.

## What must NOT happen

- Route a one-line fix through phil:edd.
- Invoke a skill for an inline route.
- Remove an assignee.

## Why this fixture exists

D9 rule 4: a card that fits one sitting goes inline, overriding rule 3.
