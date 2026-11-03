# Expected — START-SELFTEST-15

`LAUNCHED` · `CLAIMED` · `BUILD-PATH` · `WORKTREE-CUT`

## Situation

`/phil:start /phil:autopilot` on this repo. The search, with the argument as given, returns `issueCount` 1: card 76, in Todo and unassigned. The developer answers **start it**.

## What must happen

The run reads 76 with the number query, claims it, describes it and routes it to `nw-discuss` by CLAUDE.md's build path. It prints the outcome tokens, then invokes `nw-discuss` through the Skill tool. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Report NO-MATCH.
- Strip `/phil:autopilot` as if it were a search qualifier.
- Report outcomes after the launch.
- Remove an assignee.
- Launch the route, or begin an inline fix, before the session is in the new worktree.

## Why this fixture exists

The slice brief's dogfood moment. Run live 2026-11-03: the search reads the colon in `/phil:autopilot` as text, not as a qualifier.
