# ADR-002: Single correctness critic in v1; disjoint panel is earned, not default

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** subagents / review stage

## Context

Two forces (rgr-loop.md §critic-panel). Heterogeneous independent critics beat a single
judge (CollabEval/Sage/judge-debate). But AHE non-additivity: +11pp single-component gains
collapsed to +7pp combined — *"a cage has a coordination budget; past it, more controls
subtract."* "Most coding tasks don't need a 5-reviewer panel" (dynamic-workflows).

## Decision

v1 ships **proposer + one separate `refactor-critic-correctness`** through the hard gate.
The disjoint-rubric panel (idiom + architecture critics, CollabEval 3-phase, collaborative
never adversarial, hard-critic tiebreak) is **v2**, promoted **only when the single critic
demonstrably misses a class of problem** — established via the §6.3 human spot-check showing
a recurring miss category, not speculation.

## Consequences

- (+) Lowest token cost that still decorrelates judgment (proposer ≠ critic — LLM-Modulo:
  self-verification lowers accuracy; tri-agent = correlated errors).
- (+) Avoids spending the coordination budget before it's needed.
- (−) v1 may miss idiom/architecture smells the correctness rubric doesn't cover — accepted,
  and explicitly the measured trigger for v2.
- Tiebreak (v2) routes to the **hard critic** (tests + metric deltas), never a bigger model
  (which inherits the panel's bias).

## Trace
rgr-loop.md §critic-panel, §component-map (separate proposer from critics); gap-memo
§advanced-if (soft judge F1 0.728 → brittle as a runtime conjunction).
