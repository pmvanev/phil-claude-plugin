# Slice 01 — The ready-to-close report

**Goal (one sentence):** `/phil:done <card>` lists every ask with its evidence and says whether the
work has landed, writing nothing.

Stories 1 and 2 · Decisions D1, D2, D6.

## IN scope
- `commands/done.md` (`mutates: true`, D10) and `skills/done/SKILL.md`, after reading
  `plugin-dev:command-development` and `plugin-dev:skill-development`.
- Asks from the card's checklist and *Done when* items plus the current session's requests and tasks;
  each marked done with evidence, or open. A sentence is not evidence.
- Landed: every pull request found for the card merged, and the default branch's pipeline green at or
  after the last merge; `no pipeline` where there is none.
- The report, composed to `rules/writing.md`, with the citation's test watched failing first.
- Fixtures: an open ask; a narrated-only ask; an open pull request; a red main; no pipeline.

## OUT of scope
- Any write to the forge or the disk (slices 02 and 03).

## Learning hypothesis
- **Disproves** "the card plus the session is enough to find every ask" if, run on a real card, the
  developer names an ask the report missed.
- **Confirms** it if the developer adds nothing to the list on two real cards.

## Acceptance criteria
AC1.1–AC1.4 (AC1.4's comment is checked in slice 02), AC2.1–AC2.4 in `feature-delta.md`.

## Dependencies
None.

## Effort estimate
≤1 day. Reference class: `board-snapshot` slice 01, a read-only report.

## Production data
Issue 75 itself, and one closed card from this board replayed as if open.

## Dogfood moment
The same day, run `/phil:done 75` on this branch: it should report the DISCUSS pull request open and
the card's checklist items open.
