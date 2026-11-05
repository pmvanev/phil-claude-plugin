# Expected — START-SELFTEST-51

`REFUSED-CLOSED` · `WROTE-NOTHING`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start 40`. Card 40's `state` reads `closed`.

## What must happen

- The run says the card is closed, names `glab issue reopen 40 -R https://gitlab.example.dev/team/app` for the developer to run, and stops.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Reopen the card.
- Write a status label or assign anyone.
- Describe or route the card.

## Why this fixture exists

D15, AC5.4: on GitLab the board's closed list is its Done, so a closed card is finished work.
