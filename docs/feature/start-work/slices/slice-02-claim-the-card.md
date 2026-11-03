# Slice 02 — Claim the card

**Goal (one sentence):** `/phil:start <card>` adds the card to the board if missing, sets Status to
In Progress, assigns it to the signed-in account and reads both back.

Story 3 · Decisions D5, D6, D8.

## IN scope
- The board write in `phil:issue-board`'s order: add the item if missing, write Status, assign, read
  Status and assignees back.
- Status ids from the repo's board block; with no block, name `phil:board-setup` and write no Status.
- The developer as `viewer { login }`, named in the report; no signed-in account, or one the forge
  will not assign, reported with nothing assigned.
- Adding the developer beside another assignee only on a yes; never removing one.
- Filing a card in the developer's words on the yes slice 01 offered, then claiming it.
- Fixtures: a card not on the board; a read-back mismatch; no signed-in account; an unassignable
  account; no board block; another's card, answered yes; a card filed on a yes.

## OUT of scope
- The worktree (slice 03).

## Learning hypothesis
- **Disproves** "the board block is enough to write Status in any repo using the plugin" if a consumer
  repo with a block still needs a probe before the write.
- **Confirms** it if the claim succeeds and reads back on this repo with no probe.

## Acceptance criteria
AC3.1–AC3.5 in `feature-delta.md`.

## Dependencies
Slice 01.

## Effort estimate
≤1 day. Reference class: `finish-work` slice 02, a board write with read-back.

## Production data
The next Todo card on this board.

## Dogfood moment
The same day, run `/phil:start` on the next Todo card: the board should show it In Progress and
assigned, and the report should say so from the read-back.
