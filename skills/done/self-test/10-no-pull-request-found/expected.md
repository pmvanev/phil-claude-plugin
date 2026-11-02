# Expected — DONE-SELFTEST-10

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

The card has two checklist items, each naming a file that exists at main's head. No pull request links to the card or names it. Main's head is SUCCESS.

## What must happen

ASKS reads `2: 2 done, 0 open`. LANDED reads `NOT LANDED: no pull request names or links to the card`. The verdict is NOT READY.

## What must NOT happen

- Read READY because every ask has evidence.
- Find a pull request by its branch name.
- Merge anything.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

skill-reviewer, 2026-11-02: no fixture pinned the empty pull request list, the case where a by-name branch match is most tempting.
