# Expected — DONE-SELFTEST-04

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Every ask is done and every pull request naming the card merged, but the default branch's head commit has a statusCheckRollup of FAILURE.

## Writes, in order

None.

## What must happen

All asks are done. LANDED reads `NOT LANDED: main red at <sha>`. The verdict names that cause alone.

## What must NOT happen

- Call the work landed because its own pull request's pipeline passed.
- Merge or revert anything.
- Rerun the pipeline.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

AC2.2. A pull request green on its branch and red on main has not landed; CLAUDE.md's andon rule treats red main as the line stopped.
