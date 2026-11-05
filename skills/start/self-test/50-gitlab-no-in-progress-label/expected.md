# Expected — START-SELFTEST-50

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::todo`, `status::wip` and `status::review`. `user` answers `pvanevery`. `/phil:start 63`. Card 63 is open in `status::todo` and unassigned. No label reads `in-progress`, `in progress` or `doing`. At the label question the developer picks `status::wip`, then answers **not now** at the route.

## What must happen

- Before the first claim write, the run lists the family in the context block and asks which label is In Progress.
- Only after the answer, CLAIM swaps `status::todo` for `status::wip` in one call, assigns with `+pvanevery`, and reads both back: `CLAIMED`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Write a status label before the developer answers.
- Choose `status::wip` from what its name suggests.
- Record the answer anywhere.

## Why this fixture exists

D12, AC5.3, the developer's answer: match the label by name, and ask when none or several match. A guessed column is a card in the wrong place, reported as a success.
