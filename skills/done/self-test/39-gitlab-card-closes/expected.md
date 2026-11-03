# Expected — DONE-SELFTEST-39

`CLOSED` · `CLEARED`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`. Card 21 carries `status::in-progress` and `wave::deliver`. !193 (`finalize-21`, `sha` `42b67c71`, the developer's, same project) merged into main and names the card; main's head `071dc6b8` has a newest pipeline of `success`. Every ask is done. GitLab deleted the source branch on merge, so the branch read answers 404; the local branch sits at `42b67c71` with no worktree.

## The developer answers

`yes`

## Writes, in order

the closing note, then remove the status label status::in-progress, then the close, then delete the local branch

## What must happen

- The report reads `LANDED: !193 merged into main; main green at 071dc6b8`.
- The note posts first, then `glab issue update 21 -R https://gitlab.example.dev/team/app --unlabel 'status::in-progress'`, then `glab issue close 21 -R https://gitlab.example.dev/team/app`.
- The read-back finds the card closed, with the note and no `status::` label: `CLOSED: note posted, status::in-progress removed, issue closed — read back clean`.
- `CLEARED: 1 branch (local)`; the remote copy is skipped because the merge deleted it.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Use `:id` or `:fullpath` in a `glab api` path.
- Add a label or create a board list.
- Remove `wave::deliver`.
- Merge anything.

## Why this fixture exists

Dogfood, `/phil:done 21` on modive (GitLab, 2026-11-03): the skill refused at its forge check, and the developer closed the card and cleared its branches by hand.
