# Slice 02 — Single-engine qualitative-evidence gate

**Goal (one sentence):** When some expectations are genuinely qualitative, `/phil:edd` delegates
the build to ONE engine, then attaches a scaled EXECUTED-evidence gate to the qualitative residue
that the developer adjudicates — and persists expectations + evidence + verdicts as living docs.

**WS strategy:** B — extends the skeleton's qualitative branch end-to-end on one engine.

## IN scope
- BUILD-VIA-ENGINE: route the build to one engine (nwave user-facing / phil:work invisible),
  inheriting its native oracle for the checkable expectations (no re-verification — ADR-005).
- SCALED EVIDENCE GATE for each qualitative expectation:
  - if the engine already produced relevant executed evidence → point at it (near-zero cost);
  - else COMMISSION a new executed artifact (real run/render, captured verbatim + reproducing
    command) from an agent that is **not** the builder (separation of powers).
- NARRATION REJECTION: evidence without a raw reproducible artifact is rejected + re-commissioned.
- ADJUDICATE: human accepts/rejects each qualitative expectation on the evidence; a rejection
  blocks "done" and iterates.
- LIVING DOCS: persist `docs/edd/<slug>/` (expectations, `evidence/`, verdicts) + evolution summary.
- Self-test fixtures: (a) evidence-already-exists path, (b) commission-new path, (c) narration
  rejected, (d) builder≠evidence-producer enforced, (e) rejected expectation blocks done.

## OUT of scope
- Cross-domain multi-initiative sequencing + seam-level expectations (slice 03, deferred).
- An AUTOMATED independent-critic *verdict* on qualitative evidence — v1 keeps the human as final
  adjudicator; an advisory pre-screen seam may be reserved (mirrors refactor-tests' deferred critic).
- Extracting the gate into a shared skill both engines attach (DESIGN factoring decision).

## Learning hypothesis
- **Disproves** "the gate is either ceremony or a rubber stamp" if it can't scale to near-zero
  when evidence already exists, or if narrated evidence slips through.
- **Confirms** the qualitative gate adds real, non-redundant value if a qualitative expectation
  is adjudicated on an executed artifact the engine alone would never have surfaced.

## Acceptance criteria
- Given a qualitative expectation and an engine that already produced relevant executed evidence,
  when the gate runs, then it points me at the existing artifact (no new commission) and asks me
  to adjudicate.
- Given a qualitative expectation with no existing evidence, when the gate runs, then it
  commissions a NEW executed artifact produced by a non-builder agent, captured verbatim with the
  command that reproduces it, and presents it for adjudication.
- Given "evidence" that is narration (no raw artifact / not reproducible), when validated, then it
  is rejected and re-commissioned — narration never satisfies the gate.
- Given I reject a qualitative expectation, then "done" is blocked, the expectation iterates, and
  the run is never reported as done with an outstanding rejection.
- Given completion with ≥1 adjudicated qualitative expectation, then `docs/edd/<slug>/` holds
  expectations + evidence artifacts + verdicts, and `docs/evolution/<date>-<slug>.md` is written.

## Dependencies
Slice 01. Reuses: ADR-002 human-approval port; ADR-004 human-validated-claim pattern
(redesign-tests); refactor-loop's independent-critic pattern; ADR-006 doc-namespace pattern.

## Effort estimate
≤1 day per sub-path; may split commission-new vs evidence-exists if the crafter dispatch exceeds 6h.

## Production data
Adjudicate a real qualitative expectation (e.g. actual CLI error output on this plugin), not synthetic.

## Dogfood moment
Run `/phil:edd` on a real intent containing "error messages should be helpful" and adjudicate the
captured transcript the same day.
