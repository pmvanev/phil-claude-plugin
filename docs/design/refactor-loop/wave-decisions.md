# Wave Decisions — phil:refactor-loop architecture (DESIGN)

**Architect:** Morgan (nw-solution-architect), interaction_mode = propose, scope =
application/components. **Date:** 2026-06-17.

This is NOT a standard nWave feature: no DISCUSS/DISCOVER/SSOT artifacts exist (confirmed
absent). Requirements input = `rgr-loop.md` (grounded design) + `rgr-loop-gap-analysis.md`
(cited gap memo). Deliverable = the architecture for a **Claude Code skill + subagent
system**, built downstream via `nw:forge` (specs, not code).

## Decisions taken

| # | Decision | ADR | Rationale source |
|---|---|---|---|
| D1 | `/phil:refactor` stays untouched; `/phil:refactor-loop` is a separate, coexisting skill | — (hard constraint) | brief; rgr-loop §decision-2026-06-17 |
| D2 | Substrate: lean skill-loop v1 first, Workflow-tool v2 behind a measured trigger | ADR-001 | rgr-loop §substrate |
| D3 | v1 = proposer + 1 separate correctness critic; disjoint panel is earned | ADR-002 | rgr-loop §critic-panel; AHE non-additivity |
| D4 | Backlog is a dependency DAG; reverted prerequisite auto-invalidates dependents | ADR-003 | gap-memo §complexbench |
| D5 | Test-file lockbox = tool-scoping + PreToolUse hard guard | ADR-004 | AHE; gap-memo §agentspec |
| D6 | Behavior preservation certified only by external suite + manifest-vs-actual check | ADR-005 | rgr-loop §the-seam; gap-memo §eval-driven-iteration |
| D7 | Pinned constraints compaction-immune + re-asserted each iteration; HALT reachable everywhere | ADR-006 | gap-memo §openclaw/replit/vend |
| D8 | Rubric frozen, committed, regression-tested on change | ADR-007 | Sage; gap-memo §eval-driven-iteration |
| D9 | Guards mapped to the four-outcome taxonomy; hard-guard only recurring invariants (leverage law) | §3 | gap-memo §agentspec |
| D10 | Verdict = span+evidence typed quadruple; proposer emits predicted-impact manifest | §2.5/2.6 | gap-memo §hart; rgr-loop §messaging |
| D11 | Convergence claims gated on the 6-point acceptance checklist (no-op baseline, critic self-test, validated judge, CIs, contamination caveat, no soft conjunction) | §6 | gap-memo §agentic-benchmarks/§evaluation-engineering/§terminal-bench/§benchmark-contamination |

## Three safety invariants (all honored)

1. External suite gates — proposer never self-certifies; manifest checked vs ACTUAL delta. (ADR-005)
2. Proposer can never edit tests — tool-scoping + PreToolUse block. (ADR-004)
3. Pinned constraints compaction-immune + re-asserted each iteration; HALT/user-abort always reachable. (ADR-006)

## Cage / brain seam

- **Cage (deterministic):** loop, iteration counter, max-iter bound, when to run agents/suite,
  apply diff, revert on red, run lint/types/tests + read exit codes, the stop/HALT decision,
  all guards.
- **Brain (LLM subagents):** what to refactor and how (proposer), whether a refactor improves
  quality (critic), whether a surviving critique is weak (typed verdict, not a halt).

## Deliverables for nw:forge (component count: 4 subagents + 1 orchestrator skill + 1 hook layer + 2 state files = 8 buildable artifacts)

- `skills/refactor-loop/SKILL.md` (orchestrator: state machine + gating + stop guard)
- `commands/refactor-loop.md` (thin stub → loads the skill)
- `agents/refactor-proposer.md`
- `agents/refactor-critic-correctness.md` (v1)
- `agents/refactor-critic-idiom.md`, `agents/refactor-critic-architecture.md` (v2 panel)
- `refactor/rubric.md` (frozen), `refactor/ledger.md` (DAG), `refactor/self-test/` (critic regression fixtures)
- `settings.json` hooks: PreToolUse test-write-block (G2), Stop anti-exit (G10), pinned re-inject (G7)

## Open decisions — RESOLVED 2026-06-17 (full detail in architecture.md §11)

All 11 resolved before forge. User decisions: `max_iterations` = **10** (not 25 — conservative
for a watched v1); θ = **0.6**; HALT = **interrupt-only for v1** (sentinel user-abort deferred to
v2 — accepted v1 limitation on invariant #3); ledger = **project-root `.refactor-loop-ledger.md`**.
Recommended defaults adopted for the other seven (shared test-runner include; discrete Bash
`$?` gates; model tiers proposer+correctness=strong, idiom=cheaper, arch=strong; CLAUDE.md
test-path override; language-specific API-diff starting Python+TS; Stop-hook gated to
refactor-loop sentinel; self-test fixtures in `refactor/self-test/`).
