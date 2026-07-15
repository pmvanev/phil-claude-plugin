# ADR-009 — edd-loop: documentation namespace and trail schema

Status: accepted (DESIGN wave, 2026-07-15) · Feature: edd-loop · Resolves DISCUSS D5

## Context

`/phil:edd` must persist captured expectations, the executed evidence, and the human verdicts as
living documentation (DISCUSS D5) — but only when the evidence gate actually ran (an off-ramp-only
run must leave **no** trail, per the zero-ceremony KPI). The repo already namespaces per-feature
nwave work under `docs/feature/<id>/`, invisible-initiative work under `docs/work/<initiative>/`
(ADR-006), and durable summaries under `docs/evolution/`. DESIGN must place the edd trail without
colliding.

## Decision

**Working trail under a new `docs/edd/<slug>/`; durable summary migrates to `docs/evolution/`.**

Per intent slug (kebab-case of the intent), created **only when the evidence gate ran**:

```
docs/edd/<slug>/
  expectations.md   # each captured expectation + classification + routing (engine | qualitative)
  evidence/         # the captured EXECUTED artifacts (verbatim), one per qualitative expectation
  verdicts.md       # per-expectation human verdict (accept/reject) + timestamp + evidence ref
docs/evolution/<date>-<slug>.md   # durable summary: expectations, verdicts, evidence pointers
```

- `docs/edd/` is transient working state for an in-flight or recently-finished loop.
- An **off-ramp-only** run writes nothing here — the recommendation is delivered in-session and the
  run exits (zero-ceremony KPI).
- On completion with ≥1 adjudicated qualitative expectation, `/phil:edd` writes the evolution
  summary to `docs/evolution/`, reusing the plugin's established convention (as ADR-006 does).

## Alternatives considered

- **Reuse `docs/work/<slug>/`** (phil:work's namespace) — rejected for the same reason ADR-006
  rejected reusing `docs/feature/`: it conflates expectation-evidence loops with behavior-
  preservation initiatives; a reader could not tell an `/phil:edd` run from a `/phil:work` one.
- **Reuse `docs/feature/<id>/`** — rejected: treads on nwave's namespace; edd runs are not nwave
  features.
- **Keep the durable summary inside `docs/edd/` too** — rejected: breaks the repo's single
  `docs/evolution/` history convention (same call ADR-006 made).

## Consequences

- (+) Clean, self-documenting separation from nwave (`docs/feature/`) and `phil:work`
  (`docs/work/`); three sibling namespaces, one per orchestrator.
- (+) Durable history stays consolidated in `docs/evolution/`.
- (+) The gate-ran-only rule makes "did this run add ceremony?" observable as a filesystem fact
  (trail dir exists ⇔ the gate ran), which the zero-ceremony KPI asserts.
- (−) A third `docs/*/` orchestrator namespace to learn — mitigated by the parallel structure
  (expectations/evidence/verdicts mirrors work's frame/roadmap/decisions/progress).
- Open (→ DELIVER): git-ignore `docs/edd/` while in flight vs commit per adjudication — deferred,
  leaning committed (matching ADR-006's lean and the delegates' per-item commit discipline).
