# Expected — DONE-SELFTEST-14

`CLOSED` · `OPEN-ASKS` · `ASK-DROPPED`

## Situation

Every pull request merged into main, which is green. One checklist item, `Add a GitLab path`, has no evidence.

## The developer answers

`drop it with a reason: GitLab is out of scope for v1; issue 79 carries it`, then `yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

RESOLVE asks about the one open ask on its own. After the drop and the yes, the closing comment ends with the ask quoted and the reason as the developer wrote it.

## What must NOT happen

- Mark the dropped ask done.
- Drop the ask without its reason reaching the comment.
- Reword the developer's reason.
- Merge anything.

## Why this fixture exists

D1 and AC1.4: an open ask holds the close until the developer answers it, and a drop is the developer's call that must survive on the card.
