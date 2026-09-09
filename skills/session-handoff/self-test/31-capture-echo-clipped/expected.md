# Expected — 31 (the echo is bounded; the record is not)

**Pins:** issue #43 on the **capture** path. Fixtures 28 and 29 are both read-backs, so without this one
the ceiling was pinned on only one of the two paths it governs.

**Expected decision:** `CAPTURE` + `PROJECTED` + `REPORT-CLIPPED`.

## The asymmetry this fixture exists to hold

On read-back the withheld words are one file read away and the reader is often not their author. **On
capture the author is present, and the echo is the only proofread the record ever gets** — step 10 says
it exists so *a mistake is visible immediately*. Clipping it therefore costs something read-back
clipping does not: a mis-recorded decision can slip past while the one person who could correct it is
still in the chair.

The echo is bounded regardless, because an unbounded one is the wall of text the ceiling exists to
prevent. **`REPORT-CLIPPED` and its count are the whole mitigation**: they tell the author something
went unshown, so *open the file* is an available next move rather than an unknown one. Accepted cost,
recorded as one.

## What must appear

- `CAPTURE`, and `PROJECTED` — the card was refreshed, and a `CAPTURE` reporting neither
  `PROJECTED` nor `PROJECTION-UNREFRESHED` silently skipped the card.
- Both frames, with `crossed 1` on the outer and **no `crossed` on the inner**, which sits at zero.
  Neither is marked `⚠ stale`: the threshold is two.
- The recorded next action.
- `REPORT-CLIPPED`, **counting against what was recorded** — of the form *three of six decisions shown;
  three decisions and five ruled-out approaches withheld* — and naming `.session-handoff.md` as their
  home. The exact split is not pinned; the basis of the count is.

**The budget, measured rather than assumed.** The mandatory part of the echo costs 78 words — the
outcome codes (10), the projection line (8), the two rendered frames
(48) and the next action (12) — leaving 222 for reasoning that runs
610. Measured for the reason fixtures 28 and 29 were: both first shipped estimated costs that
measurement refuted, and **a ceiling fixture whose arithmetic does not force the clip is not testing the
ceiling.**

## Gate failures

- **Recording less than the session reached.** The severest failure available here. The file is
  uncounted; a capture that drops a decision so its own echo fits has destroyed the payload to tidy the
  report, and no later read-back can tell.
- **Clipping in silence.** A `CAPTURE` that echoes three decisions and reports nothing else has
  asserted it recorded three.
- **Reporting `CEILING-BREACHED`.** The mandatory content fits; clipping did real work here.
- **Dropping the projection line to save room.** It is mandatory, and its absence is
  indistinguishable from the silent card-skip it exists to expose.
- **Printing `crossed 0`**, or suppressing `crossed 1`. The ceiling does not override a render rule.

**Why this is not fixture 28 on another path.** 28 withholds from a *historical* record for a reader who
can go and read it. This withholds from a *proofread*, at the only moment the record is still cheap to
correct. Same outcome code, different cost, and the skill says so rather than leaving the two to look
alike.
