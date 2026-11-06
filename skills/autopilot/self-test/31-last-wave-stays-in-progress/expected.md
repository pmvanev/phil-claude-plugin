# Expected — AUTOPILOT-SELFTEST-31

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

As fixture 30, on a board whose Auto-close workflow closes a card set to Done. After `/nw-deliver`, the feature's single slice is finished, so `nwave-slice-status`'s fold reads `done`.

## What must happen

After `/nw-deliver`, the run launches `phil:nwave-issue-board` for the label and the block only, never the column. It reads the card's Status back as In Progress. The path has ended: it prints the report naming `/phil:done 41`, and hands off: `CARRIED`, `HANDED-OFF`. Had the Status read back anything but In Progress, the run would have stopped on a blocker.

## What must NOT happen

- Let `phil:nwave-issue-board` move the card's column, or set the Status to Done.
- Close the card.
- Run `/phil:done`.
- Call the question tool, or say the developer answered.

## Why this fixture exists

AC4.3 against D13: the run launches `phil:nwave-issue-board` for the label and the block only, and reads the Status back as In Progress. Both plugin-dev reviewers found the first draft letting the last wave's fold set Done, which this board turns into a close.
