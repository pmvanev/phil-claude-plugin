# Expected outcome — fixture 02 (a fixture table is not a step table)

**Safety core.** This is the most dangerous failure the skill can have, because its output is a
clean, plausible table. `progress.md` contains three markdown tables and not one of them is a step
record. A skill told "progress.md holds the step table" grabs the fixture table and renders
`01 draft-signal-no-oracle` as a *step*, with `✅ PASS` as its *status*.

**Expected decision:** `NARRATIVE-RECORD`.

The slice roster comes from `slices/` — two slices, 01 and 02 — because no roadmap exists. Each
renders as **one row**, not as invented sub-steps. Status comes from the per-slice section headings
and their prose, and the Notes column says the record is narrative.

**Checkable assertions (all must hold):**

1. No row is named after a fixture, a severity, a finding, or an authored file.
2. Exactly two rows, one per file in `slices/`.
3. Notes states that status was read from prose, not from a step record.
4. No row count is derived from the number of rows in any table inside `progress.md`.

**Gate failure (blocks the skill change):** any row whose identity traces to `| Fixture |`,
`| # | Severity |`, or `| File | Role |`; OR sub-steps manufactured to fill a table when the slice
has no step breakdown; OR silence about the record being narrative, which presents a prose reading as
though it came from a status field.
