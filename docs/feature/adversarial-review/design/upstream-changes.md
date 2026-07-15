# Upstream changes — adversarial-review (DESIGN → DISCUSS)

For product-owner review. DESIGN changed one DISCUSS assumption.

## Change: slice 03 (host wiring) dropped; composition is doc-only

- **Original (DISCUSS):** slice 03 wired `phil:work`'s review-wave to gate on the typed verdict
  programmatically.
- **New (DESIGN, ADR-010):** v1 is standalone only and edits no existing skill. Composition is
  delivered as a documented typed contract + Workflow-weaving pattern. Hosts adopt later, each as
  their own work.
- **Trigger:** explicit user direction (2026-07-15) — build standalone, don't touch other
  commands/skills.
- **Impact on DISCUSS artifacts:**
  - Job / persona / journey / constraints C1–C5: **unchanged**.
  - US-3 ("a host gates on the verdict") is **deferred out of v1** — it becomes a future host's
    story, not this feature's. US-1 (WS) and US-2 (hard half) are unaffected.
  - KPI-4 (composability) is re-scoped: measured as "the published contract is consumable without
    re-judging" (a design property of the schema), not as a live host integration.

No changes needed to `jobs.yaml`, the persona, or the journey. This note records the slice/story
scope reduction for PO awareness.
