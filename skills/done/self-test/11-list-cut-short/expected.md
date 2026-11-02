# Expected — DONE-SELFTEST-11

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Card 7 in a busy repo: the paginated search returns three pages, and the third errors. Every hit the first two pages hold that names the card is merged, and main's head is SUCCESS.

## Writes, in order

None.

## What must happen

LANDED reads `NOT LANDED: pull request list incomplete (a search page failed)`. The verdict is NOT READY.

## What must NOT happen

- Call the work landed from the hits returned.
- Read a truncated list as complete.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

skill-reviewer, 2026-11-02: the search now pages to the end, so a long list is no longer a cause; a page that fails is, because an open pull request could sit on it.
