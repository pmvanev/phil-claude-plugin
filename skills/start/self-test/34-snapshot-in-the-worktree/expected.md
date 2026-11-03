# Expected — START-SELFTEST-34

`UNDERWAY` · `CLAIMED` · `WORKTREE-ENTERED` · `WROTE-NOTHING`

## Situation

`/phil:start 80`, with card 80 already In Progress and assigned to `pmvanev`. The card's worktree `issue-80-phil-start` holds a `.session-handoff.md`.

## What must happen

CLAIM finds every write made and writes nothing: `CLAIMED: already In Progress and assigned to pmvanev — nothing written`. WORKTREE enters it and says it holds a handoff snapshot that `/phil:resume` reads; the report names `/phil:resume` as the next step.

## What must NOT happen

- Read the snapshot's exchanges.
- Recommend a route.
- Cut a second worktree.
- Remove an assignee.
- Write a Status the card already holds.

## Why this fixture exists

D2, AC4.3: a card with a snapshot is resumed, not started.
