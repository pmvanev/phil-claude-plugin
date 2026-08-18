# Expected — 26 (the two pop branches fixture 21 cannot reach)

**Pins:** the compare-and-swap on the `pop` path, and `pop` step 5's stale announcement.

**This fixture exists because fixture 21 asserts both and can detect neither.** Its `hash_at_read` and
`hash_at_verify` are equal, so an implementation that never hashes at all produces byte-identical output
and passes — the gate failure it lists (*"taking `h1` and writing without re-taking `h2`"*) cannot fail
it. And its header predates every frame, so nothing it pops is ever stale and the announcement branch
never runs. Fixture 17 pins the compare-and-swap for `push` only; its manifest says `"verb": "push"`, so
a driver has no basis to infer coverage for `pop`.

## Run A — `WRITE-REFUSED`

```
WRITE-REFUSED — .session-handoff.md changed between read and write.
  read   a1b2c3d
  verify 9f8e7d6
  The frame was NOT popped: Wave-to-command table · the task in hand
  Another session or worktree is writing this snapshot. Nothing has been merged or overwritten.
```

**Pop is a write and carries every rule a write carries.** Same guard, same refusal, same prohibition on
retrying — a retry resolves a competing write by overwriting it, which is arbitration. The frame that was
*not* popped is echoed for the same reason push echoes the frame it did not record: so the user knows
exactly what did not happen.

A deletion feels safer than an append and is not. Popping into a file another session just rewrote
removes a frame from a stack that may no longer be the one that was read.

## Run B — `POPPED`, and the stale frame is announced

```
POPPED — the fixture runner · it needed a flag it did not have   ⚠ was stale (crossed 2)
  back to: Wave-to-command table · the task in hand   ⚠ stale (crossed 2)
  stack now 1 deep
```

**Saying it is the point.** A frame that survived two wind-downs and is then closed silently takes with it
the only signal that the record had drifted from the work — the stack looks healthy afterwards precisely
because the unhealthy part was removed. The announcement is the last moment anyone can notice.

Note the shape: **both** frames carry `crossed 2`, which is the only arrangement that lets the innermost
be stale. `CAPTURE` increments every frame in the file together, so a child can never carry a higher count
than its parent — `parent ≥ child` is a theorem of the rule, not a coincidence.

An earlier draft of this fixture had the child at `crossed 2` under a parent at `crossed 1`: a state no
sequence of pushes and captures can produce. Its prose then claimed the fixture *"guards against an
implementation that assumes staleness accumulates outward"*. It **does** accumulate outward. That gate
item would have failed a correct implementation, and a reader would have concluded the rule was wrong.

**Gate failures:**

- Run A writing anything, retrying, or merging.
- Run A omitting either hash, or the frame it did not pop.
- Run B popping without mentioning the stale mark.
- Run B popping frame 1 because it "looks older", or because both are stale. Innermost only, always.
- Accepting a stack where a child's `crossed` exceeds its parent's. That state is unreachable.
- Either run reporting the other's outcome.
