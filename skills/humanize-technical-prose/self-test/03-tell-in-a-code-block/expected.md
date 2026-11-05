# Expected — HTP-SELFTEST-03

`WROTE`

## What must happen

The prose sentence loses its tell. The request id *is how a failed call is traced*, or a rewording
like it that adds nothing. The report gives `TELLS: 1 found, 1 rewritten; re-check: 0 left`.

## What must NOT happen

- The fenced block, its comment included, does not change by a byte.
- The occurrence inside the block is neither counted as found nor reported as left.
- `X-Request-Id` and the function names stay as written.

## Why this fixture exists

A search-and-replace editor rewrites both occurrences. The comment is code, and it may need to match
a file the draft was copied from.
