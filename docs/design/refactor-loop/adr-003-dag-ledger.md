# ADR-003: Backlog is a dependency DAG; a reverted prerequisite auto-invalidates dependents

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** state / ledger

## Context

`phil:refactor` treats the backlog as a flat priority-sorted list. gap-memo §complexbench:
a complex instruction composes as And/Chain/Selection/Nested; a failed prerequisite voids
every dependent regardless of local quality (`r'_q = r_q ∧ ⋀ r_p`), and topology-aware
scoring beat flat averaging on human agreement (0.614 vs 0.574). In a loop, when an applied
refactor reverts on red, re-surfacing its dependents wastes iterations and can re-propose
provably-invalid work.

## Decision

Model the backlog as a **dependency DAG**. The `seen/resolved` ledger
(`refactor/ledger.md`) carries **dependency edges** (`depends_on`), not just resolved IDs.
On `REVERT`, the cage walks the transitive closure of the reverted node and sets every
dependent to `invalid`. `PROPOSE` only ever receives `pending` nodes, so invalidated
dependents are never re-proposed.

## Consequences

- (+) No wasted iterations re-proposing work voided by a failed prerequisite.
- (+) The ledger header doubles as the durable pinned-constraint slot (ADR-006).
- (−) Requires the proposer to declare `depends_on` per node; edges may be imperfect —
  acceptable, because the hard gate still catches any bad apply regardless of edge quality.
- Naive decomposition *without* shared state lowered scores (complexbench); the shared
  ledger is exactly that blackboard, so this is positive evidence for the structured-state
  messaging design, not a risk.

## Trace
gap-memo §complexbench.
