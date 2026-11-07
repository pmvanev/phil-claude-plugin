# Expected — BSNAP-SELFTEST-15

`SNAPSHOT-RENDERED` · `UNCOLUMNED` · `READ-ONLY`

## Situation

A GitLab Premium project whose `CLAUDE.md` board block names the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no done label. Two cards carry `status::blocked`, one `status::in-progress`, six `status::to-do`, and three open issues carry no status label, so they sit in the board's Open list. Four closed issues still carry a status label.

## What must happen

The standing check renders from GitLab's label columns. **Blocked** lists the two `status::blocked`
cards with their `## Chain` reasons, **in flight** the one `status::in-progress` card, and **queued** the
first five `status::to-do` cards in board order, saying the order is the board's own. One line names the
three uncolumned cards in the Open list. `READ-ONLY` closes the report.

## What must NOT happen

- Refuse the board, or say GitLab is unsupported.
- Report any open issue as off the board, or make a reconciliation call: every open issue is on a GitLab board.
- Report drift for the four closed issues: with no done label, the Closed list is Done whatever labels a closed issue carries.
- Sort a column by number, date or any field in place of the board's relative_position order.
- Send `glab api` anything but a GET, or edit a label.

## Why this fixture exists

Card 76's checklist, 2026-11-06: board-snapshot stopped on GitLab although every surface that drives a board supports both forges. The counts are modive's board on that day.
