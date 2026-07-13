# Slice 05 — Breadth + trail: route to the right skill; leave an evolution record

**Goal:** MAP routes each wave to the most suitable tactical skill across initiative types (refactor, cleanup, extract, test work), and VERIFY leaves a richer decision/progress/evolution trail — completing the broad-scope promise.

## IN scope
- Skill-routing heuristics in MAP: pick the delegated skill per wave from the full set
  (`refactor-loop`, `refactor`, `extract-method`, `review-code`, `clean-comments`,
  `redesign-tests`, `refactor-tests`) based on the wave's change type.
- Support the broader initiative types named in the brief (cleanup, dependency/perf passes,
  larger re-architecture) — verified on at least two distinct real initiative types.
- VERIFY writes an evolution summary (what changed, why, outcome vs goal) alongside the
  decision log and progress entries; the documentation namespace/schema is settled here.

## OUT scope
- Migration-specific tooling beyond delegation (a migration is handled as a re-architecture
  initiative; no bespoke migration engine).

## Learning hypothesis
**Disproves** "one orchestrator covers the broad span of invisible work" **if** routing across
initiative types proves so varied that each type needs its own bespoke workflow.
**Confirms** the broad-scope claim **if** the same FRAME→MAP→SAFETY-NET→EXECUTE→VERIFY spine,
with per-wave routing, handles ≥2 distinct initiative types with only skill-selection differences.

## Acceptance criteria
- MAP selects an appropriate tactical skill per wave and justifies the choice in the roadmap; demonstrated across ≥2 distinct real initiative types (e.g. an extraction and a cleanup).
- VERIFY produces an evolution summary plus the decision/progress trail in the settled namespace.
- The full run on each type ends with preservation floor + goal gate both green (or an honest not-met report).

## Dependencies
- Slices 01–04. All tactical skills listed above.

## Effort estimate
~1–1.5 days. **Reference class:** `docs/evolution/` summaries already produced by nwave finalize.

## Pre-slice SPIKE
None — all delegated skills exist; this slice is routing + documentation, not new mechanism.
