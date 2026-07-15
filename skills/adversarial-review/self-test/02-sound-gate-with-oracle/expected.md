# Expected outcome — fixture 02 (the hard half: a real oracle earns a sound gate)

A deterministic oracle (the test suite) is available and reports a real failure. The reviewer must
partition its findings and let the oracle-backed one carry the `sound-gate` label.

**Pins:** US-2, AC2.1–AC2.2, C2 (hard/soft split). This is where "hard-checkable" becomes concrete
for a code target.

**Expected decision:** `SOUND-GATE`. The verdict:
- `overall_label: "sound-gate"` — at least one hard finding is backed by a real oracle result (C4/
  ADR-011).
- A `kind: "hard"` finding for the failing test: `evidence` **cites the actual result**
  (`test_bulk_discount_rounding` failed, expected 90.00 got 90.01), not a prediction — the reviewer
  **inherits** the oracle result, never re-implements or re-runs its own check (ADR-005 lineage).
- A `kind: "soft"` finding for the non-intention-revealing name `calc2` — a judgment call, ranked
  below the hard failure.

**Checkable assertions (all must hold):**
1. `overall_label == "sound-gate"`.
2. Every finding has a `kind` of `hard` or `soft`.
3. The hard finding's `evidence` quotes the actual failing-test result, not a guess.
4. The soft finding is present and ranked below the hard finding.

**Gate failure (blocks the skill change):** the hard finding predicts a failure instead of citing the
real result (turns a sound check back into an opinion); OR findings are not tagged `hard`/`soft` (C2
lost); OR `overall_label` is `draft-signal` despite a backing oracle (under-claiming — the inverse
dishonesty). If no runner had been detectable, the correct behavior degrades to fixture 01
(`draft-signal`) — asserted there and in fixture 03.
