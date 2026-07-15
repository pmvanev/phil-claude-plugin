# Slice 03 — Cross-domain sequencing & seam-level expectations (DEFERRED — post-v1)

**Status:** OUT of v1. Recorded here so the later capability has a home; do NOT build in this cycle.

**Goal (one sentence):** When a single intent decomposes into MULTIPLE phil:work initiatives AND
MULTIPLE nwave initiatives with cross-domain dependencies, `/phil:edd` strings them together and
adjudicates SEAM-LEVEL expectations that no single sub-initiative's oracle can cover.

## Sketch (for continuity, not commitment)
- Lift phil:work's MAP → EXECUTE → VERIFY sequencing spine to the INITIATIVE level: a flat ordered
  list of heterogeneous initiatives (each routed to nwave or phil:work), escalating to a DAG only
  on evidence of real dependencies.
- Each initiative inherits its engine's oracle; each leaf qualitative expectation uses the slice-02
  gate; SEAM-LEVEL expectations ("after all this lands, the system as a whole should X") get an
  evidence gate that runs only after the whole sequence lands.
- Off-ramp discipline bites hardest here: a single-initiative intent must route straight to one
  engine — multi-initiative orchestration is the exception, justified only by cross-domain
  dependencies. Never manufacture a multi-initiative roadmap to look busy (mirrors phil:work MAP §3).
- Anchor that keeps this EDD and not a Gantt chart: every unit AND every seam is framed as an
  expectation graded on executed evidence.

## Why deferred
Most value lands in slices 01–02 (triage/off-ramp + single-engine qualitative gate). Cross-domain
orchestration is the most ambitious and least common case; it should earn its place on evidence
that single-engine EDD is used and the multi-initiative need is real.
