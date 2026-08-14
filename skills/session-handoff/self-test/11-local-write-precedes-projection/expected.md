# Expected — 11 (the snapshot survives a forge failure)

**Pins:** slice-04 AC1, and the ordering that makes the whole partition safe.

**Expected decision:** `CAPTURE` **and** `PROJECTION-UNREFRESHED`. The snapshot is written and complete.
The card is untouched. The report says both:

```
CAPTURE — .session-handoff.md written (2 decisions, 1 next action).
PROJECTION-UNREFRESHED — could not reach the forge to refresh #26's block.
  The snapshot stands and /phil:resume will read it normally.
  The card still shows what the previous capture projected, with that capture's timestamp.
```

**Why the order is the safety property, not a preference.** The projection is a copy; the snapshot is the
authority. Refresh first and a network failure leaves the authority behind its own published copy — the
card asserting a state the local file never reached, with nothing to reconcile them because the projection
is write-only by design. Write first and the worst case is a stale card that says how stale it is.

**Why this must not report as a failed capture.** The capture *succeeded*; a side effect did not. A run that
reports failure here teaches the user that `/phil:handoff` is unreliable offline, and the next thing they do
is stop running it — losing the local snapshot too, which was the part that worked.

**Gate failures:**

- Any forge call before `.session-handoff.md` exists on disk.
- Reporting only `CAPTURE`. The card is now behind and nothing says so.
- Reporting `NO-OP` or an error. The session advanced work and the snapshot proves it.
- Retrying the refresh until it succeeds, blocking the wind-down. The session is ending; that is the
  circumstance.
- Rolling back the snapshot to keep it consistent with the un-refreshed card. Backwards — the card is the
  copy.
