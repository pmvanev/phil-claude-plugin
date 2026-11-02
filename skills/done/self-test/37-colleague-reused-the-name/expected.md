# Expected — DONE-SELFTEST-37

`CLOSED` · `LEFT`

## Situation

PR 91 (`finish-work/slice-02`, opened by the developer) merged into main, which is green, and every ask is done; its branch is gone. The developer's PR 86 (`spike`, head `0b6c881`) named the card and closed unmerged, and its branch was deleted. Later a colleague pushed a new `spike` at `9c2a687`, which does not descend from `0b6c881`; its one commit's author is `kim`.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

The report reads `LEFT: spike — no longer the branch of PR 86; its commits are kim's`.

## What must NOT happen

- Offer to force-delete spike.
- Show kim's commit as the developer's.
- Delete spike on any answer.
- Merge anything.

## Why this fixture exists

Adversarial run, 2026-11-02, verified in a scratch repo: a branch reusing the name of the developer's closed pull request was offered, its commits shown with no author, and the leased delete went through.
