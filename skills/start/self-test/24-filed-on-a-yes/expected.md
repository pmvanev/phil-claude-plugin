# Expected — START-SELFTEST-24

`NOT-LAUNCHED` · `FILED` · `CLAIMED` · `NO-DONE-WHEN` · `WORKTREE-CUT`

## Situation

`/phil:start retry flaky uploads`. The search returns `issueCount` 0. The developer answers **file it**, then **not now** at the route.

## What must happen

The run files `retry flaky uploads` with `gh issue create`, its title as typed and its body empty. CLAIM's first step adds it to the board in the same breath; the claim then writes Status, assigns the developer and reads both back. DESCRIBE reports `NO-DONE-WHEN` and names `/phil:groom-ask`. After CLAIM and before DESCRIBE, WORKTREE fetches the default branch, cuts `issue-<n>-<slug>` with EnterWorktree, moves the session in, and names its path, branch and base commit: `WORKTREE-CUT`.

## What must NOT happen

- Compose a body or a done-when for the card.
- Reword the developer's title.
- File the card without adding it to the board.
- Remove an assignee.

## Why this fixture exists

AC3.5: a card filed on a yes is claimed, and carries only the developer's words.
