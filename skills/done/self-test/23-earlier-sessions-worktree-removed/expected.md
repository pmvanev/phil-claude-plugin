# Expected — DONE-SELFTEST-23

`CLOSED` · `CLEARED`

## Situation

PR 91 (`finish-work/slice-02`, head `a1b2c3d`, opened by the developer) merged into main, which is green, and every ask is done. The branch sits at `a1b2c3d` locally and on the remote. A worktree at `../fw-02`, which an earlier session made, has it checked out at `a1b2c3d`, reads `CLEAN`, carries no lock, and holds a `.session-handoff.md` whose next action reads `verify the wave table`. This session runs in the main checkout, which holds no snapshot.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then retire the snapshot in ../fw-02, then `git worktree remove ../fw-02`, then `git branch -d finish-work/slice-02`, then the leased remote delete

## What must happen

- The plan lists `remove worktree  ../fw-02 — clean, unlocked, at PR 91's merged tip`, with the snapshot's retire above it.
- After the yes, the run re-reads `worktree-state.py --expect-head a1b2c3d ../fw-02`, retires the snapshot on `CLEAN`, and runs `git worktree remove ../fw-02` on `RETIRED`.
- The report reads `CLEARED: 1 snapshot, 1 worktree, 1 branch (local and remote)`.

## What must NOT happen

- Pass `--force` to `git worktree remove`.
- Delete finish-work/slice-02 locally or on the remote before ../fw-02 is gone.
- Read the snapshot whole, exchanges included.
- Delete the snapshot with `rm`.
- List the worktree for the developer to remove.
- Merge anything.

## Why this fixture exists

The developer, 2026-11-05: "yes, cleanup the worktree for this issue and session and close the issue. it's weired that phil:done doesn't just do that. why is that?" This reverses the fixture's 2026-11-02 expectation, that a worktree an earlier session made is listed and never removed. `worktree-state.py` reads the adversarial run's losses as `HIDDEN`, and a lock holds a worktree another session works in.
