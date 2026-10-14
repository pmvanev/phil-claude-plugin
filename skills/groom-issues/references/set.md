# Resolving the set-level candidates — `/phil:groom-set`

Part of the `groom-issues` skill. `SKILL.md` governs this command as much as this file does: the
standard, the scan, the defect table, the cross-issue candidates, reporting, the decision outcomes and
the invariants all apply here.

The operations in `SKILL.md`'s *Cross-issue candidates* are the only ones here, and each asks. What
follows is what the question must contain to be answerable, and what the apply owes afterwards.

**The ask must have the same arity as the finding.** This is the rule the whole step turns on. Two
issues that overlap in part are not a yes-or-no about merging: they may be a merge, a split along the
seam, a dependency edge, or two cards that happen to share a mechanism and should stay apart. Offering
*merge? y/n* over that finding forces a wrong answer, and a declined merge then reads as *these are
unrelated*, which was never asked either. Present the outcomes the evidence actually admits, and let *leave them alone* be one of them.

**Evidence is quoted, not characterised.** "These look similar" is the finding restating its own
conclusion. Quote the overlapping content from both bodies, then say in one line what is shared and
what is not. The difference is what the user is adjudicating.

**One candidate at a time, re-derived, not carried.** An apply here changes the set the remaining
candidates were computed over: a merge closes a card a later candidate names, a split assigns numbers
no earlier read could have seen. `SKILL.md`'s *re-read a card immediately before writing it* holds for
every card this command edits, including a merge's survivor, and one level up as well: re-read the
board between candidates, and drop any whose subject a previous apply has already moved.

## Merge

**Which card survives is the user's choice, not the lower number.** Age correlates with
nothing that matters here. Ask, showing enough of both to choose.

On approval, in this order: move the detail that would be lost into the survivor, close the other with
a comment naming the survivor, then **re-point every reference to the closed issue.** That pass comes last,
once the close has landed: search the board for the closed number and fix each mention.

**Closing sets Status on a project board** — the mechanism and its comment-dropping hazard are
`phil:issue-board`'s, under *A status write can close the issue underneath you*. Where the project has the **closed → Done**
workflow enabled — a different setting from Done → close, and one nothing here has verified — the card
lands in Done by itself, and this command holds no `gh project item-edit` to move it. Say so when you
close.

## Split

**"Split" means two different operations now, and this command performs only one of them.** Splitting a
**story** creates cards, as below. Splitting a **feature** on a board where one issue is one feature means
re-slicing its roadmap — a change to `docs/feature/<id>/slices/`, not to which cards exist — and this
command has no business there. Refuse it and say which operation was asked for; the
roster inside the feature's card is where its parts live (`phil:nwave-issue-board`).

**Numbers are assigned at creation, so the cross-references are a second pass.** Create the new cards
first, collect the numbers the forge hands back, then write the `## Chain` lines. A number written before
creation links to whatever else claims it. *(Mechanism: `phil:issue-board`, Bulk seeding needs two passes.)*

**Nothing is inherited.** Labels, milestone, and the chains that pointed at the original do not follow
the split — they are carried deliberately or not at all, and both are decisions. State what you are
carrying to each new card as part of the ask, not after.

**Then decide the original.** A split leaves a card that no longer describes work: it is closed as
superseded, or kept as the container the new cards hang under. Ask it as a second question; the split is
finished only once it is answered.

**A created issue is not a board card.** `gh issue create` puts an issue in the repo and nowhere on the
project; a card that was never `item-add`ed has no Status and is invisible in a kanban grouped by it
(`phil:issue-board`, *GitHub does not work the same way*).
Add each new card to the project, and report that its Status is unset — placing it in the queue is
`phil:rank-issues`, which is a decision about order and not this command's.

## Overcome by events

**This is the weakest oracle of the four, and it fails in the expensive direction.** It is a claim about
the world outside the board — that the work landed another way, or the decision behind it was
reversed — and board prose is no evidence of that.

So an OBE candidate arrives **unverified**, like the scan's unlinked path: report it, name what would
settle it, and leave it open until the repository settles it — the commit, the file, the reversing
decision, through `git log` and the working tree. A live card closed on another card's word goes
unnoticed for months.

On approval, close with the reason **in the same call** (`gh issue close -c`). Comment first, then close
or set Status; the same-call form satisfies that ordering by construction. The hazard is
`phil:issue-board`'s, under *A status write can close the issue underneath you*.

## Ungrouped effort

A card belonging to a larger effort that says so nowhere. **A milestone is a goal**, by
`phil:issue-board`'s convention; use it, and invent no second grouping convention.

**Joining an existing container and creating a new one are different questions.** Joining is the only
reversible operation in this whole section — one `--milestone` away from undone — so it can be offered
over a group of cards at once, provided the evidence for each is shown beside it. Creating a container
cannot: a goal commits the board to a purpose. Propose it, hand over the exact call, and stop.

**Before offering a goal, check whether the right container is a story.** A goal holds *cards*; a story
holds *feature directories*. Where the cards are whole features whose deltas declare one `Story:` slug,
the container is a **story card** and *features of one story, carded separately* supersedes this class —
offer that one and not this.

## Consolidate features of one story

Several open cards, each a whole feature, whose deltas declare the same `Story:` slug. The target shape
is **one story card** whose feature roster holds them as rows.

