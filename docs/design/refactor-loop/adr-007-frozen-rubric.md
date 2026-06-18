# ADR-007: Rubric authored once, frozen, committed, regression-tested on change

**Status:** Accepted
**Date:** 2026-06-17
**Scope:** rubric

## Context

Sage situational-preference fix: critics that re-improvise their standard per call are
order-dependent and inconsistent. gap-memo §eval-driven-iteration: changes to a loop's own
prompts/rubric are **non-monotonic** — a generic "be more helpful" tweak silently cost
−13pp grounding while lifting another axis, invisible without a fixed suite. Autorubric: a
well-formed rubric on the *wrong* construct is confidently wrong.

## Decision

The rubric (`refactor/rubric.md`) is **authored once, frozen, committed, and applied
identically to every proposal**. It is analytic (binary criteria where possible, behavioral
anchors, narrow ordinals, negative-weight anti-patterns, mandatory per-criterion
explanation, `CANNOT_ASSESS` abstention, anti-flattery clause). Two clocks: a **human owns
construct validity** on the slow clock; execution runs on the fast clock. **Every edit to
the rubric is regression-tested against the critic self-test suite (§6.2), never eyeballed.**

## Consequences

- (+) Order-invariant, consistent critic behavior.
- (+) Rubric drift is caught by a regression gate, not discovered in production.
- (−) Slower to evolve the rubric (deliberate — the slow clock is the point).
- The rubric references the existing `rules/*.md` standards + path-scoped idiom files so the
  loop reuses the plugin's single source of coding truth.

## Trace
rgr-loop.md §verdict-schema-and-frozen-rubric; gap-memo §eval-driven-iteration, §advanced-if.
