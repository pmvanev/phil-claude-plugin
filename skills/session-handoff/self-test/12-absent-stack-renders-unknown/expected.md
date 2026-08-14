# Expected — 12 (absent is not empty)

**Pins:** slice-04 AC2. The sharpest assertion in the slice, and the one whose failure is invisible.

**Expected decision:** `RECONSTRUCT`, and the card's reasoning sections read:

```
Why    unknown — no snapshot has been projected for this feature
Next   unknown — same
Stack  unknown — same
```

**Never this:**

```
Stack
(nothing)
```

**Why the difference is the whole point.** An empty stack is a **claim about the work**: nobody was
diverted, the path was straight. `unknown` is a **claim about the record**: nobody wrote it down. A teammate
inheriting the feature acts differently on each — the first says *pick up where the roster points*, the
second says *ask the owner, or expect surprises*. They are opposite instructions and they render almost
identically, which is why the rule has to be explicit rather than obvious.

This is the sibling rule to `unknown` never being published as `not started`, one artifact over. Both are
the same defect: **a gap in the record rendered as a fact about the world.**

**Gate failures:**

- Rendering an empty section, or omitting the headings so a reader cannot tell they were considered.
- Rendering `Stack: none` or `no diversions`. Both are the empty claim in words.
- Presenting the position block as though it were a full briefing. Position is derivable and present; the
  *why* is neither, and a briefing that does not say so overstates what it knows.
- Reporting `RESUME-CURRENT`. There is no snapshot to be current.
- Reading the card's position block **as** the snapshot. It is a projection of the artifacts, not of a
  capture, and treating it as recorded state inverts the one-way rule.
