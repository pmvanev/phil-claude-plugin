# Expected — START-SELFTEST-07

`LAUNCHED` · `CLAIMED` · `BUILD-PATH` · `WORKTREE-CUT`

## Situation

`/phil:start 76`. The card asks for a new command, `/phil:autopilot`, carries no `wave:` label, and sits in Todo, unassigned. A user would see the change, so rule 3 alone would pick `phil:edd`. This repo's CLAUDE.md reads `Run nw-discuss before authoring a new feature, skill or command`. The developer answers **start it**.

## What must happen

CLAIM writes Status In Progress and assigns the developer, adding the card to the board where it is missing, and reads both back: `CLAIMED`. ROUTE reads `nw-discuss`, quoting the CLAUDE.md rule and naming the file. On the yes, the run prints its outcome tokens, then invokes `nw-discuss` through the Skill tool. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Recommend phil:edd.
- Name the route without citing the rule.
- Launch before the yes.
- Remove an assignee.
- Launch the route, or begin an inline fix, before the session is in the new worktree.

## Why this fixture exists

AC2.2. The repo's recorded build path comes before any default; this is the dogfood card the slice brief names.
