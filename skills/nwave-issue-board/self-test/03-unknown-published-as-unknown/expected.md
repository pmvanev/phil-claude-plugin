# Expected outcome — fixture 03 (absence of evidence, published)

**Safety core.** `nwave-slice-status` already refuses to call these steps `not started`, because that
asserts something about the work from a fact about the record. This skill must not undo that refusal
on the way out — and the temptation is real, since `unknown` looks like a gap in a public table while
`not started` looks like a plan.

**Expected decision:** `UNKNOWN-PUBLISHED`.

**Checkable assertions (all must hold):**

1. Every published row reads `unknown`. Not one reads `not started`.
2. A line inside the block states why: no status is recorded and no execution log exists.
3. No step is published as `current`. With nothing known, there is no defensible "where we are" to
   show the team.
4. Any count line reports what is recorded, not what is done — "0 of 5 recorded", or no count.

**Gate failure (blocks the skill change):** any published row reading `not started`; OR a `current`
marker chosen by position; OR a count asserting zero completions from an empty record.
