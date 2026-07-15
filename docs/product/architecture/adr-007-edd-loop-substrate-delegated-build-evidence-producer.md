# ADR-007 — edd-loop: prose spine, delegated build, evidence via independent producer

Status: accepted (DESIGN wave, 2026-07-15) · Feature: edd-loop

## Context

`/phil:edd` adds an Expectation-Driven Development discipline on top of the plugin's existing
build engines (DISCUSS job `prove-qualitative-expectations-with-evidence`). Its core moves are:
capture expectations → classify (engine-checkable vs qualitative) → **off-ramp** to nwave /
`phil:work` when everything is already provable → for the qualitative residue, delegate the
build to one engine and attach a **scaled executed-evidence gate** the human adjudicates
(DISCUSS D1–D5). Two hard constraints from DISCUSS: (a) compose nwave and `phil:work`
**unchanged** and inherit their oracle (ADR-005 lineage — never re-implement verification);
(b) **separation of powers** — the agent that produces/judges the evidence must not be the
builder ("fox guarding the henhouse").

The repo already offers two orchestration substrates (per ADR-005): a **prose-skill loop**
(`work`, `refactor-tests`) and a **Workflow-tool cage** (`refactor-loop`,
`docs/design/refactor-loop/adr-008`). DESIGN must fix HOW `/phil:edd` runs.

## Decision

**A prose-skill spine that delegates the build and gathers evidence through an independent
subagent; the human is the adjudicating oracle.**

- `/phil:edd` = `commands/edd.md` (thin loader) + `skills/edd/SKILL.md` (orchestrator prose).
- The spine OWNS only the interactive, non-safety-critical flow: **CAPTURE**, **CLASSIFY**
  (bias-to-off-ramp, D1), **OFF-RAMP**, routing the **BUILD** to one engine, running the
  **EVIDENCE GATE**, driving **ADJUDICATION**, and the **DOCUMENT** trail.
- The **build** is delegated to nwave (user-facing) or `phil:work` (invisible), and its native
  oracle is **inherited** for the engine-checkable expectations — `/phil:edd` does not re-verify
  them (ADR-005 lineage).
- **Separation of powers is structural**: for each qualitative expectation the spine dispatches a
  dedicated **evidence-producer subagent** (`agents/edd-evidence-producer.md`) — a distinct
  context from the builder — whose sole job is to RUN / RENDER and capture the artifact
  **verbatim** with the command that reproduces it (D2). It does not judge.
- The **human adjudicates** every qualitative expectation via the ADR-002 human-approval port
  (AskUserQuestion + optional IDE review). An **automated evidence critic**
  (`agents/edd-evidence-critic.md`, advisory pre-screen of executed-vs-narration) is **deferred**
  behind a clean seam — the same empirical-design move ADR-002 (deferred test-diff critic) and
  ADR-004 (deferred coverage oracle) made.

## Alternatives considered

- **Pure Workflow-tool cage** (JS owns the loop + gate) — rejected for the same reason ADR-005
  rejected it: CAPTURE/CLASSIFY-confirm/ADJUDICATE are interactive and the oracle is a **human**,
  which fights a headless/background cage; it is also the most new mechanism to build (anxiety B,
  ceremony). Separation of powers does not require the cage — a distinct subagent supplies it.
- **Inline the evidence producer in the spine** (no subagent) — rejected: the builder and the
  evidence-producer would share one context, reintroducing the fox-guarding-the-henhouse problem
  the whole feature exists to solve.
- **Re-implement the engine oracles inside `/phil:edd`** — rejected: violates the ADR-005
  inherit-don't-reimplement principle and duplicates nwave/`phil:work` (DISCUSS anxiety A).

## Consequences

- (+) Faithful to ADR-005: the orchestrator composes; the engines build and gate; `/phil:edd`
  adds only the one gate the engines structurally lack (the qualitative-evidence gate).
- (+) Separation of powers is enforced by context isolation (distinct subagent), not by prose
  promises.
- (+) Least new mechanism; interactive flow stays interactive; matches "piece it together from
  what I've already written."
- (−) The spine is prose (drift risk) — mitigated by `skills/edd/self-test/` fixtures pinning the
  safety-critical behaviors (off-ramp zero-trail, narration rejection, builder≠producer,
  blocked-done), mirroring `work`/`refactor-tests`/`refactor-loop`.
- Open (→ DELIVER): the exact invocation mechanism for the evidence-producer subagent (Agent vs
  Task) and for the engine build — settled empirically by the slice-01 walking skeleton, as
  ADR-005 settled its delegate-invocation question.
