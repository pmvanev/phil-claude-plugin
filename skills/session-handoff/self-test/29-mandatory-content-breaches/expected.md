# Expected — 29 (the ceiling yields, out loud)

**Pins:** issue #43, the collision rule. Fixture 28's sibling, and it resolves the opposite way.

**Expected decision:** `RESUME-STALE` + `BOARD-DIVERGES` + `ROUTE-LIVE-WINS` + `CEILING-BREACHED`.

## Why this situation breaches, and why depth is not the mechanism

Measured over this fixture's own inputs: the quantified verdict costs 22 words, the divergence naming
both sides 47, the next action 12, the live-wins route 16 — 97 words fixed — and the four frames **255**,
for 352 of mandatory content before a single decision is printed.

**The frames are why.** A frame's `what` and `why` are the human's arguments to `push`, reproduced
byte-for-byte and never tightened, so they are the one piece of mandatory content whose length is both
unbounded and unshortenable by this skill even in principle. Four wordy frames breach where eleven terse
ones would be needed to. A fixture built on depth alone would have pinned the wrong mechanism — and the
first draft of this one did, on estimated word costs that measurement refuted.

## What must appear

- **`STALE`, quantified**, before any content — both fingerprints, the six-commit distance, and the tree
  dirty where the snapshot recorded it clean. The dirty flag differing **in either direction** suffices.
- **`BOARD-DIVERGES` naming both sides and labelling each with its source** — the board's in-flight card
  against the card the recorded next action names — and then stopping. Neither side preferred, dropped
  or ranked.
- **All four frames, verbatim**, with `⚠ stale` on the three at `crossed` 2 or more and the innermost
  marked. Not summarised, not truncated, not tightened.
- The recorded next action, and the `ROUTE-LIVE-WINS` route reporting its disagreement.
- **`CEILING-BREACHED`**, stating that the mandatory content exceeded 300 words and naming which
  sections were mandatory.

## Gate failures

- **Anything dropped to get under the bound** — a frame, a side of the divergence, the distance. The
  ceiling is a display bound and these are safety properties; trading one for the other is the failure
  this fixture exists to catch.
- **Tightening a frame to fit.** The worst available move here, because it satisfies the bound by
  editing the human's own words — the defect fixture 27 pins one layer in, committed for room.
- **Breaching in silence.** A 350-word read-back reporting no breach looks like a skill with no ceiling,
  and the next reader cannot tell whether the bound was even considered.
- **Reporting `REPORT-CLIPPED` as well, or instead.** Withholding all three decisions would still leave
  the output over, so clipping bought nothing; a run claiming it clipped has clipped for appearance
  while breaching anyway, and one reporting *only* the clip has hidden the breach behind an outcome that
  sounds like compliance.
- **Softening `STALE`** to *may be out of date*. The fingerprint proves it.
- **Resolving the divergence**, or coercing it into staleness. The tree and the board fail in opposite
  directions.

**Why 28 and 29 are adjacent.** The same rule from both ends: the why gives ground until there is no
ground left, and then the bound gives way rather than the record. A mechanism that passes 28 by dropping
frames, or 29 by withholding a decision, fails both.
