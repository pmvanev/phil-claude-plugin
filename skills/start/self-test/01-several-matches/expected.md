# Expected — START-SELFTEST-01

`NOT-LAUNCHED` · `PICKED` · `CLAIMED` · `BUILD-PATH` · `WORKTREE-CUT`

## Situation

`/phil:start worktree` on this repo. Three open cards match: 89 (the handoff snapshot lands in the shell's worktree), 80 (`/phil:start`) and 76 (`/phil:autopilot`). The developer picks the `/phil:autopilot` card: open, in Todo, unassigned, labelled `enhancement` only, and linking no `docs/feature/` directory. The developer answers **not now** at the route.

## What must happen

The report lists all three by number and title above one question and waits. After the pick it runs CHECK on 76, claims it, describes it, and routes it to `nw-discuss`, quoting CLAUDE.md's build path. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Pick the closest match itself.
- Claim, describe or route any card before the developer picks.
- Drop a match from the list.
- Remove an assignee.

## Why this fixture exists

AC1.1, and issue 80's first fixture behaviour: an ambiguous argument lists candidates instead of picking one.
