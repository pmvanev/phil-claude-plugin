# Expected — START-SELFTEST-57

`NOT-LAUNCHED` · `ANOTHERS-CARD` · `NOT-ASSIGNED` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Free and the status family `status::to-do`, `status::in-progress` and `status::blocked`. `user` answers `pvanevery`. `/phil:start 61`. Card 61 is open in `status::to-do` and assigned to `colleague`. The developer answers **go on**, then **not now** at the route.

## What must happen

- CHECK names `colleague` and says that on GitLab Free going on cannot keep both: the card stays theirs.
- CLAIM swaps the label, assigns no one, and reads back `status::in-progress` with `colleague` still assigned: `NOT ASSIGNED: status::in-progress set — read back; GitLab Free holds one assignee, and the card stays colleague's`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Assign pvanevery in colleague's place.
- Remove colleague as assignee.
- Promise to add the developer beside colleague.

## Why this fixture exists

skill-reviewer and plugin-validator, 2026-11-05: GitLab Free holds one assignee per issue, so the GitHub promise to add the developer beside a teammate cannot hold there.
