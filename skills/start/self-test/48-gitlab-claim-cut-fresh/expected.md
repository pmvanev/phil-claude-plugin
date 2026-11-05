# Expected — START-SELFTEST-48

`NOT-LAUNCHED` · `CLAIMED` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start 58` from the main checkout. Card 58 is open, carries `status::to-do` and is unassigned, with no worktree, no open merge request and no surviving branch. The developer answers **not now** at the route.

## What must happen

- CLAIM runs one `glab issue update 58 -R https://gitlab.example.dev/team/app --label 'status::in-progress' --unlabel 'status::to-do'`, then `--assignee +pvanevery`, and reads both back from `projects/team%2Fapp/issues/58`: `CLAIMED: status::in-progress set, status::to-do removed, assigned to pvanevery — read back`.
- WORKTREE fetches `main`, cuts `issue-58-<slug>` with EnterWorktree, and compares the base with `commit.id` from `projects/team%2Fapp/repository/branches/main`: `WORKTREE-CUT`.
- The report keeps the GitHub lines and terminals; the CARD line names `status::to-do` where GitHub names a Status.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Run `gh project item-add` or any `gh` call.

## Why this fixture exists

AC5.1, and the slice's learning hypothesis: the GitHub steps translate call for call, and only the claim changes shape.
