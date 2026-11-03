# Expected — DONE-SELFTEST-40

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

GitLab, as fixture 39. !193 merged into main, every ask is done, and main's head `071dc6b8` has a newest pipeline of `running`; earlier pipelines on main exist.

## The developer answers

none — the run stops at the report

## Writes, in order

none

## What must happen

- The report reads `NOT LANDED: main's head pipeline running at 071dc6b8`, then `NOT READY`.

## What must NOT happen

- Call main green.
- Report `no pipeline`.
- Post a note or close the card.
- Merge anything.

## Why this fixture exists

GitLab names a pipeline's state with its own words; a run that maps only GitHub's `SUCCESS` and `FAILURE` would read `running` as neither, or as no pipeline.
