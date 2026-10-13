# Resolving the set-level candidates — `/phil:groom-set`

Part of the `groom-issues` skill. `SKILL.md` governs this command as much as this file does: the
standard, the scan, the defect table, the cross-issue candidates, reporting, the decision outcomes and
the never-do list all apply here.

The operations in `SKILL.md`'s *Cross-issue candidates* are the only ones here, and each asks. What follows is what the question has to
contain to be answerable, and what the apply owes afterwards.

**The ask must have the same arity as the finding.** This is the rule the whole step turns on. Two
issues that overlap in part are not a yes-or-no about merging: they may be a merge, a split along the
seam, a dependency edge, or two cards that happen to share a mechanism and should stay apart. Offering
*merge? y/n* over that finding forces a wrong answer, because the true answer was never on the menu —
and a declined merge then reads as *these are unrelated*, which is a third thing that was also never
asked. Present the outcomes the evidence actually admits, and let *leave them alone* be one of them.

**Evidence is quoted, not characterised.** "These look similar" is the finding restating its own
conclusion. Quote the overlapping content from both bodies, then say in one line what is shared and
what is not — the difference is the part the user is actually adjudicating, and summarising it away
leaves them deciding on your reading instead of theirs.

**One candidate at a time, re-derived, not carried.** An apply here changes the set the remaining
candidates were computed over: a merge closes a card a later candidate names, a split assigns numbers
no earlier read could have seen. `SKILL.md`'s *re-read a card immediately before writing it* holds for every card this command edits,
including a merge's survivor, and one level up as well — re-read
the board between candidates, and drop any whose subject a previous apply has already moved. Working
down a list built at the start of the run is how a session proposes merging an issue it closed ten
minutes ago.

## Merge

**Which card survives is the user's choice, not the lower number.** The lower number is older, which
correlates with nothing — the better-written body, the one carrying the acceptance criteria, and the
one people have already linked to are all independent of it. Ask, showing enough of both to choose.

On approval, in this order: move the detail that would be lost into the survivor, close the other with
a comment naming the survivor, then **re-point every reference to the closed issue.** That last pass is
separate and comes last, because until the close lands there is no settled answer to point at. Search
the board for the closed number and fix each mention — a merge that leaves five cards pointing at a
tombstone has moved the confusion rather than removed it.

**Closing sets Status on a project board** — the mechanism and its comment-dropping hazard are
`phil:issue-board`'s, under *A status write can close the issue underneath you*. Where the project has the **closed → Done**
workflow enabled — a different setting from the Done → close one this repo declares, and one nothing here has
verified — the card lands in Done by itself, and this command holds no `gh project
item-edit` to put it anywhere else. Say so when you close; a card the user expected to keep triaging
has just left the queue.

## Split

**"Split" means two different operations now, and this command performs only one of them.** Splitting a
**story** creates cards, as below. Splitting a **feature** on a board where one issue is one feature means
re-slicing its roadmap — a change to `docs/feature/<id>/slices/`, not to which cards exist — and this
command has no business there. Refuse it and say which operation was asked for; the roster inside the
feature's card is where its parts live, and adding cards for them undoes the paradigm rather than
implementing it. See `phil:nwave-issue-board`.

**Numbers are assigned at creation, so the cross-references are a second pass.** Create the new cards
first, collect the numbers the forge hands back, then write the `## Chain` lines. Writing a reference
during creation means writing a number that does not exist yet, and the forge will render it as a link
to whatever else claims it. *(Mechanism: `phil:issue-board`, Bulk seeding needs two passes.)*

**Nothing is inherited.** Labels, milestone, and the chains that pointed at the original do not follow
the split — they are carried deliberately or not at all, and both are decisions. State what you are
carrying to each new card as part of the ask, not after.

**Then decide the original.** A split leaves a card that no longer describes work: it is closed as
superseded, or kept as the container the new cards hang under. That is a second question, and the split
is not finished until it is answered — an original left open beside its own pieces is now the
duplicate this command exists to find.

**A created issue is not a board card.** `gh issue create` puts an issue in the repo and nowhere on the
project; a card that was never `item-add`ed has no Status and is invisible in a kanban grouped by it
(`phil:issue-board`, *GitHub does not work the same way*).
Add each new card to the project, and report that its Status is unset — placing it in the queue is
`phil:rank-issues`, which is a decision about order and not this command's.

## Overcome by events

**This is the weakest oracle of the four, and it fails in the expensive direction.** The others are
answerable from the payload the scan already holds; this one is a claim about the world outside the
board — that the work landed another way, or the decision behind it was reversed. Board prose is not
evidence of that. A sibling card asserting that something shipped is exactly the stale copy of state
the defect table already distrusts.

So an OBE candidate arrives **unverified**, in the same shape as slice 01's unlinked path: report it,
name what would settle it, and do not close on it. What settles it is the repository — the commit, the
file, the reversing decision — reachable here through `git log` and the working tree. Confirm it or
leave it standing. Closing a live card because another card said the work was done is the one
irreversible mistake on this board that nobody notices for months.

