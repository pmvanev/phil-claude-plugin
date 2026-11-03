# Expected — START-SELFTEST-35

`STOPPED` · `WROTE-NOTHING`

## Situation

`/phil:start 95` from a session inside `.claude/worktrees/done-gitlab-no-card`, which is not card 95's. The developer answers **stop**.

## What must happen

CHECK names where the session is and asks whether to move it. On stop it ends, before the claim.

## What must NOT happen

- Move the session without a yes.
- Exit the current worktree.
- Write a Status or assign anyone.

## Why this fixture exists

AC4.4: a session already in another worktree is moved only on a yes.
