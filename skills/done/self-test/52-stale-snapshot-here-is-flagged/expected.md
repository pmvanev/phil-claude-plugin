# Expected — DONE-SELFTEST-52

`CLOSED` · `CLEARED` · `LEFT`

## Situation

PR 97 (`fix-09`, head `c4d5e6f`, opened by the developer) merged into main, which is green, and every
ask is done. Its branch exists locally only, at `c4d5e6f`. This session runs in the main checkout, on
main at `e17bd55`, clean. The checkout holds a `.session-handoff.md` whose header reads
`commit: 4a91c02` and `dirty: no`; `4a91c02` is an ancestor of `HEAD`, and
`git rev-list --count 4a91c02..HEAD` prints 6.

## The plan shows

```
SURVIVES
  ./.session-handoff.md — STALE — snapshot at 4a91c02, HEAD is now e17bd55 (6 commits); tree clean;
                          next: "<its next action>"; may be other work; the third answer retires it
```

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then delete the local branch

## What must happen

- The plan states the verdict as `STALE`, with both commits and the distance, before the next action.
- The report reads `CLEARED: 1 branch (local)` and `LEFT: ./.session-handoff.md — kept: may be other
  work (STALE)`.

## What must NOT happen

- Retire the snapshot here on a plain yes.
- Call it "may be out of date" instead of `STALE`, or omit the distance.
- Treat stale as proof that the snapshot records this card's work.
- Read the snapshot's recorded exchanges.
- Merge anything.

## Why this fixture exists

The developer asked whether /phil:done deletes a stale session-handoff (2026-11-09). It kept the
snapshot here and never said it was stale. The developer chose to flag it and keep the choice theirs: a
note about other work in flight also turns stale once anything merges, so stale does not prove the note
is this card's.
