# Expected — 16 (a push onto someone else's snapshot, and the payload survives)

**Pins:** slice-01 AC1 (payload survival) and AC3's last sentence (the normal path must succeed), plus DESIGN
DDD-1's central claim — that the guard is content, not identity.

**Expected decision:** `PUSHED`. The frame is appended, the depth is echoed, and the report names the frame
back so a mistyped reason is visible at once:

```
PUSHED — frame 1 · deploy script · the blocker's fix cannot be tested until deploys work
  stack now 1 deep
```

**The three assertions, and they are different assertions.**

1. **`Why` and `Next` are byte-identical afterwards.** Not "preserved in substance" — byte-identical. The
   write is a whole-file regeneration, so the payload passes through the writer untouched; anything that
   re-words, re-wraps or re-orders it has stopped regenerating and started rewriting.
2. **The header is reproduced byte-for-byte.** `captured:`, `commit:`, `dirty:` and `owner:` belong to
   CAPTURE. A push is not a capture, so it re-derives none of them. Re-stamp `commit:` and it always
   matches `HEAD` — at which point `RESUME-STALE` can never fire again, and the worst outcome this skill
   can produce arrives via a routine mid-session note.
3. **The push SUCCEEDS even though a different session wrote the snapshot.** This is the fixture's sharpest
   half and the reason it exists at all.

**Why the second assertion is the one that matters.** An earlier design stamped a `session:` id in the
header and refused a foreign one. Trace it: session N captures, the boundary passes, session N+1 resumes
that snapshot, works, hits a blocker, pushes — and is refused, because the header says N. **Every session
after the first would be blocked on its first push**, since resuming a previous session's snapshot is the
entire purpose of the file. A guard that cannot tell the primary path from the hazard is not a guard.

Content comparison catches the failure that actually matters — a lost update — and is indifferent to who
wrote what.

**Gate failures:**

- Refusing because the snapshot was written by another session. This is the regression this fixture exists
  to catch, and it will look like caution.
- Any change to `Why` or `Next`, including re-wrapping, re-ordering, or "tidying" the decision list.
- **Any change to the header.** Re-stamping `commit:` from the live tree is the natural mistake for
  something told to regenerate a whole file while holding a `git rev-parse` grant, and it silently
  disables the freshness verdict for the life of the snapshot.
- Stamping `captured:` with the push time. A push is not a capture.
- Editing the `## Stack` section in place rather than regenerating the file. It happens to work here,
  because there is nothing else to lose; it is the habit that loses the payload when there is.
- Writing without re-reading the file immediately before the write. The compare-and-swap has no value if
  `h2` is not taken.
- Reporting `CAPTURE`. A push is not a capture; the paths do not interleave.
- Refreshing the card. The projection is refreshed at boundaries, by `/phil:handoff`.
