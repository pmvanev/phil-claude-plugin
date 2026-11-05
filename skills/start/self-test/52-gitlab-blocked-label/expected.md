# Expected — START-SELFTEST-52

`STOPPED` · `WROTE-NOTHING`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start 44`. Card 44 is open and carries `status::blocked`. The developer answers **stop**.

## What must happen

- CHECK names the blocked label and asks whether to go on, saying going on moves the card out of Blocked.
- On stop it ends with nothing written.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Swap `status::blocked` without asking.
- Write a status label or assign anyone.

## Why this fixture exists

D15, AC5.4: a label that reads blocked asks, as Blocked does on GitHub; moving the card hides the blocker.
