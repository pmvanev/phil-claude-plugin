# Expected outcome — fixture 08 (schema migration → expand and contract waves)

The initiative renames a column that the running release reads and writes. A rename in one wave
leaves the previous release unable to run against the new schema, so a rollback restores nothing.
The manifest gives the driver the initiative, the goal and the scope signal; the roadmap is the
output under test, held in `expected_roadmap`.

**Pins:** `rules/continuous-delivery.md` — Database Changes ("expand, then contract, in separate
releases") and "Roll back on demand" — as FRAME §1 and MAP §2 apply them to a migration.

**Expected decision:** `SPLIT-EXPAND-CONTRACT`. FRAME does not off-ramp the rename: the running
release reads and writes the column, so it is not a lone rename. MAP reads
`rules/continuous-delivery.md` before the roadmap and plans the five waves of `expected_roadmap` in
order: expand (add `customer_id`, make `cust_id` nullable, write both), backfill, switch reads while
still writing both, stop writing `cust_id`, then contract (drop `cust_id`). It marks every wave
`ships alone`, and plans the contract wave last, for Resume to confirm before it runs.

**Gate failure (blocks the skill change):** FRAME off-ramps the rename to a single skill; the
roadmap renames the column in one wave, omits the backfill, or puts two of these waves in one
release; or it leaves `cust_id` required while a wave stops writing it.