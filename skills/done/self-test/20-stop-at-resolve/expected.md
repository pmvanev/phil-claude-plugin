# Expected — DONE-SELFTEST-20

`STOPPED` · `OPEN-ASKS` · `WROTE-NOTHING`

## Situation

The work landed. One checklist item, `Document the GitLab path`, has no evidence.

## The developer answers

`stop`

## Writes, in order

None.

## What must happen

The question describes the open ask in plain words; the quote sits in the context block above it. The stop ends the run: `STOPPED`, with `OPEN-ASKS`.

## What must NOT happen

- Show the plan after the stop.
- Report NOT-READY instead of STOPPED.
- Put the quoted ask, a path or an issue number in the question itself.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

skill-reviewer, 2026-11-02: a stop at RESOLVE matched both NOT-READY and STOPPED, and a quoted ask in the question collides with a strict repo's decision-request hook.
