# Slice 05 — Check the running product with declared sign-in

**Goal (one sentence):** where the work changes a running product, the run checks it in the browser,
signing in from the source the repo declares, and stops when only a person can sign in or nothing is
declared.

Story 5 · Decisions D1, D3.

## IN scope
- Telling whether the work needs the running product, from the path and the card.
- Reading the declared sign-in source; a declaration that a person signs in is a blocker.
- Driving the browser through Chrome DevTools or Playwright, and recording the evidence.
- Fixtures: no declaration blocks only when the running product is needed (AC5.2); a person-signs-in
  declaration blocks (AC5.3); no credential searched for or invented (AC5.4).

## OUT of scope
- Creating test users or tenants; the repo owns them.

## Learning hypothesis
- **Disproves** "a declared source is enough to sign in unattended" if modive's declared test tenant
  still needs a step the run cannot take.
- **Confirms** it if a modive card's in-browser check runs to evidence with no ask.

## Acceptance criteria
AC5.1–AC5.4 in `feature-delta.md`.

## Dependencies
Slice 04.

## Effort estimate
≤1 day. Reference class: `phil:edd`'s evidence producer driving a browser.

## Production data
A modive card that changes a page, and beatrix's "The agent types no credential".

## Dogfood moment
The same day on modive; then confirm beatrix stops on the sign-in.
