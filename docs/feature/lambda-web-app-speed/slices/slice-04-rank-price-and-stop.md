# Slice 04 — Rank the fixes, price the warmth, draw the line

**Goal.** The skill ranks fixes on the measured path, prices the warmth options for the app's own
traffic, measures a browser load, and stops at the target.

**Story:** US-04 · **Job:** make-a-lambda-web-app-load-fast

## IN scope
- Ranking by saving per unit of effort, the standard pattern first among equals (D13).
- Pricing provisioned concurrency, SnapStart and a heartbeat from the app's invocation counts, with
  partition availability checked (D9).
- A browser trace for TTFB and LCP; the stopping line against D16's targets.
- The rule's remaining Principles (INIT budget, warmth, static assets, the bundle, cached views) and its
  Advisory list, bytecode included (D7, D9, D11). V3 closed first.

## OUT scope
- Fonts, LCP images, preload and the sign-in chain (D15).

## Learning hypothesis
Disproves "saving per effort from measurements orders fixes the way their real gains fell" **if** the
replay of beatrix 254 leaves any of its three largest measured gains outside the top three.

## Acceptance criteria
See US-04 in `feature-delta.md`.

## Dependencies
- Slice 03.

## Effort / reference class
≤ 1 day. Reference class: `build-ci --speed`'s ranking and stopping line.

## Production data
beatrix 254's recorded measurements replayed in order; one browser trace of a real deployed app.
