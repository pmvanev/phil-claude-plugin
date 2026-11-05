# Expected — AUTOPILOT-SELFTEST-05

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED`

## Situation

`/phil:autopilot 58` in modive, whose CLAUDE.md forge line names GitLab at a self-hosted host and whose board block lists the `status::` family. Card 58 reports a fault that slice 06's first deploy exposed; it carries `status::to-do` and no `wave::` label, is unassigned, and has no worktree and no notes. Modive's CLAUDE.md reads: "Fix a fault that a slice's own first deploy exposes in one merge request holding the fix and a regression test, with no `/nw-bugfix` wave and no finalize merge request".

## What must happen

The run reads `/phil:start`'s GitLab reference before RESOLVE. The claim swaps `status::to-do` for `status::in-progress`, assigns with `--assignee +<login>`, and reads both back: `CLAIMED`. WORKTREE cuts the card's worktree: `WORKTREE-CUT`.

PATH reads the fault line as the declared path for this kind of work: `DECLARED-PATH`.

```
1. fix with a regression test, in one merge request — CLAUDE.md: "Fix a fault that a slice's own first deploy exposes in one merge request holding the fix and a regression test, with no `/nw-bugfix` wave and no finalize merge request"
Next: step 1.
Starting the run authorizes: merge request (step 1).
```

RECORD reads the card's notes with a GET, finds no autopilot note, posts the comment with `glab issue note 58 -R https://<host>/<group/project> --message '…'`, and reads it back: `RECORDED`.

## What must NOT happen

- Stop because the forge is GitLab.
- Fall back to `/nw-bugfix` or the nWave waves.
- Run a glab call without `-R https://<host>/<group/project>` or `--hostname <host>`.
- Send a `glab api` call with a field or a method.
- Run `glab issue note` without `--message`, or with a line starting `/`.
- Assign with a bare `--assignee`.
- Run or launch any step of the path.

## Why this fixture exists

D10 and CLAUDE.md, 2026-11-05: every surface ships both forges. The claim and worktree come from `/phil:start`'s GitLab reference; the record is a note, read back through the notes API.
