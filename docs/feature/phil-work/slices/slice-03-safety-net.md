# Slice 03 — SAFETY-NET: characterization coverage before structural change

**Goal:** Before any wave cuts structure, `/phil:work` checks coverage over the change surface and, where the seam is thin, adds characterization / golden-master / contract tests — so the preservation floor is *enforced*, not merely claimed.

## IN scope
- SAFETY-NET step between MAP and EXECUTE: assess whether the change surface is pinned.
- Where the pin is thin, pin current observable behavior: characterization / golden-master / contract tests for **code**; captured self-test scenarios or a recorded human-approval baseline for **prose artifacts** (skills/rules/agents) — delegating authoring where a tactical skill fits.
- Establish and record a good baseline before EXECUTE begins.
- EXECUTE's preservation gate now checks "pinned behavior intact + oracle passing," not just a bare suite run.
- Where a seam has no feasible executable oracle, fall back to the human-approval diff gate and flag the wave high-risk for manual review rather than proceeding silently.

## OUT scope
- Declared per-initiative goal metric (slice 04).
- Broad skill routing (slice 05).

## Learning hypothesis
**Disproves** the anxiety-C worry ("preservation is claimed but not actually enforced") **is worth a dedicated step** — i.e. this slice fails to convince — **if** real initiatives already arrive with enough coverage that SAFETY-NET rarely adds anything.
**Confirms** the step is essential **if** on real initiatives SAFETY-NET repeatedly finds thin seams and the added characterization tests catch at least one regression EXECUTE would otherwise have shipped.

## Acceptance criteria
- On a real initiative with a thin seam, SAFETY-NET reports the coverage gap, adds characterization test(s) pinning current behavior, and records a green baseline before EXECUTE runs.
- EXECUTE's preservation gate fails if a characterization test breaks, triggering revert of that wave — demonstrated with a deliberately behavior-changing edit that the net catches.
- A hard-to-test seam is flagged high-risk (manual-review) rather than passed silently.

## Dependencies
- Slices 01–02. `redesign-tests` / `refactor-tests` reuse for test authoring; testing.md rules; test-runner detection.

## Effort estimate
~1 day. **Reference class:** characterization-test setup in `refactor-tests` self-test harness.

## Pre-slice SPIKE
Optional half-day probe: confirm a repeatable way to detect "thin coverage over a named change surface" for BOTH the plugin's JS/Python test suites AND prose artifacts (which have no code coverage — the "pin" there is self-test scenarios or a human-approval baseline). Uncertainty is moderate (coverage-mapping heuristics + the prose case), so timebox before committing the full slice.
