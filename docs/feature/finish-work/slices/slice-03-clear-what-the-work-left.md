# Slice 03 — Clear what the work left behind

**Goal (one sentence):** `/phil:done` clears the work's snapshot, worktrees and branches in the one
approved plan, holding back anything unmerged or uncommitted for its own answer.

Story 4 · Decisions D3, D7, D8, D9.

## IN scope
- Candidates per D8: pull requests the forge links to the card, or merged pull requests whose title or
  body names it; the worktrees on their branches. Never a branch by name alone.
- For each checkout, the snapshot's next action and stack, read through `session-exchanges.py head`;
  its deletion listed before its worktree's removal.
- The full plan: comment, Status, snapshots, worktrees, branches local and remote — one yes, with
  `stop`.
- Held out, each with its own question: an unmerged branch; a worktree with uncommitted or unpushed
  changes.
- `git branch -d`, `git worktree remove` without `--force`; git's refusals reported, items left.
- The report: what it did, what it left, and why.
- Fixtures: snapshot before worktree; unmerged branch survives; dirty worktree survives; a
  name-only branch is no candidate; a clean finish asks one question.

## OUT of scope
- GitLab; retiring a snapshot on resume.

## Learning hypothesis
- **Disproves** "one yes is enough" if, on a real finish, the developer wants to edit the plan rather
  than approve or stop it.
- **Confirms** it if two real finishes go through on the one yes.

## Acceptance criteria
AC4.1–AC4.6 in `feature-delta.md`.

## Dependencies
Slice 02.

## Effort estimate
≤1 day. Reference class: `session-handoff` slice 02.

## Production data
This feature's own branches and worktree, cleared when issue 75 closes.

## Dogfood moment
`/phil:done 75` closes this card and clears `finish-work/*`.
