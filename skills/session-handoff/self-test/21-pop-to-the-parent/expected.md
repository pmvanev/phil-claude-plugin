# Expected — 21 (the detour closes and the parent comes back)

**Pins:** slice-02 AC1, and the header rule that every stack write inherits.

**Expected decision:** `POPPED`. Depth 3 becomes depth 2, and the frame now in hand is named — the point
of the verb is that returning is navigated rather than recalled:

```
POPPED — the fixture runner · it needed a flag it did not have
  back to: Fixture 07 · it contradicted the table, so it had to be settled first
  stack now 2 deep
```

**Naming the parent is the assertion, not a courtesy.** A pop that reports only "popped" leaves the human
to re-derive what they have returned to, which is the exact work the stack exists to save. The frame
coming *off* is echoed too, so a mis-aimed pop is visible immediately rather than discovered later as a
missing level.

**`Why`, `Next` and the header are byte-identical afterwards.** A pop is not a capture. It regenerates
the whole file, so the payload and the fingerprint pass through untouched; re-stamping `commit:` here
would disable `RESUME-STALE` exactly as it would on a push.

**Only the innermost frame goes.** Frames 1 and 2 are untouched, in order, with their original
timestamps. Popping to an arbitrary level is editing the stack rather than navigating it — the format is
prose so that a human can do that by hand, and the verb deliberately cannot.

**Gate failures:**

- Dropping any frame other than the innermost, or renumbering the survivors' timestamps.
- Not naming the frame now in hand.
- Any change to `Why`, `Next`, or the header.
- Taking `h1` and writing without re-taking `h2`. Pop is a write and carries the same guard as push.
- Reporting `PUSHED`, `CAPTURE`, or any read-back outcome.
- Refreshing the card. Boundaries refresh the projection; a pop is not a boundary.
