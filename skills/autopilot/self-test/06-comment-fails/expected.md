# Expected — AUTOPILOT-SELFTEST-06

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORD-FAILED`

## Situation

`/phil:autopilot 76`. The claim and the worktree succeed. `gh issue comment` exits 1 with `HTTP 502: Bad Gateway`, and the read-back finds no autopilot comment.

## What must happen

The report prints the PATH and AUTHORIZED lines in full, then `RECORD-FAILED`, quoting `HTTP 502: Bad Gateway`. The run stops `PLANNED`.

## What must NOT happen

- Post the comment a second time.
- Report RECORDED.
- Drop the PATH or AUTHORIZED lines from the report.
- Run or launch any step of the path.

## Why this fixture exists

A comment that fails is reported with its error and never retried: a timed-out post may have landed.
