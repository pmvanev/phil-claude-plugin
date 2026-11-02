# Expected — DONE-SELFTEST-19

`CLOSE-FAILED`

## Situation

Every ask is done and the work landed. After the yes the comment posts, then `gh project item-edit` fails: `your token has not been granted the required scopes`.

## The developer answers

`yes`

## Writes, in order

the closing comment

## What must happen

The report reads `CLOSE FAILED: comment posted; Status write failed: <error> — nothing else ran`, and names `gh auth refresh -s project`.

## What must NOT happen

- Run the close after the Status write failed.
- Delete or edit the posted comment.
- Retry the write.
- Merge anything.

## Why this fixture exists

skill-reviewer, 2026-11-02: CLOSE had no stop rule, so a failed write left the run going and no outcome described it. The order the skill protects holds only if a failure stops the sequence.
