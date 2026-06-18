# ADR-005: Behavior preservation certified only by the external suite + manifest-vs-actual check

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** safety invariant #1 / hard gate

## Context

A prompt constraint is obeyed only **~80–90%** of the time even when task-specific (gap-memo
§eval-driven-iteration) — defied 1-in-5 to 1-in-10. That residual is exactly the gap a sound
external check must close. The proposer's "I preserved behavior" is a self-report; the
Replit field report (gap-memo §replit-database) is the cautionary tale — a "confession" is
generated text, not an audit trail.

## Decision

The proposer **never self-certifies** behavior preservation. Every iteration:
- the **pre-existing suite** runs externally at `TEST` (Bash, exit code read by the cage);
  red → auto-revert (G3), no LLM in the loop.
- the proposer's **predicted-impact manifest** (`predicted_regressions_risk`,
  `public_api_touched`) is checked against the **actual** test delta + a public-API diff.
  Mismatch → hard revert (G4). The manifest is a measurable contract, never trusted on its
  word.

## Consequences

- (+) Soundness inherited from the hard checker (LLM-Modulo); the ~10–20% prompt-compliance
  residual is covered structurally, not by a better prompt.
- (+) Turns proposer self-justification into a verifiable contract.
- (−) Requires a per-language public-API diff mechanism (open decision §10.8).
- Conjunctive strictness (tests AND types AND no metric regression) belongs to this **hard**
  gate only — never to the soft panel (gap-memo §advanced-if).

## Trace
rgr-loop.md §the-seam, §messaging (predicted-impact manifest); gap-memo
§eval-driven-iteration, §replit-database.
