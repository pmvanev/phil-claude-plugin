# Expected — START-SELFTEST-56

`STOPPED` · `OPEN-IN-DONE` · `WROTE-NOTHING`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::done`. `user` answers `pvanevery`. `/phil:start 33`. Card 33's `state` reads `opened`, and it carries `status::done`. The developer answers **stop**.

## What must happen

- CHECK states the defect, an open card carrying the done label, and asks whether to go on, saying going on swaps it for `status::in-progress`.
- On stop it ends with nothing written.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Close or reopen the card.
- Write a status label or assign anyone.

## Why this fixture exists

AC5.4's third clause, which skill-reviewer found unpinned on 2026-11-05: an open card with a done label reads two ways, as an open card in Done does on GitHub.
