# Slice 05 — Grooming and ranking recognise the story

**Goal:** Stop the silent failure. Make `groom-issues` pass a correct story card, report the one shape
that is genuinely wrong, and offer a story card where it would have offered a milestone; make
`rank-issues` know that the ranked unit is the card.

**Stories:** S4 (groom without false positives, and catch the real defect), S5 (rank a board whose unit
may be a story), S6 (tell a story from a goal on sight — the prose half)
**Answers:** issue #36's question 4, and its *"Plus"*

## Learning hypothesis

**Disproves C10** — *extend a shipped oracle at the new scale, never loosen it* — if the only way to make
grooming see a story card is to weaken the demonstrability rule. That is the `keep-a-backlog-trustworthy`
anxiety (F) firing: *"An oracle loosened to stop the false positives stops catching the real ones."* If
it fires, the story tier has bought a worse board.
**Confirms**, if it passes, that a vacuously-passing rule is closed by adding a rule that fires, not by
adjusting the one that passes.

## IN scope

### `groom-issues` / `groom-set`

- **The oversized paragraph is extended, not edited** ([D13]). A story card is large, holds several
  demonstrable things, and passes. The `Do not "fix" this rule toward size` sentence gains the story
  case, with the same oscillation reasoning: the family stores no marker, so a declined split returns
  forever and only has to be accepted once.
- **New set-level signal: two features in flight on one story card** ([D12]). Evidence is the fold's
  output and the block's two `▶` rows, quoted. Resolution offered: split into feature cards under a
  goal. Derived from `issue-board:616-625`'s concurrency reading — **not a new granularity rule.**
- **New set-level class: features of one story, carded separately.** Directly parallel to the shipped
  *decomposed feature* class, one level up, and it **supersedes *ungrouped effort* the same way** —
  that class proposes a milestone, which is a goal, where the right container is a story card. Evidence
  ranked as decomposed-feature's is: a `Story:` line in the deltas, **confirmed present in the repo** with
  `git ls-tree`, licenses an offer; a shared title prefix licenses a report only.

### `rank-issues`

- **The ranked unit is the card: a feature or a story.** A story holds one position; its member features
  hold none.
- **The stop condition narrows to slice cards.** A story card does not stop the session.
- A story card and a member-feature card both open: say so and stop, naming `/phil:groom-set`. **Reuses
  grooming's oracle rather than duplicating it** — two detectors over one defect drift.

### The discriminator ([D5], story S6)

Stated where a reader meets it, in one sentence each: **a goal holds cards; a story holds feature
directories.** In `issue-board` beside *a milestone is a goal*, and in `groom-issues` at the
ungrouped-effort supersession. Milestones do not nest; a story is not a milestone; neither replaces the
other.

## OUT scope

- Migrating any existing card. There are no multi-feature cards on this board to consolidate, and
  retro-consolidating closed ones is refused in the delta.
- A `check-invariants.py` validator for the membership declaration. Named as a candidate; a script is not
  this feature's deliverable.
- Any loosening of the demonstrability rule. If that becomes necessary, this slice has failed.

## Acceptance criteria

1. **KPI-4, both sides, pinned by an adjacent fixture pair that resolves opposite ways** — in the style
   of 04/11: a correctly-shaped story card produces **zero** findings; a two-in-flight story card
   produces **one**, quoting both feature names. Getting one right by a rule that gets the other wrong is
   a gate failure.
2. No oversized finding and no split proposal against a correct story card, **verified without modifying
   the rule's demonstrability text**.
3. Several cards that are features of one story are reported as a set, and the offered container is a
   story card — never a milestone. A fixture pins the milestone offer as wrong.
4. `/phil:rank-issues` ranks a board holding a feature card and a story card without stopping, and gives
   each exactly one position.
5. `/phil:rank-issues` **does** stop on a slice card, unchanged.
6. **KPI-5's prose half:** the discriminator sentence appears in both surfaces, and a reader applying it
   to slice 01's card and its goal gets the right answer.
7. Every never-do list that mentions the feature card is checked for whether it now needs to mention the
   story card. A never-do that names one tier and not the other is read as permission at the unnamed one.

## Dogfood moment

Run `/phil:groom-issues` against the real board after slice 01's card exists. **The predecessor measured
this and the number was zero findings on a clean board** — so the informative outcome here is whether the
new check fires when it should, which needs a deliberately wrong card. Build one, scan it, close it.

## Dependencies

- Slices 02, 03 and 04 — the fold, the block and the label are what the new checks read.
- Slice 01's card, as the real correct-shape input.

## Effort

~1-1.5 days. Reference class: the predecessor's slice 05, which verified two shipped oracles held and
reversed one journey rule, at ~1.5 days.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | Three surfaces — `groom-issues`, `groom-set`, `rank-issues` — plus one sentence in `issue-board`. **Over the one-day test at ~1.5 days**, and kept whole because a check and the fixture that would have caught its absence must ship together, per this repo's fold-back rule. Stated as a failed test, not rounded off. |
| Depends on a new abstraction? | On 02-04, all shipped by then. |
| Disproves a pre-commitment? | Yes — that shipped oracles need only extension, not loosening. |
| Synthetic data only? | No — the real board for the clean case, one deliberately-wrong card for the firing case. |
| Duplicate of another slice at scale? | No. Every other slice makes the card *readable*; this makes the board *honest about it*. |
