# Slice 03 — Land in the worktree

**Goal (one sentence):** `/phil:start <card>` moves the session into a worktree cut from the freshly
fetched default branch, or into the card's existing one, and hands a card already underway to
`/phil:resume`.

Story 4 · Decisions D1, D2, D3.

## IN scope
- A new worktree through Claude Code's worktree tool, named `issue-<n>-<slug>`, after a fetch; the
  report names its path, branch and base commit.
- The card's existing worktree, found by its name or by the head branch of the developer's open pull
  request naming the card; several listed for the developer to pick.
- A card underway — a worktree, an open pull request, or a snapshot — handed to `/phil:resume`, with
  no other route recommended.
- A session already in another worktree reported, and moved only on a yes.
- Settle first: whether a command's `allowed-tools` can grant the worktree tool, and whether that tool
  fetches before it branches. Record the answer in `feature-delta.md`.
- Fixtures: a card with no worktree; a card with one; two candidate worktrees; a snapshot in the
  card's worktree; a session already in another worktree.

## OUT of scope
- Removing a worktree. `/phil:done` lists worktrees and never removes one. (Since `/phil:done` 1.25.0,
  2026-11-03, it removes a worktree its own session made once it reads clean; removal stays its call.)

## Learning hypothesis
- **Disproves** "a command can drive Claude Code's worktree tool" if the tool cannot be granted to a
  command, or refuses a call the developer did not type.
- **Confirms** it if `/phil:start` moves this session into a new worktree on this repo.

## Acceptance criteria
AC4.1–AC4.4 in `feature-delta.md`, and Definition of Done item 9: `/phil:done` lists the worktree by
its branch.

## Dependencies
Slice 02.

## Effort estimate
≤1 day. Reference class: `finish-work` slice 03, which met git's worktree edge cases.

## Production data
The next Todo card on this board, started from the main checkout.

## Dogfood moment
The same day, run `/phil:start` on the next Todo card from the main checkout, then again: the second
run should enter the same worktree and name `/phil:resume`.
