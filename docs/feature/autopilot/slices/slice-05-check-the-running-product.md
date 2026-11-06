# Slice 05 — Dogfood the running product without the developer

**Goal (one sentence):** where the work changes a running product, the run works out from the repo how
to walk the change in a browser and walks it, and stops only when it finds no way, suggesting one.

Story 5 · Decisions D1, D3 (revised 2026-11-06).

## IN scope
- Telling whether the work changes a running product, from the card and the work.
- Reading how the repo dogfoods itself: `CLAUDE.md`, `AGENTS.md`, the README's dogfood and
  local-development sections, test-user docs, dogfood and dev scripts.
- Taking the first way that works: the repo's dogfood steps and test accounts; the product run locally;
  any other way. Driving the browser through Chrome DevTools or Playwright, and recording the walk.
- A blocker, when no way works, that suggests documenting an automatic way forward.
- All of it as prose in `references/run.md`; no hook and no script (the developer, 2026-11-06).
- Fixtures 35 to 40: the repo's dogfood command (AC5.1, on GitLab); a test account named, never its
  secret (AC5.1, AC5.4); a local run (AC5.2); no way found (AC5.3); no running product (AC5.2); a repo
  rule that binds one browser and not another (D3).

## OUT of scope
- Creating test users or tenants; the repo owns them.
- Filing the suggested documentation as a card; it stays in the blocker comment.

## Learning hypothesis
- **Disproves** "the repo's own docs are enough to dogfood unattended" if a modive or beatrix card's
  walk still needs a step the run cannot take.
- **Confirms** it if a modive card's walk runs to evidence with no ask.

## Acceptance criteria
AC5.1–AC5.4 in `feature-delta.md`.

## Dependencies
Slice 04.

## Effort estimate
≤1 day. Reference class: `phil:edd`'s evidence producer driving a browser.

## Production data
modive's and beatrix's fixture-served dogfood commands; beatrix's dev test accounts; modive's test
tenant; submission-tracker, whose only sign-in is a person's own account.

## Dogfood moment
A modive card that changes a page, on the plugin version that ships this slice.
