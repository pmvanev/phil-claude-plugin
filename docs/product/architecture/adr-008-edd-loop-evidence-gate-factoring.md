# ADR-008 — edd-loop: qualitative-evidence gate factoring (inline + extraction seam)

Status: accepted (DESIGN wave, 2026-07-15) · Feature: edd-loop · Resolves DISCUSS D3

## Context

DISCUSS deferred one factoring question to DESIGN (D3): the qualitative-evidence gate — capture a
qualitative expectation, scale the evidence (point at existing engine evidence or commission a new
executed artifact via a non-builder producer), put it to human adjudication, persist the verdict —
is potentially useful beyond `/phil:edd`. `phil:work`'s FRAME §2 currently **refuses** uncheckable
goals (restate-as-metric or drop to preservation-only); the gate is exactly the missing third
option. nwave DELIVER/VERIFY has the same latent need for qualitative expectations its ATs can't
assert. DISCUSS required the gate be **encapsulated so it COULD be shared** and preserve
separation of powers, but left the physical factoring to DESIGN.

## Decision

**Inline the gate in `skills/edd/SKILL.md` as a self-contained section with a defined
input/output contract and a documented extraction seam. Do NOT extract a shared skill in v1, and
do NOT modify `phil:work` or nwave to attach it.**

- The gate is written as one cohesive block of the edd skill with an explicit contract:
  - **input:** `{ expectation, classification, engine_evidence? }`
  - **output:** `{ verdict, evidence_artifact, trail_entry }`
  - **invariants:** evidence is executed-not-narrated (D2); producer ≠ builder (D4); human is
    final adjudicator (D4).
- A short **"Extraction seam"** note records that this block is a candidate for
  `skills/shared/qualitative-evidence-gate.md` once a **second real consumer** exists.

## Alternatives considered

- **Extract `skills/shared/qualitative-evidence-gate.md` now**, attached by `/phil:edd` and later
  by `phil:work`/nwave — rejected: builds a shared abstraction for exactly **one** consumer today.
  That is speculative design, which the plugin explicitly rejects (empirical design over
  speculation; ADR-002/ADR-004 both deferred heavier mechanisms until real usage data existed).
  "Encapsulated so it could be shared" is satisfied by the contract + seam, not by premature
  extraction.
- **Integrate the gate into `phil:work` FRAME now** (offer it as the third option for uncheckable
  goals) — rejected: changes `phil:work` internals, which DISCUSS scoped OUT ("compose the engines
  unchanged"); largest blast radius; couples two features before the gate has proven itself.

## Consequences

- (+) Least new mechanism; fastest to the walking skeleton; no premature coupling into
  `phil:work`/nwave.
- (+) The contract + seam make later extraction cheap and mechanical when a second consumer
  appears (mirrors how `redesign-tests` pattern-copied `refactor-tests` rather than extracting a
  shared loop — ADR-003 Option A).
- (−) When `phil:work`/nwave do want the gate, an extraction step is needed — but the recorded
  contract bounds that work, and doing it then means designing against **two** real consumers
  instead of one imagined one.
- Open (→ future feature): promoting the gate to `skills/shared/` and having `phil:work` FRAME
  offer it as the third option for uncheckable goals — tracked as the post-v1 opportunity in
  `docs/feature/edd-loop/slices/slice-03-cross-domain-sequencing.md`'s neighborhood.
