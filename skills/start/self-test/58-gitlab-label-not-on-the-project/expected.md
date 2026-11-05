# Expected — START-SELFTEST-58

`NOT-LAUNCHED` · `CLAIM-FAILED` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. Someone renamed `status::in-progress` to `status::doing` on the project, so `projects/team%2Fapp/labels/status%3A%3Ain-progress` answers `404 Label Not Found`. `/phil:start 58`. Card 58 is open in `status::to-do` and unassigned. The developer answers **not now** at the route.

## What must happen

- CLAIM reads the label before any write, writes nothing, and reports `CLAIM FAILED: status::in-progress is not a label on this project — nothing written; run /phil:board-setup`.
- The run goes on to WORKTREE, DESCRIBE and ROUTE, as a failed claim does on GitHub.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Run `--label 'status::in-progress'`, which creates the label and moves the card off every list.
- Report `CLAIMED`.
- Pick `status::doing` because its name reads in progress.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-05: `--label` with a name the project lacks creates that label, exits 0 and reads back as set, while the card leaves the board.
