# ADR-008: Workflow tool as v1 orchestrator; G2 hook the only surviving guard

**Status:** Accepted
**Date:** 2026-06-18
**Scope:** substrate / orchestrator container (supersedes ADR-001)

## Context

Three substrates were weighed for the loop's deterministic cage. They operate at *different
layers* — this was the key realization:

- **Hooks** are an event-triggered *boundary* layer (PreToolUse, Stop), not an orchestrator.
  They cannot own a loop. G7 (pinned re-inject) and G10 (anti-premature-exit) only exist to
  compensate for a prose loop's weaknesses (context rot, model-driven termination).
- **Workflow tool** — deterministic JS orchestrator native to Claude Code. The loop/gate/stop
  is code the *runtime* executes; the model never sees the loop condition and cannot decide it
  is done. `schema`-validated agent I/O, per-agent model tiers, `parallel()` for the v2 panel,
  journal/resume. In-session agent invocation; first-party. JS sandbox cannot run Bash/FS.
- **mplv2** — a formal executable statechart (`github.com/lostinplace/mplv2`) + Python sim
  engine: deterministic tick, immutable Manifest, priority→weight→seeded-RNG conflict
  resolution, provenance-tagged replayable **ledger** (a sound audit trail). Most rigorous
  cage and best audit story, but it is a *simulation* engine — it decides transitions, it
  cannot run pytest or invoke a subagent. It would require an external Python driver and would
  run *outside* the Claude Code session, so the harness's hooks would not fire on its agents.

## Decision

**The Workflow tool is the v1 orchestrator.** Keep **G2** (test-file write-block) as a
PreToolUse hook — the one substrate-independent safety boundary. **Drop G7 and G10** — the
Workflow owns loop state in JS variables (no compaction → G7 moot) and owns the loop condition
(model can't exit early → G10 moot). Add a thin **gate-runner agent** to cover the JS-can't-Bash
gap: it runs the command and returns a `schema`-validated `{exit_code, stdout}`; the JS routes
deterministically on the integer.

The forged proposer + correctness-critic agents are **substrate-agnostic leaves** and carry
over unchanged. The prose `skills/refactor-loop/SKILL.md` is retained only as an optional
interactive-debug substrate, not the production path.

**mplv2 is recorded as the "rigorous edition" / v2+ option** if the feature graduates into a
standalone, formally-analyzable, auditable tool. The same agents could then be driven by an
mplv2 cage.

## Consequences

- (+) Deterministic loop enforcement *by construction*, stronger than the hook approach.
- (+) `schema`-sound verdict/manifest I/O (G6 becomes sound, not advisory).
- (+) Two of three hooks eliminated; only the genuine safety boundary (G2) remains.
- (+) v2 disjoint-rubric panel is native (`parallel()` + bounded rounds).
- (−) JS cannot run Bash/FS: gate execution, diff apply, revert, and ledger persistence are
  delegated to thin agents; the DAG ledger lives in JS memory during a run and is written out
  at the end (cross-run resume deferred).
- (−) Workflow runs in the background and needs opt-in; less interactive than the prose loop
  (the retained SKILL.md is the fallback for interactive debugging).
- (−) Tool-scoping for plugin-defined agent types under `agent({agentType})` is unverified;
  v1 mitigates by having the proposer *return a diff as text* (never touch disk) and relying on
  the G2 hook, which fires on any agent's write regardless of substrate.

## Trace
Three-way analysis (session 2026-06-18); `harebrain/docs/mpl/mpl.md` (mplv2 ↔ Harel);
`lostinplace/mplv2` README + Feature Status; rgr-loop.md §substrate; gap-memo §replit-database
(audit-trail requirement — mplv2's ledger satisfies it, motivating the v2+ option).
