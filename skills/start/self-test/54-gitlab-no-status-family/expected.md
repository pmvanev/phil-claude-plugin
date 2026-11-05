# Expected — START-SELFTEST-54

`NOT-LAUNCHED` · `NO-BOARD-BLOCK` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`, and the block names no status family. `user` answers `pvanevery`. `/phil:start 70`. Card 70 is open, carries only `bug`, and is unassigned. The developer answers **not now** at the route.

## What must happen

- CLAIM writes no label, names `/phil:board-setup`, still assigns with `--assignee +pvanevery` and reads it back: `NO BOARD BLOCK: no status family — run /phil:board-setup; assigned to pvanevery — read back`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Add or remove any label.
- Guess a status family from the project's labels.

## Why this fixture exists

D13, AC5.6: the board block, not a probe, supplies the status labels, as it supplies the Status ids on GitHub.
