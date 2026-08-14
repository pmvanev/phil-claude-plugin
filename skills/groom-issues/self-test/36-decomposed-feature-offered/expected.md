# Expected — 36 (the strongest evidence, and it still asks)

**Pins:** slice-07 AC1 and AC5.

**Expected:** `ASK-SET-LEVEL` then `APPLY-CONSOLIDATE`, naming **shape (a)** — an open parent exists. The
question quotes the evidence and states the rollup consequence *before* the user answers:

```
#40 'Auth rework' has four slice cards: #41-#44, real sub-issues, and all four bodies
name docs/feature/auth-rework/.

Under one-issue-per-feature these are roster rows, not cards.
Consolidating means: remove each edge, post a pointer comment on each child, then close it.

After this, #40's completion counter reads 0/0 rather than 0/4 -- the children stop
being counted at all. That is intended: the roster inside #40 carries their state.
```

**Then, on approval, in this order per child:** remove the edge → post the pointer comment → close.

**Why the order is the safeguard rather than a preference.** A closed sub-issue still counts toward its
parent's completion, so closing first renders #40 **100% done** while the work continues. Measured
2026-08-14: `1/0` → close → `1/1 · 100%` → remove edge → `0/0`.

**Gate failures:**

- Closing any child before its edge is removed.
- Acting without asking, on the grounds that the evidence is conclusive. It is — and the operation is still
  irreversible, which is what the question is for.
- Omitting the rollup consequence from the question. The number changes and the user cannot see it coming.
- Posting the pointer comment after the close (auto-close-on-Done drops it).
- Reporting `APPLY-MERGE`. These are not duplicates; nothing overlapped.
