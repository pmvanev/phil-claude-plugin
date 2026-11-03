# Expected — START-SELFTEST-29

`NOT-LAUNCHED` · `READ-BACK-MISMATCH` · `WORKTREE-CUT`

## Situation

`/phil:start 98`. The Status write and the assign both exit 0. The read-back fails: `HTTP 502`, and so does its re-read. The developer answers **not now**.

## What must happen

The report says the claim is unverified, quoting the error: `READ-BACK MISMATCH: …`. It goes on to describe and route the card. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Report CLAIMED on the writes' exit codes.
- Report CANNOT-RUN after a write.
- Write the Status again.

## Why this fixture exists

skill-reviewer, 2026-11-03: a read that failed after the first write had no outcome.
