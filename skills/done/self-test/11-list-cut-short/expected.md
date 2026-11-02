# Expected — DONE-SELFTEST-11

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Card 7 in a busy repo: the search for `7` returns an issueCount of 312, so the first 50 hits cannot be the whole list. Every hit that names the card is merged, and main's head is SUCCESS.

## What must happen

LANDED reads `NOT LANDED: pull request list incomplete (312 search hits)`. The verdict is NOT READY.

## What must NOT happen

- Call the work landed from the hits returned.
- Read a truncated list as complete.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

skill-reviewer, 2026-11-02: the query read a fixed window and never checked for more, so an open pull request past hit 50 would read as landed.
