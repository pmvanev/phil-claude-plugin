# ADR-006 — phil-work: documentation namespace and trail schema

Status: accepted (DESIGN wave, 2026-07-13) · Feature: phil-work

## Context

`/phil:work` must leave a decision/progress trail (DISCUSS D8, deferred to DESIGN). nwave writes
per-feature artifacts under `docs/feature/<id>/`, and durable evolution summaries already live in
`docs/evolution/` (e.g. `docs/evolution/2026-07-02-refactor-tests.md`). DESIGN must pick where an
initiative's trail lives without colliding with nwave's namespace.

## Decision

**Working trail under a new `docs/work/<initiative>/`; durable evolution summary migrates to
`docs/evolution/`.**

Per initiative slug (kebab-case of the FRAME goal):

```
docs/work/<initiative>/
  frame.md       # goal metric, preservation contract, IN/OUT scope, chosen oracle
  roadmap.md     # ordered waves; per wave: change, delegated skill, gate
  decisions.md   # decision log (why each wave, routing/oracle choices, deviations)
  progress.md    # per-wave status + commit shas — also the resume source
docs/evolution/<date>-<initiative>.md   # durable summary: what changed, why, outcome vs goal
```

- `docs/work/` is transient working state for an in-flight or recently-finished initiative.
- On VERIFY completion, `/phil:work` writes the evolution summary to `docs/evolution/`, reusing
  the convention the plugin already established at finalize.

## Alternatives considered

- **Reuse `docs/feature/<initiative>/`** — rejected: conflates invisible technical work with
  user-facing features and treads on the namespace nwave owns; a reader could not tell an
  `/phil:work` initiative from an nwave feature.
- **Keep the evolution summary inside `docs/work/` too** — rejected: breaks the repo's existing
  `docs/evolution/` convention and scatters durable history.

## Consequences

- (+) Clean separation from nwave features; self-documenting namespace.
- (+) Durable history stays in one place (`docs/evolution/`), consistent with prior features.
- (+) `progress.md` doubles as the resume source for an interrupted multi-wave run.
- (−) Two locations per initiative (working vs durable) — mitigated by writing the evolution
  summary only once, at VERIFY, as the last step.
- Open: whether `docs/work/<initiative>/` should be git-ignored while in flight or committed
  per wave — deferred to DELIVER (leaning committed-per-wave, matching the delegates' per-item
  commit discipline).
