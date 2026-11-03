# Expected — START-SELFTEST-11

`LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

`/phil:start 93` in a consumer repo whose CLAUDE.md holds a board block and records no build path. The card, in Todo and unassigned, asks to fix one broken link in the README, lists it under *Done when*, and leaves nothing open. The developer answers **start it**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. ROUTE reads `inline` — one done-when item, nothing open. On the yes, the run prints its outcome tokens and ends; the session begins the fix, and no skill is invoked. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Route a one-line fix through phil:edd.
- Invoke a skill for an inline route.
- Remove an assignee.
- Launch the route, or begin an inline fix, before the session is in the new worktree.

## Why this fixture exists

D9 rule 4: a card that fits one sitting goes inline, overriding rule 3.
