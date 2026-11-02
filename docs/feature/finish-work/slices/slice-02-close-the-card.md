# Slice 02 — Close the card in the safe order

**Goal (one sentence):** once the report is clean, `/phil:done` posts the closing comment, writes
Status=Done, closes the issue where the board does not, reads both back, and has the card's
generated block show a finished line.

Story 3 · Decisions D3 (the close's part of the plan), D4, D5, D6.

## IN scope
- The plan's first entries: the closing comment and the Status write, under the one yes.
- Comment first, then Done, then an explicit close where no workflow closes on Done; read state and
  Status back and report any mismatch.
- The closing comment composed to `rules/writing.md`; dropped asks quoted with their reasons.
- `phil:nwave-issue-board` learns the **finished** reasoning state and renders
  `Finished <date> — closed by /phil:done.`; `/phil:done` asks it to regenerate, never edits the block.
- Fixtures: comment before Done; read-back mismatch; a finished card with no `Stack: unknown`.

## OUT of scope
- Branches, worktrees and the snapshot (slice 03).

## Learning hypothesis
- **Disproves** "one writer can own the finished state" if rendering it needs `/phil:done` to edit
  the block itself.
- **Confirms** it if the generator renders the finished line from the closed issue alone.

## Acceptance criteria
AC1.4, AC3.1–AC3.4 in `feature-delta.md`.

## Dependencies
Slice 01.

## Effort estimate
≤1 day. Reference class: `nwave-issue-board`'s projection slice.

## Production data
A real card on this board, closed by the command.

## Dogfood moment
Close the next finished card on this board with `/phil:done`, and read the card on GitHub.
