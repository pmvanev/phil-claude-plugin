# Slice 02 — `ui.md` mobile aesthetic guardrails

**Goal.** Add a short mobile-guardrails note to `rules/ui.md` so its aesthetic advice
(glassmorphism, heavy micro-animations, "wow at first glance") is scoped for mobile and stops
implicitly pushing desktop-only polish.

**Story:** US-02 · **Job:** catch-ux-violations-while-building-ui (mobile facet)

## IN scope
- ≤ ~8-line note in `ui.md` covering: honour `prefers-reduced-motion`; heavy-effect performance on
  constrained devices; small-screen type/contrast legibility.
- Keep the note within `ui.md`'s aesthetics remit — guardrails, not usability rules.

## OUT scope
- Any usability/a11y content (that's `ux.md`, Slice 1) — no duplication.
- Adding a `/phil:ui-review` command — `ui.md` stays passive.
- Measured performance budgets or tooling.

## Learning hypothesis
Disproves "mobile aesthetic guardrails fit in `ui.md` without crossing into `ux.md`'s usability
remit" **if** review finds the note restating usability/a11y items rather than qualifying aesthetics.

## Acceptance criteria
See US-02 ACs in `feature-delta.md`. Boundary check: no verbatim overlap with `ux.md`/`react.md`.

## Dependencies
- Independent of Slice 1 in code (different file), but conceptually paired; author after Slice 1 so
  the ux/ui boundary is fresh. Research precursor (D1) informs the perf/legibility wording.

## Effort / reference class
≤ 0.5 day. Reference class: `ui.md` is ~23 lines today; this is a small additive note.

## Pre-slice SPIKE
None.
