# Expected — DONE-SELFTEST-15

`CLOSED`

## Situation

Every ask is done and the work landed. The board's `Auto-close issue` workflow closes a card when its Status becomes Done, and it has closed this one by the time the run reads the state.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done

## What must happen

The run posts the comment, writes Done, reads the state, finds it closed, skips the close, and reports the read-back clean.

## What must NOT happen

- Write Status before the comment is posted.
- Run `gh issue close -c`.
- Close the issue without first reading its state.
- Merge anything.

## Why this fixture exists

D5 and AC3.1: on this board Done closes the issue, and `gh issue close -c` on a closed issue drops the comment silently, so the order is the rule.
