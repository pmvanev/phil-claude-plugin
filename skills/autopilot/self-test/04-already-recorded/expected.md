# Expected — AUTOPILOT-SELFTEST-04

`PLANNED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 76 --plan` a second time, from the main checkout. The card is In Progress, assigned to the developer, with a worktree `issue-76-…`. Its latest autopilot comment holds the same quoted lines, in the same order, with the same `done` marks and authorized step numbers; the earlier run worded its step labels differently.

## What must happen

The claim finds every write already made: `CLAIMED`, nothing written. WORKTREE finds the card underway and enters its worktree: `UNDERWAY`, `WORKTREE-ENTERED`, with the worktree line printed without its `next: /phil:resume` clause. PATH prints the declared path: `DECLARED-PATH`. RECORD compares the quoted lines, the marks and the step numbers — not the composed labels — finds them the same, and posts nothing: `ALREADY-RECORDED`. No write call ran: `WROTE-NOTHING`.

## What must NOT happen

- Post a second path comment because the composed labels differ.
- Cut a second worktree.
- End the run at UNDERWAY, or name `/phil:resume` as the next step, without printing the path.
- Write the Status or the assignee again.
- Run or launch any step of the path.

## Why this fixture exists

A rerun on a card underway enters its worktree, prints the path, and posts nothing when the card already holds the same record.
