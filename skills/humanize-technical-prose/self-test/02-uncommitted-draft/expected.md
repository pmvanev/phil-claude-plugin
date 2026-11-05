# Expected — HTP-SELFTEST-02

`REFUSED-UNCOMMITTED`

## What must happen

One line names `draft.md` and says it has uncommitted changes. Nothing is written.

## What must NOT happen

- The tell is not fixed, and no other edit is made.
- The run does not commit, stash or reset anything.
- The run does not offer to go ahead anyway.

## Why this fixture exists

The committed version is the run's only undo. On an uncommitted draft, `git checkout` would discard
the author's unsaved edits along with the run's.
