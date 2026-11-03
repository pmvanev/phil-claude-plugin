# Expected — START-SELFTEST-09

`LAUNCHED` · `CLAIMED` · `ROUTE-OVERRIDDEN`

## Situation

`/phil:start 12` in a consumer repo whose CLAUDE.md holds a board block and records no build path. The card carries `wave: design` and sits in Todo, unassigned. The developer types `phil:work — the design is settled; this is a rename` under Other.

## What must happen

CLAIM adds nothing the board already holds, writes Status In Progress, assigns the developer, and reads both back: `CLAIMED`. ROUTE reads `/nw-design`, taken from `phil:nwave-issue-board`'s table. The run launches `phil:work` instead and quotes the developer's reason.

## What must NOT happen

- Launch /nw-design over the developer's answer.
- Drop the developer's reason.
- Remove an assignee.

## Why this fixture exists

D9 rule 2, and the learning hypothesis: an override is the evidence that the card and CLAUDE.md did not choose the route.
