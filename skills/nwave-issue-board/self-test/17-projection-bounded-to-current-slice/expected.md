# Expected — 17 (the roster plus one step table, never 94 rows)

**Expected outcome:** `PROJECTION-BOUNDED`. The block carries **22 roster rows** and **the step table for
slice 07 only** — 4 rows. The other 90 steps are not rendered; their slices link to their briefs.

**Why this fixture exists.** The hundreds-of-issues argument justified making steps rows rather than cards,
and a 22-phase feature is the size that made it real rather than hypothetical. **Inverting the mapping
inverts that argument rather than retiring it:** all 94 steps in one description is the same defect wearing
different clothes — one page nobody reads instead of a hundred cards nobody scans. The bound is what keeps
the thirty-second read achievable at any feature size.

**Gate failures:**

- Rendering steps for any slice other than the current one.
- Rendering all 22 slices' step tables behind collapsed sections. Collapsed is still present, still
  regenerated, and still the thing a reader has to skip past.
- Dropping the roster to make room for more steps. The roster is what a teammate reads first.
- Rendering fewer than all 22 roster rows. The roster is bounded by the feature, not truncated.