On approval, close with the reason **in the same call** (`gh issue close -c`), so the account of why it
went cannot be separated from the going. The observed hazard runs the other way round — a Status write to
Done closes the issue, and a `gh issue close -c` afterwards reports "already closed" and drops its comment —
and it is `phil:issue-board`'s to state, under *A status write can close the issue underneath you*. Comment
first, then close or set Status; the same-call form satisfies that ordering by construction.

*(Corrected 2026-08-14: this paragraph previously asserted that a comment posted after a close is dropped
"once the project's close workflow has run" — a claim in the close-first direction that neither
`phil:issue-board` nor this repo's `CLAUDE.md` establishes. Both observed the Status-first case. The
advice was right and the mechanism was invented.)*

## Ungrouped effort

A card belonging to a larger effort that says so nowhere. **A milestone is a goal** — #7's convention,
owned by `phil:issue-board`. Consume it; a second grouping convention invented here would make the two
disagree and neither authoritative.

**Joining an existing container and creating a new one are different questions.** Joining is the only
reversible operation in this whole section — one `--milestone` away from undone — so it can be offered
over a group of cards at once, provided the evidence for each is shown beside it. Creating a container
cannot: a goal is a commitment about what the board is for, and this command deliberately cannot make
one. Propose it, hand over the exact call, and stop.

**Before offering a goal, check whether the right container is a story.** A goal holds *cards*; a story
holds *feature directories*. Where the cards are whole features whose deltas declare one `Story:` slug,
the container is a **story card** and *features of one story, carded separately* supersedes this class —
offer that one and not this. A milestone filed around those cards groups them on the board while leaving
the thing that should be one card as several, which looks like a resolution and is not.

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
decomposed-feature section mandates, and the never-do list in `SKILL.md` names both tiers for that reason.

**Irreversible, so it is one candidate at a time and never a group offer.** Closing a feature card
discards its own comments and history.

**The decomposed-feature rollup hazard does NOT transfer, and importing it would be a warrant that
cannot obtain.** That hazard is *un-parent before closing, or the parent renders complete while the work
continues* — it presupposes a real parent/child edge, which is that class's defining tier-1 evidence.
This class is defined by the **absence** of any forge grouping, so there is no edge to remove. Where a
member does happen to sit as a sub-issue of something, remove that edge first for the shipped reason;
otherwise the step does not apply.

**Confirm the declarations are pushed before offering.** Evidence is a `Story:` line at column 0 in each
member's `feature-delta.md` **on the default branch** — `git ls-tree`, not the working tree. A slug that
exists only locally is invisible to every other reader, and consolidating on it produces a story card
whose membership nobody else can verify.

**Two or more members in flight at once is a reason NOT to consolidate**, and it is the one case where the
answer runs the other way: concurrency means two people, which is what makes them separate cards under a
goal. Report it and do not offer the merge. **Outcome: `REFUSE-CONCURRENT`** — a refusal on verified
evidence, which is neither `DECLINE-NO-TRACE` (nobody declined) nor `REFUSE-UNVERIFIED` (the evidence is
good). A terminal stop with no outcome of its own is unreportable.

## Consolidate a decomposed feature

**Establish which of three shapes it is before writing anything.** The old split either closed its original
as superseded or kept it as the container, so the target of a consolidation may already exist, may exist
closed, or may not exist at all:

| Shape | Target | Can this command complete it? |
|---|---|---|
| **(a)** An open parent exists | Close the children under it | **Yes.** Lowest risk, and it still asks. |
| **(b)** No parent, but a closed original is findable | That closed card is the feature card | **No — the reopen is not in this command's grant.** Report `REFUSE-UNGRANTED` and hand over the calls. |
| **(c)** Neither | The feature card must be *created* | **Yes**, with the two-pass discipline for its cross-references. |

**Search closed issues before concluding (c).** The scan reads `--state open`, so shape (b) is **invisible to
it** — a second read is required, and skipping it is how (b) gets resolved as (c), minting a duplicate of a
card that already exists while the original's history sits behind a tombstone:

```sh
gh issue list -R <owner/repo> --state closed --search "<feature id>"
```

Never guess between the three. Name which one the evidence shows, and put it in the question.

**Shape (b) is proposed, never performed.** Reopening is not something this command holds, and that is
deliberate rather than an oversight: it is the milestone case again — *propose it, hand over the exact call,
and stop*. Two calls, because `gh issue reopen` restores the issue and **not** its Status field, so the card
would otherwise sit OPEN inside Done, a combination no board view flags:

```sh
gh issue reopen <n> -R <owner/repo>
# then set Status by hand — this command holds no `gh project item-edit`
```

