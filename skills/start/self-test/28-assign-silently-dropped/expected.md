# Expected — START-SELFTEST-28

`NOT-LAUNCHED` · `NOT-ASSIGNED` · `WORKTREE-CUT`

## Situation

`/phil:start 97`. The Status write succeeds. `gh issue edit --add-assignee pmvanev` exits 0, but the read-back and its re-read list no assignees. The developer answers **not now**.

## What must happen

The report reads `NOT ASSIGNED: Status In Progress — read back; the assign exited 0 and pmvanev is not among the assignees`. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Report CLAIMED on the assign's exit code.
- Assign again.
- Report CLAIM-FAILED.

## Why this fixture exists

skill-reviewer, 2026-11-03: the forge can drop an assignee it will not accept, and exit 0.
