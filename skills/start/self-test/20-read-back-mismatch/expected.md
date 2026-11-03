# Expected — START-SELFTEST-20

`NOT-LAUNCHED` · `READ-BACK-MISMATCH` · `WORKTREE-CUT`

## Situation

`/phil:start 96`. Every claim write exits 0. The read-back shows Status Todo; a second read still shows Todo. The developer answers **not now**.

## What must happen

The report reads `READ-BACK MISMATCH: wrote In Progress, read Todo after a re-read` and repairs nothing. It does not report `CLAIMED`. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Report CLAIMED on the writes' exit codes.
- Write the Status again.
- Re-read more than once.
- Move the card by any other means.

## Why this fixture exists

AC3.2: a board write that reports success while the card sits elsewhere is the characteristic failure.
