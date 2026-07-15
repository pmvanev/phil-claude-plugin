# DESIGN Decisions — adversarial-review

## Key Decisions
- [DDD1] Substrate = prose spine + Task-dispatched reviewer subagent (not a Workflow cage):
  single dispatch→verdict, advisory, no loop/gate to make deterministic. (see: adr-010)
- [DDD2] Reusable unit = `agents/adversarial-reviewer.md`; skill is the standalone driver; typed
  verdict is the composition contract. (see: adr-010)
- [DDD3] Verdict schema pattern-copies `refactor-critic-correctness` + `overall_label` + per-finding
  `kind`. (see: adr-010/011)
- [DDD4] Hard/soft split generalized to PROSE oracles; mechanical `sound-gate`/`draft-signal` label.
  (see: adr-011)
- [DDD5] Reviewer independence v1 = single fresh-context subagent; different-model/multi-lens panel
  = documented extension seam (accepted v1 risk). (see: adr-010)
- [DDD6] Standalone advisory flow; report by default, no trail unless asked. (see: adr-010)
- [DDD7] Composition = documentation only; NO existing skill edited. (see: adr-010)

## Architecture Summary
- Pattern: modular prose skill, ports-and-adapters (edd / phil-work lineage).
- Paradigm: N/A — prose artifacts (Claude Code plugin); no code paradigm, no CLAUDE.md write.
- Key components: command (thin loader) · skill spine · reviewer agent (reusable unit) · self-test
  fixtures · acceptance.feature.

## Reuse Analysis
| Existing Component | File | Overlap | Decision | Justification |
|---|---|---|---|---|
| refactor-critic-correctness | agents/refactor-critic-correctness.md | critic + span-evidence schema + anti-flattery + reason-first | CREATE NEW (pattern-copy) | different judgment domain; ADR-003 precedent; source unmodified |
| refactor-loop GUARD | skills/refactor-loop/SKILL.md | severity θ + ranking | REUSE (pattern ref) | prose reference; source unmodified |
| test-runner-detection | skills/shared/test-runner-detection.md | code-oracle detection | REUSE (invoke) | read-only helper; source unmodified |
| ADR-002 human port | docs/product/architecture/adr-002-*.md | advisory human presentation | REUSE (pattern) | same port mechanism |

Zero unjustified CREATE NEW; **zero existing skills modified**.

## Technology Stack
- Prose artifacts (command/skill/agent markdown) authored per nw-agent-builder / nw-forge
  conventions. Oracles prose-shaped (self-test fixtures, ADR-002 human diff, acceptance.feature).

## Constraints Established
- Inherit oracles, never re-implement (ADR-005 lineage). Honesty label is mechanical, not a
  judgment (ADR-011). Reviewer advisory, never self-adjudicating (C3). Independence via fresh
  context (C1).

## Outcome Collision Check
- SKIPPED — methodology/prose feature; no `docs/product/outcomes/` registry in this plugin
  (per D-6 "code-feature pipelines only" gate-scoping).

## Upstream Changes
- Slice 03 (host wiring) dropped; composition is doc-only. US-3 deferred out of v1. See
  `design/upstream-changes.md`.

## Handoff
- To: DISTILL (acceptance-test / self-test design). Deliverables: feature-delta.md DESIGN [REF]
  sections, ADR-010/011, brief.md Application Architecture entry + C4 diagrams, slice briefs 01–02.
- Open for DISTILL: typed-verdict JSON field names + fixture set; prose-oracle catalog breadth;
  reviewer invocation mechanism (Task vs Skill) settled by the WS.
