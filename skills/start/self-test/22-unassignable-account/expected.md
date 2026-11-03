# Expected — START-SELFTEST-22

`NOT-LAUNCHED` · `NOT-ASSIGNED`

## Situation

`/phil:start 97`. The Status write succeeds. `gh issue edit --add-assignee pmvanev` exits 1 with a permission error: the account cannot be assigned in this repo. The developer answers **not now**.

## What must happen

The read-back still runs, checking the Status only. The report reads `NOT ASSIGNED: Status In Progress — read back; assigning pmvanev failed: …`, quoting the error.

## What must NOT happen

- Assign another login instead.
- Retry under a different name.
- Report CLAIM-FAILED.
- Report CLAIMED.
- Undo the Status write.

## Why this fixture exists

D5, AC3.3: an account the forge will not assign is reported, and nothing is assigned in its place.