**Two shapes, and the report must name which it took.** Unlike a decomposed feature there is no
open-parent shape — a story card is what is being *created*, so nothing groups the members yet:

| Shape | What exists | What to do |
|---|---|---|
| (a) A closed story card already exists for this slug | a previous consolidation, or a card closed by mistake | **reopen it** and add the members as roster rows; never mint a second |
| (b) No story card exists | the common case | propose creating one; hand over the exact call and stop |

**Search closed issues before concluding shape (b).** A story card closed by a prior pass is invisible to
an open-issues scan and minting a second one splits the story permanently. This is the same search the
decomposed-feature section mandates, and the invariants in `SKILL.md` name both tiers for that reason.

**Irreversible, so it is one candidate at a time and never a group offer.** Closing a feature card
discards its own comments and history.

**The decomposed feature's un-parent step applies only where an edge exists.** This class is defined
by the absence of forge grouping. Where a member does sit as a sub-issue of something, remove that edge
first, for the same reason.

**Confirm the declarations are pushed before offering.** Evidence is a `Story:` line at column 0 in each
member's `feature-delta.md` **on the default branch** — `git ls-tree`, not the working tree. A slug that
exists only locally is invisible to every other reader.

**Two or more members in flight at once is a reason NOT to consolidate**, and it is the one case where the
answer runs the other way: concurrency means two people, which is what makes them separate cards under a
goal. Report it and offer no merge: **`REFUSE-CONCURRENT`**.

## Consolidate a decomposed feature

**Establish which of three shapes it is before writing anything.** The old split either closed its original
as superseded or kept it as the container, so the target of a consolidation may already exist, may exist
closed, or may not exist at all:

| Shape | Target | Can this command complete it? |
|---|---|---|
| **(a)** An open parent exists | Close the children under it | **Yes.** Lowest risk, and it still asks. |
| **(b)** No parent, but a closed original is findable | That closed card is the feature card | **No — the reopen is not in this command's grant.** Report `REFUSE-UNGRANTED` and hand over the calls. |
| **(c)** Neither | The feature card must be *created* | **Yes**, with the two-pass discipline for its cross-references. |

**Search closed issues before concluding (c).** The scan reads `--state open`, so shape (b) is invisible
to it; skipping this read resolves (b) as (c) and mints a duplicate:

```sh
gh issue list -R <owner/repo> --state closed --search "<feature id>"
```

Never guess between the three. Name which one the evidence shows, and put it in the question.

**Shape (b) is proposed, never performed** — this command holds no reopen, by design: *propose it, hand
over the exact call, and stop*. Two calls, because `gh issue reopen` restores the issue and **not** its Status field, so the card
would otherwise sit OPEN inside Done, a combination no board view flags:

```sh
gh issue reopen <n> -R <owner/repo>
# then set Status by hand — this command holds no `gh project item-edit`
```

**The roster is not this command's to write.** A feature card's roster lives inside the `nwave:status`
markers and is generated by `phil:nwave-issue-board` from the artifacts. The children's state reaches it at
the next refresh, from the artifacts; absorbing them by hand is a write into a generated region
(`REFUSE-GENERATED`).

**Per child, in this order** — stated as one sequence so no other order is permitted:

1. **Remove the parent edge** (`gh issue edit <parent> --remove-sub-issue <n>`). A closed sub-issue still
   counts toward its parent's completion, so closing first renders the feature **100% done** while the work
   continues.
2. **Post the pointer comment**, naming the feature card and the slice it became. A closed card with no
   pointer is a dead end for whoever finds it later.
3. **Close the child**, with the reason **in the same call**, as *Overcome by events* does.

**Move what would be lost before closing anything.** A slice card carries acceptance criteria, chain lines
and prose that the roster does not. Four pointer comments alone lose every done-condition on four
cards — *Merge*'s duty, times N.

**The rollup counts *closed*, not *done*, and this command cannot read it.** A card closed as won't-build is
indistinguishable from one closed as shipped; this repo's board once showed `3/3 · 100%` over a child
deliberately not built. **Say what the rollup will show before the user answers**, and hand over the read rather than claiming to have made it, because `subIssuesSummary`
is GraphQL-only and `/phil:groom-set` grants no `gh api`. The mechanism and the measurement are
`phil:issue-board`'s, in its `references/hierarchy.md` under *A parent's "N of M done" counts different things on each forge*.

**Only the scan holds `gh api graphql`; this command does not, by decision.** Beside `gh issue close`, a
grant that can mutate is a far larger promise than beside a report. `REFUSE-UNGRANTED` hands over the
rollup read instead.

## A declined candidate leaves no trace

Nothing is written: no label, no comment, no note in a body, no file. A decline record is a grooming
marker, which *Scan once, derive fresh* in `SKILL.md` forbids; the next run would trust it over the
board, and a decline whose reason has evaporated would never resurface.

**Say where the decline happened that the same candidate returns next run** — not only in a footnote.
Unstated, it reads as the tool forgetting.

## What the population actually is

**On a board in reasonable shape, the question is the deliverable and the write is the exception.**
On this repo's board on 2026-08-13 the run surfaced two candidates; both were declined, nothing was
written, and one named a seam the board had not held. Build the ask as the product, and expect most
runs to end on the note that a declined candidate will return.

**A population measured through a partial oracle describes the oracle.** The same board's
decomposed-feature result was tiers 2 and 3 only, while the parent edge was unreadable.
