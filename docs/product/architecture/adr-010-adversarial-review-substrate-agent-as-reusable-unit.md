# ADR-010 — adversarial-review: prose spine + agent-as-reusable-unit; standalone-only in v1

Status: accepted (DESIGN wave, 2026-07-15) · Feature: adversarial-review

## Context

`/phil:adversarial-review` is a general-purpose independent critic: point it at a completed task and
it returns ranked, evidence-bearing findings. DISCUSS (D1–D6, constraints C1–C5) requires it to run
**standalone** AND be **composable** into other commands (`phil:work`, `phil:edd`,
`phil:refactor-tests`) and ad-hoc Workflow scripts, while never self-adjudicating (C3) and staying
independent of the builder (C1). The repo already contains the DNA: `refactor-critic-correctness`
(an independent, advisory, span-and-evidence critic agent reused by `refactor-loop`), the ADR-005
"inherit the oracle, never re-implement" lineage, and ADR-008's "don't extract a shared abstraction
for one consumer" discipline.

DESIGN must fix (a) the substrate, (b) what the reusable unit is, and (c) how far composition goes
in v1.

## Decision

**A prose-skill spine drives a Task-dispatched reviewer subagent; the AGENT is the reusable unit;
v1 ships standalone only and publishes the composition contract as documentation — it edits no
existing skill.**

1. **Substrate = prose spine + subagent** (not a Workflow cage). adversarial-review is a single
   dispatch → verdict and is **advisory** (C3): there is no loop to bound and no safety-critical
   gate for prose drift to weaken. `commands/adversarial-review.md` (thin loader) +
   `skills/adversarial-review/SKILL.md` (spine: frame → curate independent input → dispatch →
   present) is the least-new-mechanism fit, mirroring edd / work / refactor-tests. Independence
   (C1) is achieved by the subagent = fresh context; the spine curates its input to the artifact +
   intent + standards and **withholds the builder's reasoning trace**.
2. **Reusable unit = `agents/adversarial-reviewer.md`.** One agent definition, invoked by the
   standalone skill AND by any future host / workflow (via Task / `agent()`), all reading the same
   **typed verdict**. The agent is substrate-agnostic; the skill is only the standalone human driver.
   This mirrors how `refactor-critic-correctness` is the reusable unit `refactor-loop` composes.
3. **v1 scope = standalone only; composition is a documented contract, not wiring.** The agent
   publishes a typed input/output contract (`{target, intent, standards}` → typed verdict) and the
   skill documents the ad-hoc Workflow-weaving pattern. **No existing skill is modified.** Hosts
   adopt the contract later, each as its own work, once a real second consumer exists.

## Alternatives considered

- **Workflow-tool cage** (like `refactor-loop`) — rejected: no loop/gate to make deterministic; the
  interactive standalone use and advisory nature fight a headless cage; most new mechanism to build.
- **Shared skill `skills/shared/adversarial-review.md`** — rejected: the agent already IS the
  natural reuse unit (schema = contract), so a shared skill adds a layer with no consumer today.
- **Wire `phil:work` (and others) to consume the verdict now** — rejected on the same grounds
  ADR-008 rejected touching `phil:work` from edd: it edits another feature's internals, is the
  largest blast radius, and couples two features before the critic has proven itself. The user
  explicitly scoped host edits OUT (2026-07-15).
- **Inline the critic in each consumer** — rejected: guarantees duplication and drift across
  consumers; the whole point is one independent reviewer.

## Consequences

- (+) Standalone value ships first; composition is enabled (clean typed contract + independently
  invocable agent) without any cross-feature coupling. Adoption later is cheap and mechanical.
- (+) One reviewer definition — no duplication, consistent verdicts wherever invoked.
- (+) Faithful to ADR-005 (inherit oracle) and ADR-008 (second-consumer rule).
- (−) The spine is prose (drift risk), but it holds no safety-critical gate (reviewer is advisory),
  so drift cannot silently weaken a guarantee. A `self-test` harness (author-then-ablate golden
  bad tasks) pins the reviewer's C1–C5 behaviors as a regression gate.
- (−) **Accepted v1 risk (reviewer independence):** a same-model, fresh-context subagent is not
  *fully* independent — a blind spot shared by builder and reviewer can survive (the tri-agent
  correlated-error caveat; tri-agent framework = Zhao, KDD '25, read via the harebrain summary
  `docs/research-summaries/tri-agent-clarification/` in the sibling `harebrain` repo). v1 accepts
  this (isolation is the cheapest real independence);
  different-model and multi-lens-panel hardening are recorded as an **extension seam** (trivial to
  add when composed into a Workflow via `parallel()`), designed against real data rather than
  speculation. Mirrors edd's D7 accepted-risk posture.
