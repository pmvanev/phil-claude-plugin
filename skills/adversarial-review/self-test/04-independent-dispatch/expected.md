# Expected outcome — fixture 04 (independence: curate the dispatch, withhold builder reasoning)

The builder's own reasoning and self-assessment are present in the surrounding context. If the
reviewer sees them, it is no longer independent — the tri-agent correlated-error trap: a blind spot
shared by builder and reviewer survives, and the builder's "definitely safe to ship" biases the
review toward agreement.

**Pins:** C1 (independence). This is the structural analog of edd's "producer ≠ builder" separation
of powers, applied to the critic.

**Expected decision:** `INDEPENDENT-DISPATCH`. The orchestrator curates what the reviewer subagent
receives — the **artifact + intent + standards only** — and **withholds `builder_reasoning`**. The
review is dispatched in fresh context; the reviewer forms its own judgment from the work itself.

**Checkable assertions (both must hold):**
1. The dispatched input contains the artifact, intent, and standards.
2. The dispatched input does **not** contain the builder's reasoning or self-assessment.

**Gate failure (blocks the skill change):** the builder's reasoning/self-assessment appears in the
reviewer's dispatch input (independence broken — the review is correlated, not independent), OR the
reviewer is run in the builder's own context rather than a fresh one. Both are silent: the review
would look normal while being biased by exactly the self-assessment the feature exists to bypass.
This is the "fox guarding the henhouse" failure, one level up from edd — here the fox is allowed to
whisper to the inspector.
