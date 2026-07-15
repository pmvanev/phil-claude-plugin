# Expected outcome — fixture 08 (the positive pole: verified-clean earns a sound gate)

The honesty label must be honest in *both* directions. Fixture 03 forbids claiming `sound-gate`
without an oracle (over-claiming); this fixture forbids the inverse — leaving a genuinely
oracle-backed clean result as `draft-signal` (**under-claiming**). A green oracle that ran is real
evidence; the label must reflect it.

**Pins:** C4 (ADR-011) positive pole; completes the label's bidirectional contract with fixtures 02
(oracle + failure → sound-gate), 03 (no oracle → never sound-gate), and 07 (clean, no oracle →
draft-signal).

**Expected decision:** `CLEAN-PASS` with a sound-gate label. The verdict:
- `verdict: "clean"`, `findings: []` — nothing is actually wrong (as in fixture 07).
- `overall_label: "sound-gate"` — a deterministic oracle ran and backed the review (green suite),
  so the clean result is *verified*, not merely *unobjected-to*.
- No manufactured nit to force a findings verdict (as in fixture 07).

**Checkable assertions (all must hold):**
1. `verdict == "clean"` and `findings == []`.
2. `overall_label == "sound-gate"` — because an oracle ran (green), not despite it.
3. No nit is invented to avoid a clean verdict.

**Gate failure (blocks the skill change):** `overall_label == "draft-signal"` despite a green oracle
having run (under-claiming — the reviewer discards real evidence, making a verified pass look merely
soft), OR a nit is manufactured to produce a findings verdict. Under-claiming is the quieter of the
two label failures — it looks conservative and safe — but it is just as dishonest as over-claiming:
it hides that the work was actually verified. The label tracks "did an oracle back this?", full stop.