**The roster is not this command's to write.** A feature card's roster lives inside the `nwave:status`
markers and is generated by `phil:nwave-issue-board` from the artifacts. Do not "absorb" children into it —
that is a write into a generated region, which `SKILL.md`'s standard forbids and `REFUSE-GENERATED` names. The children's
state reaches the card at the next refresh, from the artifacts, without anything being typed here.

**Remove the edge, then post the pointer comment, then close. In that order, per child.** Three rules
compressed into one sequence, because stating them separately permits every wrong permutation:

1. **Remove the parent edge** (`gh issue edit <parent> --remove-sub-issue <n>`). A closed sub-issue still
   counts toward its parent's completion, so closing first renders the feature **100% done** while the work
   continues.
2. **Post the pointer comment**, naming the feature card and the slice it became. A closed card with no
   pointer is a dead end for whoever finds it later.
3. **Close the child**, with the reason **in the same call** — the form *Overcome by events* already uses,
   which satisfies the ordering by construction and needs no claim about what drops a later comment. The
   observed hazard is narrower than "a comment after a close is lost": it is a `gh issue close -c` against an
   issue a **Status write** had already closed, which is `phil:issue-board`'s under *A status write can close
   the issue underneath you*. Do not restate it more broadly than it was measured.

**Move what would be lost before closing anything.** A slice card carries acceptance criteria, chain lines
and prose that the roster does not. Consolidating four cards and keeping only four pointer comments loses
every done-condition on them — the same duty *Merge* carries, and it binds harder here because there are N
children rather than one.

**The rollup counts *closed*, not *done*, and this command cannot read it.** A card closed as won't-build is
indistinguishable from one closed as shipped: observed on this repo's board, a parent reporting `3/3 · 100%`
where one child had been deliberately **not** built and closed anyway. So consolidation does not merely
inflate a number — it produces an inflation nobody can read as one. **Say what the rollup will show before
the user answers**, and hand over the read rather than claiming to have made it, because `subIssuesSummary`
is GraphQL-only and `/phil:groom-set` grants no `gh api`. The mechanism and the measurement are
`phil:issue-board`'s, under *A parent's "N of M done" counts different things on each forge*.

**Do not read the family as one grant — the scan is the exception.**
`/phil:groom-issues` gained `Bash(gh api graphql:*)` on 2026-09-04 for the parent-edge read; this command
did not, and `REFUSE-UNGRANTED` still names a rollup read among the calls it hands over. Widening it here
was not decided and is not implied. The asymmetry is the point: the scan only reports, so a promise not to
mutate costs it nothing it was ever going to do, while this command exists to make irreversible writes —
the identical grant sitting beside `gh issue close` is a materially larger promise than it is beside a
report.

## A declined candidate leaves no trace

Nothing is written: no label, no comment, no note in a body, no file. *Scan once, derive fresh* in `SKILL.md` forbids a grooming marker, and
a decline record is a grooming marker wearing the word *decline* — the moment it exists, the next run
trusts it over the board, and a candidate the user declined for a reason that has since evaporated
never surfaces again.

The visible cost is that **the same candidate is proposed again next run**, and the report must say so
where the decline happened, not only in a footnote. Unstated, it reads as the tool having forgotten,
which is the complaint that produces a request for the marker this rule exists to refuse. Stated, it
reads as what it is: the board is the only record, and it is re-read every time.

## What the population actually is

Measured on this repo's board on 2026-08-13, thirteen open issues: **two candidates, both declined, and
nothing written.** One partial overlap (two cards adding checks to the same priority ladder) and one
ungrouped pair (the board's only two typesetting cards, with no milestone naming that goal). No
duplicates, no oversized cards, no work overcome by events, and no decomposed features — every slice card on
it was already closed, which is why that class was found by reasoning about consumers' boards rather than by
reading this one.

**Read the last of those as a tiers-2-and-3 result, because that is all it was.** A second run on
2026-08-14 against 0.53.0 reported the decomposed-feature class *evaluated with no candidates*, and the
strongest tier had no oracle behind it — the parent edge was unreadable, and on this board there happened
to be none to miss. On a board whose slice cards **are** parented, the identical sentence would have been
emitted and would have meant nothing. That is issue #30, and it is the sharpest available illustration of
this section's own lesson: a population measured through a partial oracle describes the oracle, not the
population.

Read that result carefully, because the obvious reading is wrong. The run's output was not *nothing* —
it was two questions, one of which named a seam the board did not previously hold: both cards leave the
same question open about how a new check earns its tier, and neither says so. The user declined and the
seam is now known. **On a board in reasonable shape the deliverable of this command is the question, and
the write is the exception**, which inverts the assumption a section full of merge and split mechanics
invites. Build the ask as the product; the applies are what happens on the minority of runs.

It also settles which guard is load-bearing. *Declined leaves no trace* looked like an edge case when it
was written and is the observed common path — so the note that a candidate will return is not a footnote
for a rare run, it is the sentence most runs end on.
