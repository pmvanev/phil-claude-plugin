# ADR-005 — phil-work: hybrid substrate, delegate-owned gates

Status: accepted (DESIGN wave, 2026-07-13) · Feature: phil-work

## Context

`/phil:work` is a wave-based orchestrator for invisible technical initiatives (DISCUSS D1–D9).
Its central constraint is D3 (**general contractor — do not re-implement execution**) and D9
(**artifact-aware preservation oracle**: executable self-test/suite for code, human-approval
diff for prose). The repo already contains two orchestration substrates and both oracle kinds:

- **Prose-skill loop** — `refactor`, `refactor-tests`: thin command → `SKILL.md` → model runs a
  backlog loop, one item at a time. Interactive; gates live in prose.
- **Workflow-tool cage** — `refactor-loop` (ADR-008): deterministic JS owns loop/gate/stop;
  subagents supply judgment. Strong gate enforcement; runs headless.
- **Oracles** — external suite (`refactor`, `refactor-loop`) vs human-approval diff
  (`refactor-tests`, ADR-002).

DESIGN must fix HOW `/phil:work` runs its waves and enforces the preservation floor + goal gate.

## Decision

**Hybrid: a prose-skill spine that delegates each execution wave to the tactical skill that
already owns the right gate.**

- `/phil:work` = `commands/work.md` (thin loader) + `skills/work/SKILL.md` (orchestrator prose).
- The orchestrator OWNS only the interactive, non-safety-critical spine: **FRAME** (scope the
  goal + preservation contract; off-ramp trivial work), **MAP** (survey → wave roadmap),
  **SAFETY-NET setup**, **sequencing**, **VERIFY**, and the **decision trail**.
- Each **EXECUTE** wave DELEGATES to an existing skill, and **inherits that delegate's gate**:
  - **code** refactor → `refactor-loop` (its deterministic Workflow cage IS the preservation oracle),
    or `refactor` / `extract-method` for simpler moves;
  - **prose** (skills/rules/agents) → `refactor-tests` / `redesign-tests` (human-approval diff
    oracle, ADR-002);
  - comment cleanup → `clean-comments`; survey during MAP → `review-code` / `spirit-walk` / hotspot.
- `/phil:work` **never re-implements gating**. The only gate it adds is the cross-wave
  **sequencing rule**: on any delegate failure (suite red, self-test broken, diff rejected),
  stop the sequence, record it, and leave the tree in its last-good state — never red, never a
  faked "done."

The preservation guarantee (anxiety C) is therefore **enforced by the delegate**, not claimed by
new orchestrator machinery.

## Alternatives considered

- **Pure prose-skill loop** (all waves + both gates in `SKILL.md` prose) — rejected: the
  safety-critical gates would live in drift-prone prose, weakening the very preservation
  guarantee that is the feature's reason to exist (anxiety C). Violates D3 by re-implementing
  execution/gating the delegates already provide.
- **Pure Workflow-tool cage** (`workflows/work.js` owns the wave loop + gates) — rejected: the
  interactive FRAME discussion and the per-wave **human-approval** oracle (prose case) fight a
  headless/background cage; it is also the most new mechanism to build, contradicting anxiety B
  (ceremony overhead) and D3.

## Consequences

- (+) Most faithful to D3/D9: the orchestrator composes; the delegates execute and gate.
- (+) Gate strength equals each delegate's: deterministic cage for code, human oracle for prose —
  no new, weaker gate is introduced.
- (+) Least new mechanism; matches "piece it together from what I've already written."
- (+) FRAME stays fully interactive.
- (−) The orchestrator's own spine is prose (drift risk), but drift cannot silently weaken
  preservation because the safety-critical gates are in the delegates. A `self-test` harness
  (DDD6, mirroring `refactor-tests`/`refactor-loop`) pins the orchestrator's safety-critical
  behaviors as a regression gate.
- (−) Requires a routing decision per wave (code vs prose vs comment vs survey) — this is
  slice 05's explicit scope.
- Open: the exact mechanism to invoke a delegate skill from within the orchestrator skill (run
  its slash command vs Skill tool vs Task subagent) is settled empirically by the slice-01
  walking skeleton.
