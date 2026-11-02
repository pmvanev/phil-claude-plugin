# Expected — DONE-SELFTEST-22

`CLOSED`

## Situation

The card was closed by hand last week, with no closing comment, and sits in Done. Every ask is done and the work landed.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done

## What must happen

The comment posts with `gh issue comment` on the closed issue. The state read finds it closed and the close is skipped. The read-back finds it closed, in Done, holding the comment's URL.

## What must NOT happen

- Run `gh issue close -c`, which drops the comment on a closed issue.
- Reopen the issue.
- Skip the comment because the issue is closed.
- Merge anything.

## Why this fixture exists

skill-reviewer, 2026-11-02: no fixture covered a card closed before the run, the case where `gh issue close -c` loses the comment silently.
