# Upstream issues — phil-work (back-propagation)

Findings surfaced in a later wave that refine an earlier wave's assumption. Per the nWave
back-propagation contract: document the finding, quote the original, state the refinement — do not
silently diverge.

## UI-1 — "prose → refactor-tests/redesign-tests" is imprecise for non-test prose

**Surfaced in:** DELIVER slice 05 (routing fixtures), 2026-07-13.

**Original assumption** (DISCUSS D9 / DESIGN DDD4 / ADR-005, quoted):
> "prose (skills/rules/agents) → `refactor-tests` / `redesign-tests` (human-approval oracle)"

**The gap:** `refactor-tests` and `redesign-tests` detect and act on **test files only** (they
scope to the `testing.md` globs — `*.test.*`, `test_*.py`, `**/tests/**`, etc.). A general
skill / rule / agent / doc file is **not** a test file, so those delegates will not act on it.
The design's "prose" was broader than the delegates it named.

**Refinement (v1, no design reversal):** split prose routing by subtype —
- **test prose** (test files) → `refactor-tests` / `redesign-tests` (unchanged).
- **other prose** (skill / rule / agent / doc) → the **ADR-002 human-approval diff gate applied
  directly** (apply smallest change → developer reviews the uncommitted diff in their editor →
  commit on approve / `git checkout` on reject). No dedicated non-test-prose refactoring delegate
  exists in v1.

**Why this preserves the design, not breaks it:** ADR-005 forbids the orchestrator
*re-implementing a delegate's preservation gate*. Using the human-approval diff gate directly is
**inheriting the oracle** (the human is the oracle, exactly as in ADR-002) — not fabricating an
automated preservation check. DDD4's principle ("preservation is certified by an inherited,
artifact-aware oracle; the orchestrator adds only the sequencing gate") holds unchanged; only the
*mechanism* for non-test prose is made explicit.

**Follow-up opportunity (not v1):** a dedicated `refactor-prose` / `refactor-skill` delegate for
non-test prose with its own human-approval loop would let `/phil:work` delegate this the same way
it delegates test prose, removing the "applied directly" special case. Candidate for a future
phil-plugin feature.

**Landed in:** `skills/work/SKILL.md` FRAME + MAP routing tables (test-prose vs other-prose rows +
the v1-boundary note); fixture `05-route-prose-to-approval` (manifest + expected.md) made accurate.
