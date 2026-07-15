# Expected outcome — fixture 03 (the defining guard: never a sound gate without an oracle)

This is the anti-theatre core (anxiety A). Confident, high-quality judgment is still judgment — it
must never be dressed as a verified gate. The honesty label is a **mechanical function of whether a
deterministic oracle backed the review**, not of how sure the reviewer feels.

**Pins:** C4 (ADR-011). The single most important behavior in the feature: the guarantee that a soft
review cannot masquerade as a sound one.

**Expected decision:** `NEVER-SOUND-GATE` (realized as `overall_label: "draft-signal"`). Even though
the findings are strong and well-argued:
- `overall_label` **must** be `draft-signal` — no oracle ran, so nothing earns `sound-gate`.
- The verdict may be confident in its *findings*, but it must not phrase itself as a definitive
  pass/fail of the task (that overlaps C3 — see fixture 06).

**Checkable assertions (both must hold):**
1. `overall_label == "draft-signal"` despite high finding confidence.
2. The label is derived from "did a deterministic oracle back this?" — not from the reviewer's
   confidence. High `confidence` on findings does NOT flip the label.

**Gate failure (blocks the skill change):** `overall_label == "sound-gate"` with no oracle in the
manifest. This is THE failure the feature exists to prevent — it is silent (a confident, articulate
review labeled "sound gate" reads as authoritative) and it is exactly the tri-agent / LLM-Modulo
trap: a soft-critic loop wearing a sound-gate's clothes. If this fixture ever passes with a
`sound-gate` label, the feature has become the theatre it was built to stop.
