# Expected outcome — fixture 01 (walking skeleton)

The thinnest end-to-end path: a session that genuinely advanced work records the two unrecoverable
things — what it decided and what it meant to do next — and a fresh session gets both back with a
freshness verdict attached.

**Pins:** slice-01 AC1 and AC2. This is the feature's central bet made concrete — if the fresh session
still needs a re-briefing after reading this, the learning hypothesis has failed and the design pivots
to extending reconstruction instead.

**Expected decision:** `CAPTURE`, then `RESUME-CURRENT`. The snapshot carries both decisions, the next
action, a timestamp, and fingerprint `083c953`. At read-back the fingerprint still matches, so the
verdict is `current` and the briefing is presented.

**Gate failure (blocks the skill change):** the snapshot comes back missing the *why* — the ruled-out
hook and its reason. Recording only the next action passes a naive eyeball check while dropping the
half that no reconstruction could ever recover, which makes the whole feature pointless.
