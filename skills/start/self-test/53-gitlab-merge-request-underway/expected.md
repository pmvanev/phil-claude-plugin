# Expected — START-SELFTEST-53

`UNDERWAY` · `CLAIMED` · `WROTE-NOTHING`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start 58`. Card 58 already carries `status::in-progress` and is assigned to `pvanevery`. The developer's open merge request !12, on `worktree-issue-58-show-who-owns-an-item`, says `issue 58` in its description. No worktree here holds that branch.

## What must happen

- The merge-request read uses `projects/team%2Fapp/merge_requests?state=opened&author_username=pvanevery` with `--paginate`, and keeps !12 by the card pattern.
- CLAIM finds every write made: `CLAIMED: already status::in-progress and assigned to pvanevery — nothing written`.
- The worktree line reads `UNDERWAY: !12 is open on worktree-issue-58-show-who-owns-an-item, with no worktree here — nothing cut; next: /phil:resume`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Cut a worktree.
- Recommend a route.
- Count the merge requests with `length` over a paginated read.

## Why this fixture exists

D18, AC5.5: an open merge request means the work is underway, and a fresh worktree would start it again from the default branch.
