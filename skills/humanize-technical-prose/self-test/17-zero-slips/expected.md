# Expected — HTP-SELFTEST-17

`WROTE`

## What must happen

The tells and voice passes run as in fixture 11. The document holds no new slip, and the report has
no slips section.

## What must NOT happen

- No slip is added.
- Neither `SLIPS-WARNING` nor `SLIPS-UNMIRRORED` is printed.
- The allocation script is not called.

## Why this fixture exists

A count of zero adds none. Zero is the default that keeps the command safe to run on anything.
