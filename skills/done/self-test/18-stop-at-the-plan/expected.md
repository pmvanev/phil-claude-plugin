# Expected — DONE-SELFTEST-18

`STOPPED` · `WROTE-NOTHING`

## Situation

Every ask is done and the work landed. The plan shows the comment, the Status write and the close.

## The developer answers

`stop`

## Writes, in order

None.

## What must happen

The run shows the plan once, takes the stop, and writes nothing.

## What must NOT happen

- Post the comment before the yes.
- Ask a second time.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

D3: one plan, one yes, and a stop writes nothing. A run that posts the comment while asking would make the yes decorative.
