# Slice 03 — Set-level operations, all ask-first

Feature: groom-issues · Job: `keep-a-backlog-trustworthy` · Persona: `robin-backlog-curator`

## Goal

Resolve the defects that live between issues — duplicates, oversized cards, work overcome by events,
ungrouped effort — with every decision made by the human.

## Learning hypothesis

**Disproves that set-level defects are detectable with actionable evidence.** Exact restatement is
easy; the real case is two issues that overlap in part. If the session cannot present a partial
overlap in a form the user can decide on, then set-level grooming is guesswork wearing a report's
clothes, and the honest move is to drop it.

**Confirms** that the cross-issue pass earns its separate phase — that a comparison across the whole
set finds what no per-issue read can.

## IN scope

- **Duplicates** — surface the pair with the overlapping content quoted. On approval: merge detail
  into the survivor, close the other pointing at it, re-point references to the closed one.
- **Oversized** — surface the card and the seam, per `phil:issue-board`'s *Choosing what becomes an
  issue*. On approval: split, which is bulk seeding and therefore a **second pass** for the
  cross-references between the new cards.
- **Overcome by events** — surface the evidence that the work landed another way or the decision was
  reversed. On approval: close with the reason in a comment.
- **Ungrouped effort** — surface a card belonging to a larger effort with no container. On approval:
  join the existing milestone/feature, or propose creating one. Consumes #7's convention (**a
  milestone is a goal**) rather than inventing a second one.
- **A declined candidate leaves no trace**, and the report says it will be proposed again next run.

## OUT scope

- Applying any of the four without asking (C2). This is the slice's whole discipline.
- Inventing a container convention — #7 owns it.
- Ranking the survivors — `phil:rank-issues` owns it.

## Acceptance criteria

1. Given two overlapping issues, when the candidate is surfaced, then the overlapping content is
   quoted from both and the user is asked.
2. Given approval to merge, then detail moves to the survivor, the other is closed pointing at it,
   and references to the closed issue are re-pointed.
3. Given approval to split, then the new cards are created first and their cross-references written
   in a **second pass**, because numbers are assigned at creation.
4. Given a declined candidate, then nothing is written and the report states it will reappear next
   run — the accepted cost of storing no marker (D6/C1).
5. Given an ungrouped card, when a container is proposed, then it follows #7's milestone-is-a-goal
   convention.
6. Given any of the four, then **nothing is applied before an explicit answer**.

**Production data:** this repo's real board.

## Dogfood moment

Same day: run it here. #5's own chain notes it shares design context with #6 and #7 — genuine
overlap between real cards, which is the partial-overlap case rather than the easy one.

## Dependencies

**Slice 01** — consumes its set-level candidates. Independent of slice 02.

## Effort and reference class

≤1 day, and the highest-uncertainty of the three. Reference class: `phil:redesign-tests` — a
per-item, human-approved loop where each application is behaviour-changing and expensive to undo.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — four candidate handlers sharing one ask-then-apply loop. |
| Depends on a new abstraction? | Consumes slice 01's candidates and #7's milestone convention. |
| Disproves a pre-commitment? | Yes — that partial overlap can be presented decidably. |
| Synthetic data only? | No. |
| Duplicate of another slice at scale? | No. |
