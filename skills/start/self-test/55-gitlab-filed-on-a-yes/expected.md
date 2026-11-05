# Expected — START-SELFTEST-55

`NOT-LAUNCHED` · `FILED` · `CLAIMED` · `NO-DONE-WHEN` · `WORKTREE-CUT`

## Situation

The forge line reads `GitLab at gitlab.example.dev — use glab -R team/app`; the board block names Premium and the status family `status::to-do`, `status::in-progress` and `status::blocked`, with no Done label. `user` answers `pvanevery`. `/phil:start retry flaky uploads`. The search `projects/team%2Fapp/issues?state=opened&search=retry%20flaky%20uploads&in=title,description&per_page=21` returns no entries. The developer says **yes** to filing, then **not now** at the route. `glab issue create` prints `https://gitlab.example.dev/team/app/-/issues/72`.

## What must happen

- The run files with `glab issue create -R https://gitlab.example.dev/team/app --title 'retry flaky uploads' --description '' --yes`: `FILED`.
- CLAIM adds `status::in-progress` with no `--unlabel`, since the new card carries no status label, assigns with `+pvanevery`, and reads both back: `CLAIMED`.
- The empty body yields `DONE WHEN: the card does not say`: `NO-DONE-WHEN`.

## What must NOT happen

- Stop because the forge is GitLab.
- Pass a bare `-R team/app`, which outside a checkout of the host reaches gitlab.com.
- Pass a field, `--input`, `-X` or `--method` to `glab api`.
- Pass a bare `--assignee` login, which replaces every assignee.
- Create a board list.
- Pass a label, an assignee, a milestone, a template or `--web` to `glab issue create`.
- File before the yes.
- Run any `item-add`.

## Why this fixture exists

D19, AC5.7. Settled 2026-11-05 with `glab` 1.112.0 outside a terminal: `--description ''` gets past the non-interactive check and opens no editor.
