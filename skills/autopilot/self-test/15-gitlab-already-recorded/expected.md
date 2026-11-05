# Expected — AUTOPILOT-SELFTEST-15

`PLANNED` · `CLAIMED` · `UNDERWAY` · `DECLARED-PATH` · `ALREADY-RECORDED` · `WROTE-NOTHING`

## Situation

`/phil:autopilot 58` a second time in modive, from the card's worktree. The card carries `status::in-progress` and is assigned to the developer. Its newest notes are GitLab's own system notes for the label swap and the assignment; beneath them sits the developer's note starting `**Autopilot · build path**`, holding the same quoted line, mark and authorized step number this run reads, with differently worded labels.

## What must happen

The claim finds every write made: `CLAIMED`. WORKTREE finds the session already in the card's worktree: `UNDERWAY`, with no `next:` clause. PATH prints the declared path: `DECLARED-PATH`. RECORD reads the notes newest first, skips the system notes, takes the developer's autopilot note as the latest, compares the quoted line, the mark and the step number, and posts nothing: `ALREADY-RECORDED`, `WROTE-NOTHING`.

## What must NOT happen

- Treat a system note as the latest autopilot note.
- Post a second note because the composed labels differ.
- Judge the notes read by `jq`'s exit code alone.
- Write a status label or an assignee.
- Run or launch any step of the path.

## Why this fixture exists

The GitLab comparison path — newest first, system notes skipped, the first matching note the latest — had no fixture; fixture 04 pins it on GitHub only.
