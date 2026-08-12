# Expected outcome — fixture 07 (the recorded owner went stale)

The snapshot is not wrong about what was true when it was written; it is out of date. That is a
different failure from fixture 04 — here only the *routing* has drifted, and the board still knows the
truth.

**Pins:** slice-02 AC3.

**Expected decision:** `ROUTE-LIVE-WINS`. The spine routes to `/nw-execute` from the live
`wave: deliver` label, and **reports the disagreement** — recorded `/nw-distill`, live `wave: deliver`.

**Gate failure (blocks the skill change):** either half —

- routing to the recorded `/nw-distill`, which re-runs a finished wave;
- routing to the live owner **silently**. Resolving the disagreement without mentioning it hides that
  the snapshot has drifted, which is the one signal that would tell the user their capture habit is
  falling behind.

The board is authoritative on wave, exactly as it is authoritative on card status in fixture 10. The
snapshot never overrules a source that owns the fact.
