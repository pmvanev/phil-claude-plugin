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

### What it measured — 2026-08-13

Thirteen open issues. **Two candidates, both declined, nothing written.**

| Class | Found | Outcome |
|---|---|---|
| Duplicate | 1 — #2 and #3, partial overlap | declined: *leave them apart* |
| Oversized | 0 | — |
| Overcome by events | 0 | — |
| Ungrouped effort | 1 — #4 and #20, the board's only typesetting cards | declined: *leave them ungrouped* |

**The learning hypothesis was answered, and on the branch that needed the design to change.** A partial
overlap *is* presentable — but only because the ask was widened to carry every outcome the evidence
admits. #2 and #3 both add a check to `review-code`'s priority ladder and both leave the same question
open about how a new check earns its tier; put behind *merge? y/n* that finding produces a wrong board
whichever way the user answers, because the real resolutions are *split along the seam* and *dependency
edge* and neither is on a binary menu. **The ask must have the same arity as the finding** — the slice's
central rule, and it came out of this run rather than the brief.

**Both declines invert what the command is for.** The output was not nothing: it was two questions, one
naming a seam the board did not hold. On a board in reasonable shape the deliverable here is the
question and the write is the exception — the opposite of what a section full of merge and split
mechanics suggests. Fixture `21` (*declined leaves no trace*) was written as an edge case and is the
observed common path, which makes the *this will be proposed again* note the sentence most runs end on
rather than a footnote for a rare one.

**One branch of the brief turned out not to exist.** *Ungrouped effort* is written as *join the existing
milestone, or propose creating one*, as though both were shapes of the same offer. Eleven of thirteen
cards carry a milestone, the two that do not are one effort, and no existing container is that goal — so
the live branch was the one the command deliberately **cannot** perform. The tool scoping and the design
agree by accident and now by intent: `gh` has no milestone-create verb, and the `gh api` call that would
do it is not granted. Pinned as fixture `23`, measured rather than constructed.

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
