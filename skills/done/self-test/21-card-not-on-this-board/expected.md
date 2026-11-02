# Expected — DONE-SELFTEST-21

`CLOSED`

## Situation

Every ask is done and the work landed. The card sits on another team's project, not on the board `CLAUDE.md` names.

## The developer answers

`yes`

## Writes, in order

the closing comment, then the close

## What must happen

The report reads `CLOSED: comment posted, Status skipped (card not on this board), issue closed — read back clean`.

## What must NOT happen

- Write the Status on the other team's project.
- Report READ-BACK-MISMATCH because the card is not in Done.
- Add the card to the board.
- Merge anything.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-02: item selection ignored which project an item sat on, and a skipped Status write would have read back as a mismatch on every such card.
