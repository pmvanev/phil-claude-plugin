# ADR-001: Skill-loop first; Workflow tool deferred to v2

**Status:** SUPERSEDED by [ADR-008](adr-008-workflow-orchestrator.md) (2026-06-18)
**Date:** 2026-06-17
**Scope:** substrate / orchestrator container

> **Superseded.** After a three-way substrate analysis (prose skill-loop + hooks vs. the
> Workflow tool vs. mplv2 statecharts), the decision reversed: the Workflow tool is the v1
> orchestrator, not a deferred v2. Reason — the prose skill-loop's two structural mitigations
> below (the Stop hook G10 and "exit codes can't drift") are exactly the weaknesses the
> Workflow eliminates by construction, and the hooks weren't wired yet (near-zero sunk cost).
> The prose SKILL.md survives only as an optional interactive-debug substrate. See ADR-008.

## Context

The orchestrator's control flow (loop, gates, stop, HALT) can live in prose a model
executes (a SKILL.md) or in executable code (the Workflow tool — JS with real loops,
barriers, `schema`-validated agent I/O, per-agent model selection). rgr-loop.md §substrate
frames this as a *determinism dial*: more reliability ⇒ more control flow moves from prose
into code. The Workflow tool is "the closest CC gets to cage-owns-control-flow" but needs
opt-in and runs in the background.

## Decision

Build the **lean skill-driven loop first**: `/phil:refactor-loop` SKILL.md as orchestrator,
hard gates as real Bash (reads exit codes itself), proposer + 1 critic subagents, Stop hook
for anti-premature-exit. Prove convergence (ADR §6 checklist) on a real package. **Then**
lift orchestration into a Workflow tool for the disjoint-rubric panel + bounded rounds +
tiebreak.

## Consequences

- (+) Native, debuggable, shippable now; no opt-in/background friction.
- (+) Forces the convergence proof before added machinery.
- (−) Loop control lives in prose the model executes → can drift; the Stop hook (G10) and
  the hard Bash gates are the structural mitigations (prose can drift, exit codes cannot).
- The migration trigger is **measured, not scheduled** (see ADR-002).

## Trace
rgr-loop.md §substrate ("the determinism dial"); gap-memo §terminal-bench (structure beats
volume — more iterations is not a strategy).
