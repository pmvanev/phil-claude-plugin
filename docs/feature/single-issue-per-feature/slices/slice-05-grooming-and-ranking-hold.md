# Slice 05 — Grooming and ranking hold

**Goal:** Prove the shipped defect oracle needs no loosening under the new paradigm, and land the two
reversals and one divergence that are genuinely required.

**Stories:** S5 (groom without false positives), S6 (rank features)
**Carries:** the `keep-a-backlog-trustworthy` facet.
**Backbone activity:** A7 — keep the board honest.

> **Rewritten by the amendment pass, 2026-08-14.** The first version of this brief proposed changing the
> oversized heuristic and would have caused a defect. See *Changed Assumptions* at the foot of this file.

## Learning hypothesis

**Disproves** the claim that the shipped oracle needs no change — if a correctly-shaped feature card
does produce an oversized finding under the existing definition, the rule really is size-shaped and the
harder problem is back on the table.
**Confirms**, if it holds, that this slice shrinks to two reversals, one divergence, and the fixtures
that keep a future reader from "fixing" a rule that was never broken.

## The rule already holds — this slice proves it rather than changing it

`skills/groom-issues/SKILL.md:268` defines the class:

> **Oversized** — a card carrying work that cannot be demonstrated on its own. Name the seam.

**Demonstrability, not size.** A feature is precisely a thing that can be demonstrated on its own, so a
feature card passes. `phil:issue-board:536-539` agrees, and its second clause is the same premise
correction this feature rests on: *"one issue per thing that can be demonstrated on its own, and split
further only when two halves would sit in different columns at the same time."* Under [D2] — slices
never worked concurrently by different people — one issue per feature is **already compliant with the
shipped rule**.

So the fixture is a **verification**, and it is the durable part of this slice. Without it, the next
reader who sees a large card and an oversized rule in the same file will reconcile them the obvious
wrong way.

## IN scope

- **The verification fixture** — a correctly-shaped feature card produces no oversized finding under the
  existing demonstrability definition, naming the definition it relies on. Plus its opposite: a genuinely
  non-demonstrable card is still caught, seam named. The pair resolves opposite ways.
- **Reversal 1 — session state in a body.** `journeys/groom-issues.yaml` reads, at `scan`: *"An issue body
  contains session state or other scratch → Flag it as a body defect. ADR-013 puts session state in a
  git-ignored local file precisely because a board is world-readable."* Slice 04 deliberately puts
  projected session state there. **Scope the rule, do not delete it:** inside the generated markers it is
  intended; typed scratch outside them is still a defect. Applied to both the skill and the journey, with
  the original quoted.
- **Reversal 2 — rule 4 label families.** Wave-as-column ([D3]) changes what there is to declare, and
  `CLAUDE.md`'s *Issue board* section holds the declaration rule 4 reads.
- **Divergence — `groom-set`'s split means two things now.** `SKILL.md:325-326` says a split's original is
  *"closed as superseded, or kept as the container the new cards hang under."* Here the container **is**
  the feature card and the pieces are **rows**, so splitting a *feature* means re-slicing its roadmap —
  not a board operation. Splitting a *story* still creates cards. The skill must say which it means and
  refuse the other. Nothing currently records this.
- **`rank-issues`** — the ranked unit becomes the feature card. A dependency uncovered while ranking is
  still written as a real forge link, unchanged.

## OUT scope

- **Changing the oversized heuristic.** Explicitly out, and the reason is in *Changed Assumptions*.
- Re-grooming the existing board. This slice changes the oracle's edges; running it is a separate act,
  and consolidating the board is slice 06.
- `groom-issues` slice 04's elicitation work. It lands first ([D11]) and must not be disturbed.
- What a *body* must contain. Rules 1 and 2 are unaffected — a feature card still needs a purpose and a
  done-condition, and the projection supplies neither.

## Acceptance criteria

1. **KPI-4:** `/phil:groom-issues` against the slice-01 card returns zero findings.
2. The verification fixture passes **without any change to the oversized rule's text.** A diff that
   modifies that definition is this slice failing, not succeeding.
3. A card carrying work that genuinely cannot be demonstrated on its own is still reported, with its seam
   named. The pair resolves opposite ways, in the style of 04/11.
4. Typed scratch outside the markers is still a body defect; inside them it is not.
5. The generated region is still refused for editing — the existing error path is untouched.
6. `journeys/groom-issues.yaml` carries the reversal with the original quoted verbatim, per the
   back-propagation contract, and the upstream document is not otherwise modified.
7. The skill states which of the two split operations `groom-set` performs, and refuses the other.
8. `rank-issues` ranks features; no slice card is expected.

## Dependencies

Slices 02, 03 and 04 landed — the oracle's edges cannot be settled against a paradigm that is not yet
asserted, a column family that does not exist, or a projection that carries nothing.

`groom-issues` slice 04 committed ([D11]).

## Effort

~half a day, down from ~1 day. The discriminator that was going to be the work is gone; what remains is
two reversals, one divergence, and three fixtures.

Reference class: the 2026-08-13 rule-4 fold-back, which touched `groom-issues` and `issue-board` together
because one asserted the rule and the other owned the declaration it read. Same shape, with `CLAUDE.md` as
the third party.

## Result — 2026-08-14

**Hypothesis CONFIRMED: the shipped oracle needed no change.** Verified against a live `/phil:groom-issues`
scan at 0.53.0, which reported #26 — the longest card on the board, carrying a generated projection — as
**clean**: no oversized finding, no session-state finding. Both reversals hold against real data, and
**KPI-4 is met on that evidence.**

The oversized rule's text was not modified, which was AC2 and the whole point: a size-keyed reading would
have proposed splitting a consolidated feature every run, and fixture 34 exists to stop a future reader
making it one.

Also landed: the `groom-set` split divergence, `rank-issues`' unit change, and the three deferred follow-ups
— including moving `glab`'s `-O` vs `-F` trap into `phil:issue-board`, where a forge mechanic belongs.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — three fixtures, two prose reversals, one divergence note. |
| Depends on a new abstraction? | No. Consumes the paradigm asserted in 02 and the projection from 04. |
| Disproves a pre-commitment? | Yes — that the shipped oracle needs no change. Cheap to test, and it already caught one wrong answer. |
| Synthetic data only? | No. The oracle runs against this repo's real board, including the slice-01 card. |
| Duplicate of another slice at scale? | No. 06 changes which cards exist; this changes what the oracle says about them. |

## Changed Assumptions

**Original, quoted verbatim from this brief's first version** (`slice-05-grooming-and-ranking-adapt.md`,
2026-08-14, earlier the same day):

> The oversized heuristic gains the structured/unstructured discriminator, with the reasoning.

**New assumption.** The rule is demonstrability-based, not size-based, so a feature card already passes
and no discriminator is needed. This slice verifies the rule rather than modifying it, and AC2 makes a
diff to that definition a failure.

**Full rationale — including why the proposed change was the mechanism of the oscillation defect, and how
this feature's own `jobs.yaml` anxiety (F) predicted it four files away —** is in
`../feature-delta.md` under *Changed Assumptions — amendment pass*, change 1. Recorded there rather than
restated here: one account of one correction.
