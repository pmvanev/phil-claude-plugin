# Expected — HTP-SELFTEST-16

`WROTE` · `SLIPS-UNMIRRORED` · `SLIPS-WARNING`

## What must happen

- The voice pass runs as in fixture 11.
- `--allocate formal 2` returns one *number agreement* and one *dropped article*, and exactly those
  two are added, in two different sentences of ordinary prose.
- The report's `SLIPS 2:` line names each slip's line and kind.
- `SLIPS-UNMIRRORED` says the samples put 1 of 29 slips on a technical term, and none was placed
  there.
- `SLIPS-WARNING` says a later cleanup pass will fix the slips, so this command runs last.

## What must NOT happen

- No third slip and no misspelling.
- No slip lands on a technical term, or on *must*, *never*, *forever* or any word the claim rests on.
- The two slips are not in the same sentence.
- No slip goes unreported.

## Why this fixture exists

It is the slice's happy path. The count is exact, the kinds come only from the profile, and the
report leads the author to every slip.
