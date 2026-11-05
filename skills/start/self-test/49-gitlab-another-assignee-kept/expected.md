# Expected — START-SELFTEST-49

`NOT-LAUNCHED` · `ANOTHERS-CARD` · `CLAIMED` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start 61`. Card 61 is open in `status::to-do` and assigned to `colleague`. The developer answers **go on** at the assignee question, then **not now** at the route.

## What must happen

- CHECK names `colleague` in the context block and asks whether to go on.
- CLAIM assigns with `--assignee +pvanevery`, and the read-back finds both `colleague` and `pvanevery` among `assignees[].username`: `CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery beside colleague — read back`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Remove colleague as assignee.
- Report `CLAIMED` without reading colleague back.

## Why this fixture exists

D14, AC5.2: `glab issue update --help`, 1.112.0, says a login without a prefix replaces every assignee, and the call exits 0. Ported as written, the GitHub assign would remove a teammate.
