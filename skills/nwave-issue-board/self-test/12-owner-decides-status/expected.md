# Expected outcome — fixture 12 (derivation has an owner, and it is not this skill)

**Safety core.** This pins the contradiction the skill shipped in its first draft: a flat prohibition
on reading status from `roadmap.json`. `nwave-slice-status` takes done-ness from "the execution log,
`progress.md`, or the per-step `status` field, whichever the project actually maintains" — and this
project maintains the third. A local rule forbidding it would publish `unknown` for a feature whose
status is recorded and available.

The general form matters more than this case: any precedence rule invented here will eventually
disagree with the skill that owns precedence, and the disagreement will be invisible because both
outputs are well-formed tables.

**Expected decision:** `OWNER-DECIDES`.

**Checkable assertions (all must hold):**

1. The published statuses are the values `nwave-slice-status` returns, sourced from the roadmap's
   `status` field.
2. No row reads `unknown` on the grounds that the execution log is missing.
3. No fold over `execution-log.json` is performed here, and no rule about which source wins is stated
   or applied here.
4. The absence of an execution log is not itself published as a finding; it is the owner's business.

**Gate failure (blocks the skill change):** rows published as `unknown` because the execution log is
absent; OR any source-precedence decision made in this skill.
