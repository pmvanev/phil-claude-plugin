# Slice 01 — `ux.md` mobile/responsive tier

**Goal.** Add a mobile/responsive tier to `rules/ux.md` so reflow, zoom, orientation, pointer-gesture,
and motion-actuation defects are flagged in-flow with the preferred form. *(Walking-skeleton slice.)*

**Story:** US-01 · **Job:** catch-ux-violations-while-building-ui (mobile facet)

## IN scope
- New mobile/responsive block inside `ux.md`'s existing two-tier structure.
- Always-flag items (WCAG-cited): reflow @320px/400% (1.4.10), resize text 200% (1.4.4),
  orientation lock (1.3.4), path/multipoint gesture w/o single-pointer alt (2.5.1), motion
  actuation w/o control alt (2.5.4).
- Advisory sub-tier: thumb-reach, hover-on-touch affordance, on-screen-keyboard obscuring inputs.

## OUT scope
- Touch-target size (already at `ux.md:27` — do not duplicate).
- `ui.md` aesthetic guardrails (Slice 2); `/phil:ux-review` update (Slice 3).
- Native app UI; CI enforcement.

## Learning hypothesis
Disproves "mobile always-flag items can be stated crisply in react.md voice within ~15 lines
without false-flagging responsive judgment calls" **if** the dogfood fixture yields any false
always-flag on an intentionally-responsive-dense screen, or the addition blows the length ceiling.

## Acceptance criteria
See US-01 ACs in `feature-delta.md`. Dogfood: 5/5 mobile defect classes surfaced; 0 false
always-flag on a responsive-dense fixture.

## Dependencies
- **Precursor commit:** `docs/research/ux/mobile-web-best-practices.md` (D1).
- Parent `rules/ux.md` two-tier structure must exist (it does).

## Effort / reference class
≤ 1 day. Reference class: the parent `ux-standards-rule` US-01 (author a tier in an existing rule).

## Pre-slice SPIKE
None — WCAG SC are known; research precursor removes the remaining uncertainty.
