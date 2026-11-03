# Expected — START-SELFTEST-11

`LAUNCHED` · `WROTE-NOTHING`

## Situation

`/phil:start 93` in a consumer repo whose CLAUDE.md records no build path. The card asks to fix one broken link in the README, lists it under *Done when*, and leaves nothing open. The developer answers **start it**.

## What must happen

ROUTE reads `inline` — one done-when item, nothing open. On the yes, the session begins the fix itself; no skill is invoked.

## What must NOT happen

- Route a one-line fix through phil:edd.
- Invoke a skill for an inline route.
- Write a Status or assign anyone.

## Why this fixture exists

D9 rule 4: a card that fits one sitting goes inline, overriding rule 3.
