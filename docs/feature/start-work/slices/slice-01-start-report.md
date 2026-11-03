# Slice 01 — The start report

**Goal (one sentence):** `/phil:start <card>` resolves the argument to one open card, applies the
refusals, describes the card and recommends a route, writing nothing.

Stories 1 and 2 · Decisions D4, D6, D7, D9, D10.

## IN scope
- `commands/start.md` (`mutates: true`, D11) and `skills/start/SKILL.md`, after reading
  `plugin-dev:command-development` and `plugin-dev:skill-development`.
- Resolution: a number directly; a title or description searched against open cards; several matches
  listed for the developer to pick; none reported, with filing offered and deferred to slice 02.
- Refusals: a closed card; an open card in Done; a card assigned to another account.
- The description — asks, done-when, open questions — drawn from the card, with `phil:groom-ask`
  named when the card says too little.
- The route: the repo's recorded build path first, then the wave label and nWave artifacts, then
  visible versus invisible work, then size. Named with its reason and owning command; launched only on
  a yes.
- The report, composed to `rules/writing.md`, with the citation's test watched failing first.
- Fixtures: several matches; no match; a closed card; an open card in Done; another's card; a card
  with no done-when; a repo build path that overrides the default route.

## OUT of scope
- Any write to the forge or the disk (slices 02 and 03).

## Learning hypothesis
- **Disproves** "the card and the repo's CLAUDE.md are enough to choose the route" if, on a real card,
  the developer overrides the recommendation for a reason neither records.
- **Confirms** it if the developer takes the recommendation on two real cards.

## Acceptance criteria
AC1.1–AC1.4 (AC1.2's filing is checked in slice 02), AC2.1–AC2.4 in `feature-delta.md`.

## Dependencies
None.

## Effort estimate
≤1 day. Reference class: `finish-work` slice 01, a read-only report.

## Production data
Issue 80 itself, and the open Todo cards on this board.

## Dogfood moment
The same day, run `/phil:start /phil:autopilot` on this branch: it should resolve to issue 76, describe
it, and recommend `nw-discuss` from this repo's CLAUDE.md.
