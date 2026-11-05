# Expected — START-SELFTEST-59

`STOPPED` · `WROTE-NOTHING`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::doing`. `user` answers `pvanevery`. `/phil:start 66`. Card 66 is open in `status::to-do` and unassigned. Two labels match In Progress. The developer gives no answer at the label question.

## What must happen

- Before any write, the run lists the family and asks which label is In Progress.
- With no answer it ends `STOPPED`, with nothing written.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Choose the first matching label.
- Write a status label or assign anyone.

## Why this fixture exists

D12, AC5.3's second clause: several matching labels are the developer's pick, and no answer writes nothing.
