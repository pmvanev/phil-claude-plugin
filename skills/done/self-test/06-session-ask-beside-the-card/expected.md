# Expected — DONE-SELFTEST-06

`READY` · `WROTE-NOTHING`

## Situation

The card holds two checklist items, both done with merged pull requests. Mid-session the developer asked for the report to quote asks verbatim; that request is not on the card, and a merged pull request carries it. Main's head is SUCCESS.

## What must happen

ASKS reads `3: 3 done, 0 open`. The session request appears quoted as the developer wrote it. LANDED is green. The verdict is READY.

## What must NOT happen

- Omit the session request because the card does not hold it.
- Reword the developer's request.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

AC1.2. A side request made mid-session lives in no artifact the close reads; listing it is the point of reading the session at all. This fixture also covers READY with no other line firing.
