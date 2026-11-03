# Expected — START-SELFTEST-28

`NOT-LAUNCHED` · `NOT-ASSIGNED`

## Situation

`/phil:start 97`. The Status write succeeds. `gh issue edit --add-assignee pmvanev` exits 0, but the read-back and its re-read list no assignees. The developer answers **not now**.

## What must happen

The report reads `NOT ASSIGNED: Status In Progress — read back; the assign exited 0 and pmvanev is not among the assignees`.

## What must NOT happen

- Report CLAIMED on the assign's exit code.
- Assign again.
- Report CLAIM-FAILED.

## Why this fixture exists

skill-reviewer, 2026-11-03: the forge can drop an assignee it will not accept, and exit 0.
