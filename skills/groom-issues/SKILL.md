---
name: groom-issues
description: Skill bundle for the phil:groom-issues, phil:groom-fix, phil:groom-set and phil:groom-ask commands — reads a whole issue board in one call per forge and reports what is wrong with it against a stated standard, applies the mechanical fixes inside a scope the user picks, resolves the defects between issues (merge, split, close, group, consolidate a feature decomposed under retired rules) by asking before each one, and fills in a card that says too little from the user's answers and its own suggestions, labelling where every field's words came from. Derives the defect table fresh every run and stores no grooming marker, so a declined candidate returns.
---

# Groom issues — say what is wrong with a board

A board accumulates cards that someone filed half-finished. Reading them one at a time finds the
sloppy ones and misses the expensive ones, because the costly defects live *between* issues.

**Four commands, and the splits between them are the guarantee.** `/phil:groom-issues` reads and
reports — it holds no write tool at all, so read-only is enforced rather than declared.
`/phil:groom-fix` applies the mechanical column inside a scope the user picks, and can change no card's
existence. `/phil:groom-set` resolves the defects between issues — merge, split, close, group — and asks
before every one. `/phil:groom-ask` fills in a card that says too little, asking, suggesting, and
writing what the user sanctions. Do not improvise any of them.

The splits are not tidiness. A single command carrying the report in context is the design where a write
gets computed against remembered text instead of read text, and where read-only holds only as long as
nobody adds a tool. Separating them makes the re-read structural and the guarantee mechanical.

They also separate blast radii. `/phil:groom-fix` edits bodies and labels; every change it makes is one
edit to undo. `/phil:groom-set` changes **which cards exist** — a merge closes one, a split creates
several, and neither reverses cleanly. Handing both to one command would put the reversible and the
irreversible behind the same consent, and the reversible ones are far more numerous, so the habit formed
on them is the habit carried into the others.

`/phil:groom-ask` splits on a different axis again: not how far a write reaches, but **where the content
comes from**. Everything the other three write is derivable — an absolute URL, a mirrored chain line, a
milestone the user picked from a list. What this one writes is not derivable from anything: no artifact
holds why a card is wanted. That is why it is a separate command and not a mode. The guarantee it needs is
consent **plus provenance** — *did you sanction this claim, and is it on the record whose words carried
it* — and no scoping enforces either.

An earlier draft of this paragraph named the guarantee as *did you compose this* rather than *did you
consent*. That was retired on 2026-08-14: the command may now suggest and may rephrase, so composition is
no longer the discriminator. What survives is that the words' origin is never in doubt.

**REQUIRED BACKGROUND: `phil:issue-board`.** Every forge mechanic — `-R` targeting, label semantics,
absolute-URL rules, dependency links, generated blocks — lives there. Do not guess any of it here.

## The standard — what a well-formed issue contains

Without this, "appropriate description" is not checkable and grooming is taste. This is the house
default. **A project may override it in its own `CLAUDE.md`**, beside the per-project setup block
`phil:issue-board` already prescribes; where it does, that override wins and this section is ignored.

A well-formed issue has:

1. **A purpose readable without context** — what and why, in the body. A title is not a purpose, and
   the next reader is a stranger or a forgetful you.
2. **A way to tell when it is done** — acceptance criteria, or an outcome concrete enough to check.
3. **Links that resolve.** Absolute URLs for files, because GitHub emits relative paths verbatim and
   they 404. Bare `#N` for issues, because a bare reference renders live title and state where a
   markdown link freezes both. **This rule is about the form, and the form is fully checkable here** —
   a relative path is a finding whether or not its target exists, because the form 404s either way.
   Whether a correctly-formed link *reaches* something is a different question, and it belongs to the
   cross-reference row of the defect table below, which is where it goes dark.
4. **Correct labels**, with single-valued families carrying exactly one value. Nothing in a label's
   name says whether it excludes a sibling; GitHub has no scoped labels at all. `documentation` +
   `enhancement` on one issue is a defect or two orthogonal facts depending on a convention no forge
   records — so for a **project-local** family this is checkable only where the project declares it,
   and absent a declaration you report the rule **unevaluated**.

   **`wave: *` is the exception, and it is not the project's to declare.** In a repo holding `.nwave/`
   or `docs/feature/`, the wave family is single-valued **by default**, on `phil:nwave-issue-board`'s
   authority — *"the wave label is single-valued and must be swapped, not added"* — which also names
   the failure: a feature walked DISCUSS→DELIVER accumulates four wave labels and the record of where
   it stands becomes unreadable while every command reported success. That invariant is identical in
   every nWave repo. Requiring each one to hand-copy it means a repo that forgets goes dark on **the
   one family with a documented failure mode**, and dark silently, because unevaluated reads as clean
   to anyone not looking for it. Report the accumulation as a mechanical defect. A project overrides
   this only by declaring `wave: *` multi-valued in as many words, which nothing should.

   Match a family on the prefix before `::` or `: ` — `wave::deliver` where scoped labels exist and
   `wave: deliver` where they do not are the same family, and a board may carry both spellings.

   **What counts as a declaration**, because "the project declares it" is not self-executing: a bullet
   under the project's `## Issue board` section in `CLAUDE.md` naming a family and calling it
   single-valued or multi-valued, per the setup block in `phil:issue-board`. `CLAUDE.md` is already in
   context, so this costs no read. Two things are **not** declarations. A label's own description —
   it is not authoritative and loses on disagreement. And the labels in use: inferring the family from
   what the board already carries makes the most common pairing the rule, and then the board's habits
   audit themselves.
5. **A `## Chain` section when blocked or related** — the edge *and* the reason it exists, **on both
   ends**. `phil:issue-board` puts the prose line on both issues even where the forge writes the
   reverse edge itself, because the forge records the edge and never the reason. A chain naming an
   issue that does not name back is therefore half-written, and it is the half a reader lands on that
   decides whether they learn why. Cheap to check: the reciprocal is derivable from the same payload.

And it does **not** contain:

- **Session scratch or working state *typed outside a generated region*.** A board is world-readable, and
  hand-written scratch belongs in the git-ignored local surface (ADR-013).

  **Scoped 2026-08-14, not deleted.** Session state **inside** the `nwave:status` markers is now intended:
  ADR-013's deferred *partitioned local + board* option ships, so `/phil:handoff` projects the why, the next
  action and the diversion stack there — generated, timestamped, write-only, with the local file still the
  single authority. What remains a defect is *typed* scratch outside the markers, which is what the original
  rule was about. **Reporting a generated projection as a body defect would flag the correct shape**, and it
  would flag it on the one card most likely to have been maintained properly.
- **Hand-written content inside a generated region** — anything between `nwave:status` markers is
  regenerated, so a hand edit is destroyed on the next refresh and disagrees with its source until
  then.
- **A second copy of something the forge already keeps** — a roster where sub-issues exist, an order
  where position holds it. The copy is the one that goes stale.

  **A dated observation is not a copy.** The defect is a body asserting the forge's *present* state —
  "this board currently shows two cards In Progress" — which is wrong the moment the board moves and
  says nothing about when it was true. An observation stamped with its date, and pointing at the forge
  for the live answer, is history: it stays true, and a reader knows what to distrust. Prefer the
  observation where the state is the argument and deleting it would remove the argument.

## Scan once, derive fresh

**One call per forge**, bodies included:

```sh
gh issue list -R <owner/repo> --state open --json number,title,body,labels,milestone --limit 200
glab issue list -R <group/project> --output json --per-page 100
```

On `glab` the JSON flag is `-O`/`--output`, **not `-F`** — the mechanism and its silent failure are
`phil:issue-board`'s, under *`glab`'s JSON flag is `-O`, and `-F` fails silently*. Both commands return
bodies populated, so there is no N+1 and no reason to fetch issues individually.

**Never read or write a grooming marker.** No `groomed` label, no timestamp block, no state file. The
defect table is re-derived on every run. A stored marker becomes a second authority the moment
somebody edits a groomed issue — the exact failure `phil:issue-board` forbids under *One system of
record per scope* — and re-deriving costs one call.

The visible consequence, which the report must own: **a candidate the user declined will be proposed
again next run.** That is the price of storing nothing. Say so plainly, or it reads as the tool
forgetting and the user starts asking for the marker this rule exists to refuse.

## The defect table

Every finding names the rule it violates and quotes the evidence. A finding without both is an
opinion, and this skill does not report opinions.

Classify each, because the columns have different actors: `/phil:groom-fix` acts on the mechanical column,
and `/phil:groom-ask` on the semantic one (*Eliciting the semantic content*, below). Neither crosses.

| Mechanical — one right answer | Semantic — needs a human |
|---|---|
| A relative file link (404s on GitHub) | No purpose stated |
| An issue reference wrapped in markdown that should be bare | No way to tell when it is done |
| A single-valued family carrying two values — `wave: *` always, a project-local family where declared | Session scratch in the body |
| A missing cross-reference whose target is unambiguous | A second copy of forge-kept state the body's argument leans on |
| A second copy of forge-kept state that only restates it | Deciding which of those two a copy is |
| A `## Chain` line naming an issue that does not name back | Which end of a one-sided chain is right |

**A one-sided chain is the cheapest finding here and the easiest to write.** Detection is pure
derivation: collect every `#N` inside a `## Chain` section, and flag any whose target is open and
carries no reciprocal line. It is mechanical because the missing half is *stated on the other issue* —
nothing has to be invented, only mirrored. What is **not** mechanical is which end is right when the
two disagree about the reason; that is a human's.

Weight it by who writes it. On a real run, three of four chains written that day by an author who had
just read this rule were one-sided — writing one end while the relationship is fresh, and never
returning for the other, is the normal way this defect is made, not a careless one.

**The cross-reference row needs two things, and only one of them is a command away.** First, a
discriminator, because "unambiguous" alone made this row a judgement call wearing a mechanical label:
a reference is a finding when it names **a specific file a reader would open to follow the argument**.
A repository-root file (`CLAUDE.md`), a bare directory (`rules/`, `agents/`), a glob (`commands/*.md`)
and an ambiguous basename (`SKILL.md`, where twenty exist) are **not** findings — the first two are one
click from any page, and the last two have no single target to link. Without that line, two references
in the same body get opposite treatment and the column stops meaning "one right answer".

Second, the check itself. "Unambiguous" also means the target exists and is pushed, which
`phil:issue-board` establishes with
`git ls-tree origin/<default-branch> -- <path>` — outside a `Bash` scoped to `gh issue list` /
`glab issue list`, and deliberately so. A bare file path in a body is therefore a **candidate**, not a
finding: report it as unverified and say what would settle it. Promoting it anyway produces the failure
`phil:issue-board` warns about from the other direction — a link that renders, passes a read-back, and
404s for everyone else.

**A stale copy of forge state is two defects wearing one name.** The row used to sit wholly in the
semantic column, and a real run split it. Where the copy only restates what the forge holds — a prose
roster beside real sub-issues — deleting it loses nothing and the forge answers instead. Where the
copy is load-bearing — a card justifying its own existence by describing the board's current shape —
deleting it removes the argument, and only a human can say what replaces it.

Detection costs nothing either way: one `--json` call returns the body and the fields it contradicts,
so the comparison is inside the payload already fetched. **Read the two sides against each other on
every run** — a body asserting a sibling shipped, a parent listing children, a card citing a column's
contents. The prose keeps its confident tone long after the forge has moved.

Note what that does to the row's own classification: **the judgement comes before the fix**, so a later
slice cannot delete a stale copy unasked even when deletion turns out to be mechanical. It has to
establish which kind it is holding first, and that question is the human's.

**Do not report a missing `Work this with:` line as a body defect.** That line is generated into the
delimited block by `phil:nwave-issue-board`; its absence is a publishing question, not a content one,
and hand-writing it would be typing into a generated region.

## Applying the mechanical column — `/phil:groom-fix`

**Mechanical is a claim about the fix, never about the consent.** It says the content is derivable and
invents nothing — a relative path has one correct absolute form, a one-sided chain's missing half is
written on the other issue. It says nothing about whether the user wants their board edited now.
Reading the classification as authorisation is the failure this whole step is shaped against.

**Scope first, and write nothing before the answer.** The user picks a defect class, a subset of
issues, or everything. The tool does not choose, and does not start with the safest fix to show
progress. Group the offer by class, because that is the unit a class-level answer selects; a flat list
makes the user do the grouping the report should have done.

**Scale the offer to the population, and never the consent.** Over one finding, a
class/subset/everything menu is ceremony — and a step that feels like ceremony is the step people learn
to click through, which is how a consent gate stops working on the run where it matters. One finding
gets one confirmation naming it. Nothing gets applied because it was trivially small.

**Report the checks that ran and found nothing.** "One defect" over five silent checks reads as a thin
scan. Naming the passes is what separates *this board is clean* from *this tool looked at one thing*.
Do not report them as unevaluated — they had an oracle and they ran, which is a stronger statement than
`REPORT-UNEVALUATED` and must not be blurred into it.

**Every change carries the reason it needed no judgement**, per change, not per run:

```
#31 — rewrote ./docs/adr/ADR-013.md as <absolute URL>. No judgement: GitHub emits relative
      paths verbatim so the original 404s for every reader; target confirmed on origin/main;
      nothing invented.
```

The reason is the deliverable, because it is what makes the mechanical claim falsifiable. "Applied 2
fixes" cannot be contradicted by a reader; the sentence above can. A slice whose premise is that some
fixes need no consultation has to show its work, or the boundary is asserted rather than drawn.

**This command settles what the scan could not, and must actually do it.** The scan reports an unlinked
path as an unverified *candidate* because confirming the target needs `git`, which its `Bash` scoping
withholds. `/phil:groom-fix` holds `git ls-tree`, and that grant exists for exactly this: run
`git ls-tree origin/<default-branch> -- <path>` on every candidate in scope, and the confirmed ones
become findings you may fix. A candidate that will not confirm **stays unfixed and stays reported**,
with the check that failed named.

Read the scan's caveat as a statement about tools, not about truth. Carried across unexamined it
disqualifies the fix this command leads with — relative links that 404 are the first row of the
mechanical column and the headline of the command's own description, and a session that treats every
one of them as permanently unverifiable refuses its most common correct edit while reporting that it
followed the rules.

**The scope is a line, not a hint.** A mechanical defect outside the chosen scope stays untouched — and
stays *mentioned*. Out of scope means untouched, not unmentioned; a defect that disappears from the
output reads as fixed.

**The column is a property of the defect, not of the card that holds it.** An issue carrying one
mechanical and one semantic defect gets one of each treatment in the same pass. Skipping the card
because it also has a semantic defect makes that column contagious, and on a real board the mechanical
column would then empty itself through proximity rather than through measurement.

**Re-read before every write.** The apply is a separate command, so it must fetch the issue it edits
and cannot act on the scan's copy. If the body moved since the scan, report what moved and when, and do
not overwrite — the defect surviving is necessary but not sufficient, because the surrounding text is
unassessed and the scope the user agreed to was over the board as reported. The failure prevented here
is not a lost edit but a silent one: the forge records the session as last author, and whoever's
paragraph vanished cannot see that a groom run did it.

**Refuse a generated region even when the content is right.** A fix inside `nwave:status` markers is
destroyed on the next refresh and disagrees with its source until then. Refuse with the reason and point
at the generator — that pointer is the only part of the refusal that leads anywhere. Do not edit just
outside the markers to place it "nearly" right; that leaves the region wrong and hides it from the next
reader. Mechanical governs the content, ownership governs the bytes, and both must pass.

**What the population actually is.** Measured on this repo's board on 2026-08-13, after slice 01 had
been dogfooded twice: six mechanical checks with real oracles, and **one** defect board-wide — created
by the maintainer that same session, minutes after re-reading the rule it broke. The boundary is real
and its fixes need no question, but this is not a bulk fixer. Its value is catching the defect its own
author just made, and a design that assumes a full queue will build ceremony the population cannot
justify.

## Cross-issue candidates — the scan surfaces, never acts

These cannot be found by reading one issue, which is why the scan is whole-board. `/phil:groom-issues`
reports each with its evidence and stops; resolving them is `/phil:groom-set`, and is ask-first there.

- **Duplicates** — quote the overlapping content from both. Partial overlap is the real case and is
  not automatically a merge; it may be a split or a dependency.
- **Oversized** — a card carrying work that **cannot be demonstrated on its own**. Name the seam.

  **Demonstrability, not size, and the distinction is load-bearing.** A card holding a whole feature is
  large and demonstrable, so it passes — and on a board where one issue *is* one feature, it is the intended
  shape. Judging by size instead would report every correctly-formed card, and worse: it would propose
  splitting a consolidated feature back into slices every run, because this family stores no marker, so a
  declined split returns forever and only has to be accepted once. **Do not "fix" this rule toward size.**
  Verified 2026-08-14 against `phil:issue-board`'s own granularity rule, whose split clause is about two
  halves occupying different columns *at the same time* — that is, about concurrency.
- **Overcome by events** — the work landed another way, or the decision behind it was reversed.
- **Ungrouped effort** — a card belonging to a larger effort that says so nowhere. A milestone is a
  goal (`phil:issue-board`); do not invent a second convention.
- **Decomposed feature** — several open cards that are **slices of one feature**, on a board where one issue
  is one feature (`phil:nwave-issue-board`). Report the set with the evidence that ties them together.

  **This class exists because the retired rules produced it.** Under the old granularity rule a slice was
  independently demonstrable, so it was cardable — and this family's own split would have cut a feature into
  exactly these cards. **Grooming now meets the wreckage of its own earlier advice**, and none of the four
  classes above fires on it: not duplicates (a decomposition has no overlapping content to quote), not
  oversized (each card is small and demonstrable), not overcome by events, not ungrouped (they are grouped
  already). A board full of them reports **clean**, correctly and uselessly.

  **The evidence is ranked, because consolidating is irreversible:**

  | Signal | What it licenses |
  |---|---|
  | A real parent/child edge (sub-issues) | **Offer.** The forge asserts it; nothing is inferred. |
  | Bodies naming the same `docs/feature/<id>/` | **Offer.** The artifacts assert it. |
  | `slice NN` in the titles | **Report, never offer.** A naming convention is a habit, not a fact. |
  | A shared milestone | **Nothing at all.** A milestone is a goal and holds unrelated work by design. |

  Quote the evidence rather than characterising it. *"These look like slices of one feature"* is the finding
  restating its own conclusion.

## Resolving the set-level candidates — `/phil:groom-set`

The four above are the only operations here, and each asks. What follows is what the question has to
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
no earlier read could have seen. Slice 02's *re-read before every write* holds one level up — re-read
the board between candidates, and drop any whose subject a previous apply has already moved. Working
down a list built at the start of the run is how a session proposes merging an issue it closed ten
minutes ago.

### Merge

**Which card survives is the user's choice, not the lower number.** The lower number is older, which
correlates with nothing — the better-written body, the one carrying the acceptance criteria, and the
one people have already linked to are all independent of it. Ask, showing enough of both to choose.

On approval, in this order: move the detail that would be lost into the survivor, close the other with
a comment naming the survivor, then **re-point every reference to the closed issue.** That last pass is
separate and comes last, because until the close lands there is no settled answer to point at. Search
the board for the closed number and fix each mention — a merge that leaves five cards pointing at a
tombstone has moved the confusion rather than removed it.

**Closing sets Status on a project board** — the mechanism and its comment-dropping hazard are
`phil:issue-board`'s, under *A status write can close the issue underneath you*. Where the project has the
closed-item workflow enabled — it is on for this repo — the card lands in Done by itself, and this command holds no `gh project
item-edit` to put it anywhere else. Say so when you close; a card the user expected to keep triaging
has just left the queue.

### Split

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

### Overcome by events

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

### Ungrouped effort

A card belonging to a larger effort that says so nowhere. **A milestone is a goal** — #7's convention,
owned by `phil:issue-board`. Consume it; a second grouping convention invented here would make the two
disagree and neither authoritative.

**Joining an existing container and creating a new one are different questions.** Joining is the only
reversible operation in this whole section — one `--milestone` away from undone — so it can be offered
over a group of cards at once, provided the evidence for each is shown beside it. Creating a container
cannot: a goal is a commitment about what the board is for, and this command deliberately cannot make
one. Propose it, hand over the exact call, and stop.

### Consolidate a decomposed feature

**Establish which of three shapes it is before writing anything.** The old split either closed its original
as superseded or kept it as the container, so the target of a consolidation may already exist, may exist
closed, or may not exist at all:

| Shape | Target | The risk |
|---|---|---|
| **(a)** An open parent exists | Absorb the children into its roster, then close them | Lowest. Still ask. |
| **(b)** No parent, but a closed original is findable | That closed card is probably the right feature card | **A closed card is not in the list you just read**, so this shape is the one a session misses and resolves as (c) — minting a duplicate of a card that already exists |
| **(c)** Neither | Consolidation requires *creating* the feature card | A create, so its cross-references take the two-pass discipline |

**Search closed issues before concluding (c).** Never guess between the three; name which one the evidence
shows and put it in the question.

**In shape (b), reopening carries its own defect.** `gh issue reopen` restores the issue and **not** the
Status field, so the card lands OPEN while sitting in Done — a combination no board view flags. Set the field
by hand afterwards and read it back. (`phil:issue-board`; the same asymmetry `CLAUDE.md` records for this
repo.)

**Remove the edge, then close the child. Never the reverse.** A closed sub-issue still counts toward its
parent's completion, so closing children first renders the feature **100% done** while the work continues.
Measured 2026-08-14: adding a child gave `1/0`, closing it gave `1/1 · 100%`, removing the edge gave `0/0` —
so removal genuinely drops the child rather than hiding it, and the order is the whole safeguard.

**The rollup counts *closed*, not *done*, and that is worse than it sounds.** A card closed as won't-build is
indistinguishable from one closed as shipped. Observed on this repo's board: a parent reporting `3/3 · 100%`
where one child had been deliberately **not** built and closed anyway. So a consolidation that closes
children does not merely inflate a number — it produces an inflation nobody can read as one. Say what the
rollup will show, before the user answers.

**Every closed child carries a pointer comment, posted *before* the close** — naming the feature card and the
roster row it became. Auto-close-on-Done drops a comment posted afterwards, and a closed card with no pointer
is a dead end for the next reader who finds it.

### A declined candidate leaves no trace

Nothing is written: no label, no comment, no note in a body, no file. D6 forbids a grooming marker and
a decline record is a grooming marker wearing the word *decline* — the moment it exists, the next run
trusts it over the board, and a candidate the user declined for a reason that has since evaporated
never surfaces again.

The visible cost is that **the same candidate is proposed again next run**, and the report must say so
where the decline happened, not only in a footnote. Unstated, it reads as the tool having forgotten,
which is the complaint that produces a request for the marker this rule exists to refuse. Stated, it
reads as what it is: the board is the only record, and it is re-read every time.

### What the population actually is

Measured on this repo's board on 2026-08-13, thirteen open issues: **two candidates, both declined, and
nothing written.** One partial overlap (two cards adding checks to the same priority ladder) and one
ungrouped pair (the board's only two typesetting cards, with no milestone naming that goal). No
duplicates, no oversized cards, no work overcome by events.

Read that result carefully, because the obvious reading is wrong. The run's output was not *nothing* —
it was two questions, one of which named a seam the board did not previously hold: both cards leave the
same question open about how a new check earns its tier, and neither says so. The user declined and the
seam is now known. **On a board in reasonable shape the deliverable of this command is the question, and
the write is the exception**, which inverts the assumption a section full of merge and split mechanics
invites. Build the ask as the product; the applies are what happens on the minority of runs.

It also settles which guard is load-bearing. *Declined leaves no trace* looked like an edge case when it
was written and is the observed common path — so the note that a candidate will return is not a footnote
for a rare run, it is the sentence most runs end on.

## Reporting

Lead with the shape of the board, not the findings:

```
57 issues read · 52 clean · 3 with body defects · 2 duplicate candidates · 1 oversized
```

Then the defects, grouped by issue, each citing its rule and evidence. Then the cross-issue
candidates. Then, if anything was declined on a previous run, the note that it will reappear.

**A clean board is reported clean.** Do not manufacture findings to justify the run — that is how a
grooming tool teaches people to stop running it.

**A partial read may never make a completeness claim.** If pagination failed, the forge was
unreachable, or the limit truncated the list, say the read was partial and report *only* what was
found. "52 clean" over a partial scan is the single most misleading thing this skill can emit,
because it is a claim about issues nobody looked at.

**A rule that could not be evaluated is not a rule that passed.** Two checks go dark routinely: rule 4
wherever a **project-local** family is undeclared, and the cross-reference row wherever a target cannot be
confirmed pushed. Both then produce no findings, and no findings reads as compliance. Name them, with
the reason:

```
rules 1, 2, 3, 5 evaluated · rule 4 partly unevaluated (`wave: *` checked — normative;
  `documentation`/`enhancement` undeclared in CLAUDE.md)
· 6 unlinked paths unverified (target check needs git, out of scope here)
```

This is the partial-read failure one rule narrower, and it hides better — the issue count is honest,
so nothing in the summary looks incomplete. A reader who is told the board is clean will not ask which
rules were awake.

**Say a check went dark only when it had something to decide.** A board where no issue carries two
labels does not need rule 4's oracle, and reporting it unevaluated there is boilerplate — which is how
a caveat stops being read by the run that needs it. The note is owed when a candidate existed and the
check could not settle it: two labels and no declared family, an unlinked path and no way to confirm
the target. No candidate, no note.

## Eliciting the semantic content — `/phil:groom-ask`

The mechanical column has `/phil:groom-fix` and the set-level column has `/phil:groom-set`. **The
semantic column had nothing**, and that is a hole rather than a boundary: a card failing rules 1 and 2
is reported every run and resolvable by none of them, so a board of title-only cards produces an
identical report forever. That is *this tool teaches people to stop running it* reached from the
other side — not manufactured findings, but real findings with no exit.

**The refusal was never the problem; the missing editor was.** `/phil:groom-fix` declining to draft a
purpose is the boundary working exactly as designed, and nothing here relaxes it — that command never
asks, so it may never draft. What this adds is somewhere for the content to come from.

**Present the card before asking.** State what it is, what it already says, and which rule failed. A
question that assumes the reader remembers the card gets a worse answer, or none — and the reader is
often being asked about work a past self filed.

**The human sanctions every claim; the session may choose the words.** That is the unit, and stating it
precisely matters — an earlier draft said *sanctions every word*, which the rephrasing path below does not
deliver and cannot. Suggest one or two ways to fill the gap, **marked as the session's**, let the human
accept, edit, or replace, and write the result as a clean card in the house voice rather than a transcript.

**What must never happen is a claim reaching the card unsanctioned, or a word reaching it untraceable.**
An inferred sentence is indistinguishable from an authored one *once written*, so the remedy is not to
forbid drafting — it is to make every field's origin legible and every rewrite inspectable:

- **Each field written carries a provenance label**, from exactly this set, and the human's action decides
  which: accepted a suggestion unchanged → `you accepted my suggestion`; changed one → `you edited my
  suggestion`; **rejected the suggestions and supplied their own, or answered with none offered** →
  `you wrote`; answered in their own words and the session tidied them → `I rephrased your answer`.
  **A field written without a label is the defect**, however well the body reads. A field left alone
  because its rule passed is not written and takes no label.
- **Never combine labels, and never rephrase an accepted suggestion.** If a suggestion is accepted, the
  written form **is** the suggestion, quoted — otherwise no single label is true, and both available ones
  lie in a different direction.
- **Show the answer beside the written form wherever the two differ**, for `I rephrased your answer` and
  `you edited my suggestion` alike, and quote the suggestion for `you accepted my suggestion`. A rewrite
  the reader cannot inspect is an assertion.
- **Rephrasing is a tidying licence, not a modelling one.** Fix grammar, punctuation and register; never
  introduce a concept the human did not use, and never narrow or widen the claim. A rewrite that changes
  what the card asserts is composition wearing a truthful label — the one failure the provenance rule
  cannot catch on its own.
- **An accept must name the suggestion or restate its text.** A bare affirmation — "ok", "sure", "yep",
  "sounds right", "that works" — is never an accept. This holds **even when only one suggestion was
  offered**, where a naming rule would otherwise be satisfied by accident: the reply is equally likely to
  mean *I have read the question and will answer it*.
- **A reply that is neither an accept, an edit, a replacement, nor a decline is unanswered.** Ask once
  more, naming what is still needed. **After a second unanswered ask, treat it as a decline** — say so,
  write nothing, record nothing. Two asks is the limit; a third is the nagging that teaches people to
  stop running the tool.

**A rule that passed is never rewritten.** The session may rephrase what it elicited; a purpose that
already satisfies rule 1 is out of reach, however much tidier it could be. This is the boundary that
stops *write a clean card* becoming *rewrite the card*.

**Ask only what the scan reported missing.** Rules 1 and 2 fail independently, so derive the questions
from the findings — one question per missing rule, and none for a rule that passed. Asking for a
purpose a card already states is ceremony on the answered half, and worse than ceremony: it invites
overwriting prose that passes.

Measured on this repo's board 2026-08-14: **three cards fail rule 2 (#1, #2, #3) and none fail rule
1.** Every failing card already states a purpose and lacks only a done-condition. The population is
*partial*, not empty — so a loop that always asks both questions is wrong against every card it has
actually been observed to meet. A two-question loop was the first draft of this section, and nothing
in the suite failed when it asked for both, which is why fixture `30` exists.

Note what the family did before this. All four commands hold `AskUserQuestion`, and the other three
use it only for **consent** — pick a scope, pick the surviving card of a merge. None of them ever
asks what an issue is *for*. Elicitation is a different use of the same tool, and its absence is why
the semantic column had no exit. Here the options are the **suggestions**, and free text is the escape
hatch that keeps *the human sanctions every word* true rather than nominal.

**One card per invocation.** No batch, no apply-to-all. The content differs every time, so a
population-scaled offer has nothing to scale over — and a bulk offer would collect one answer and
write it as though it were several. Slice 02 measured what a scale-shaped offer does to a small
population: it becomes ceremony, and ceremony is what teaches people to click through a gate.

**A partial answer is written partially.** One field given and one withheld writes the one given, and
says which is still missing. **Offering** the withheld half is permitted; *supplying* it because the body
looks nearly done is not, and the difference is a visible, refusable suggestion. A card with a purpose and
no done-condition is a smaller defect than one with neither.

**Report provenance per field.** Not decoration: it is what makes an unsanctioned sentence visible.
"Wrote the body" cannot be contradicted by a reader; a per-field label, with the answer shown beside the
written form wherever they differ, can — the reader knows what they said, and any sentence they did not
sanction stands out.

**Re-read immediately before writing, and refuse a body that moved.** Slice 02's rule, and it binds
harder here — the text at risk is prose a human wrote, not a link that would have 404'd. Report what
moved and hand back **both the answers and any draft**, so a refused write does not also lose what was
just collected.

**A decline writes nothing and records nothing.** No body, no label, no comment, no note. Same D6 cost
as a declined set-level candidate, and this is the third surface that pays it: say at the decline that
the finding returns next run. A user who has now met the same cost three times still has not been told
it a third time unless this surface says so.

## Decision outcomes

Report the outcome by name, every run. Each command draws from its own set.

`/phil:groom-issues` (the scan) reports exactly one of:

`REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL`

and any of these **alongside** it: `REPORT-UNEVALUATED` (a rule had a candidate and no oracle) ·
`SURFACE-CANDIDATE` (a cross-issue candidate reported, not acted on) · `NOT-A-DEFECT` (something that
looks like a finding and is not) · `NO-MARKER` · `READ-ONLY`.

`/phil:groom-fix` (the apply) reports `SCOPE-FIRST` before any write, then exactly one of:

`APPLY-MECHANICAL` · `STALE-REREAD` · `REFUSE-GENERATED`

with `LEAVE-SEMANTIC` alongside whenever a semantic defect was reported and left.

`/phil:groom-set` (the set-level loop) reports `ASK-SET-LEVEL` before any write, then exactly one of:

`APPLY-MERGE` · `APPLY-SPLIT` · `APPLY-CONSOLIDATE` · `DECLINE-NO-TRACE` · `REFUSE-UNVERIFIED`

with `REDERIVE-BETWEEN` alongside whenever an apply invalidated a later candidate.

**`APPLY-CONSOLIDATE` must name which of the three shapes it took** — an open parent, a reopened closed
original, or a newly created card — because the three have different blast radii and the report is the only
place that distinction survives. It must also state what the parent's rollup now shows, since the number
changed and nobody reading the card can tell inflation from completion.

`/phil:groom-ask` (the elicitation loop) reports `ASK-CONTENT` before any write, then exactly one of:

`WRITE-ELICITED` · `WRITE-PARTIAL` · `DECLINE-NO-TRACE` · `STALE-REREAD` · `REFUSE-GENERATED`

**`ASK-CONTENT` standing alone is a legal terminal state, and it is the only one that resolves nothing.**
A run that asked and received no answer, no edit, no replacement and no decline reports `ASK-CONTENT`
again and stops — the unanswered case (fixture `32`) and the named-queue case (fixture `29`). This is the
counterpart of `REFUSE-UNVERIFIED` below: both are outcomes where the run correctly ends without the
thing it exists to produce. **Do not reach for `DECLINE-NO-TRACE` to obtain a terminal outcome** — it
records that the user refused, and a user who simply has not answered yet did not refuse. That
substitution is available, plausible, and false.

`DECLINE-NO-TRACE`, `STALE-REREAD` and `REFUSE-GENERATED` are the same outcomes the other commands
report, meaning the same things — a decline that stores nothing, a body that moved since the read, and
a write whose target belongs to a generator.

**`REFUSE-GENERATED` belongs here for the same reason it belongs to `/phil:groom-fix`, and the case is
less exotic than it looks.** A card can carry a generated `nwave:status` block and still state no
purpose: the block is published from the artifacts and says nothing about why the work is wanted. So
elicited prose has to be placed *outside* the markers, and a body that leaves no room for it — one
where the generated region is the whole body — is refused rather than approximated. Writing just
outside the markers to get the content in is the same defect one line over, and is forbidden in the
same words.

**`SCOPE-FIRST`, `ASK-SET-LEVEL` and `ASK-CONTENT` are preconditions, not alternatives.** An apply that reports only
its terminal outcome has not said whether it asked — and *did it ask* is the one property both writing
commands exist to guarantee. `REFUSE-UNVERIFIED` is the exception that proves it: nothing was asked
there, because an unconfirmed candidate is not put to a vote.

**`ASK-CONTENT` differs in kind from the other two.** They collect consent — a scope, a survivor.
It collects *content*, and the content is the deliverable. A run reporting `WRITE-ELICITED` without
`ASK-CONTENT` wrote a body nobody sanctioned.

**`WRITE-ELICITED` and `WRITE-PARTIAL` are incomplete without provenance.** Each written field carries one
of `you wrote` · `you accepted my suggestion` · `you edited my suggestion` · `I rephrased your answer`, and
an unlabelled field fails the outcome regardless of how the body reads. Where a label is
`I rephrased your answer` or `you edited my suggestion`, the answer appears beside the written form.

## What this skill must never do

All four commands:

- Read or write a grooming marker, in any form — including a record of what was declined.
- Report a finding without the rule it violates and the evidence for it.
- Claim completeness over a partial read.
- Let a rule that could not be evaluated pass for a rule that was satisfied.
- Report a missing generated line as a body defect.
- Merge, split, close, or group without an explicit answer to a question that offered the outcome.

`/phil:groom-issues` (the scan) additionally:

- **Write anything.** No issue edits, no labels, no comments, no milestones. It holds no write tool, so
  a session that finds itself needing one here has misread the command.

`/phil:groom-fix` (the apply) additionally:

- Write before the user has picked a scope.
- Treat the mechanical classification as consent, or a small population as permission.
- Cross the chosen scope, even to fix something mechanical.
- Apply an edit computed against text read before the last change to the issue.
- Write inside a generated region, or just outside it to approximate the fix.
- Touch a semantic defect — draft acceptance criteria, rewrite a purpose, decide a granularity. These
  are reported and left, every time.
- Carry a scope from one run into the next. Nothing is stored between runs; a remembered scope is the
  marker this skill refuses, grown back in another shape.

`/phil:groom-ask` (the elicitation loop) additionally:

- **Write any word the human has not sanctioned.** Drafting is permitted; adopting a draft on silence,
  on "ok", or on any reply that is neither an accept, an edit, nor a replacement is not.
- **Write a field without a provenance label**, or claim `I rephrased your answer` without showing the
  answer beside the written form.
- Ask a question without first presenting the card and the rule that failed.
- **Rewrite a rule that passed.** A purpose already satisfying rule 1 is out of reach; only what this run
  elicited may be rephrased.
- Complete a partial answer by supplying the withheld half. Offering it is permitted; writing it unasked
  is not.
- **Ask for a rule the scan reported as passing.** The questions come from the findings.
- Offer a batch, an apply-to-all, or "the same again for the next card".
- Overwrite a body that moved since the read, or discard the answers and any draft when refusing.
- **Write elicited prose inside a generated region, or just outside it to approximate placement.**
- Touch a mechanical defect, a label, a link, or which cards exist. Those have their own commands.

`/phil:groom-set` (the set-level loop) additionally:

- Offer a yes-or-no over a finding whose evidence admits more than two outcomes.
- Choose the surviving card of a merge, by number or by any other proxy for the user's judgement.
- Leave references pointing at an issue it closed.
- Write a cross-reference to a card the forge has not yet numbered.
- Leave a split's original open beside its own pieces, or its new cards off the project board.
- **Close a child while its parent edge still exists.** The child then counts toward the parent's completion;
  remove the edge first.
- **Conclude that no feature card exists without searching closed issues.** A previous split may have closed
  the original as superseded, and minting a second one buries the first.
- **Consolidate on title evidence alone.** `slice NN` in a title is a habit; it licenses a report, never an
  irreversible write. A shared milestone licenses nothing.
- **Reopen a card and leave its Status unset.** `gh issue reopen` does not restore the field, so the card sits
  OPEN in Done and no view flags it.
- **Split a feature into slice cards.** Splitting a story creates cards; splitting a feature means re-slicing
  its roadmap, which is not this command's to do.
- Close on board prose alone. The claim that work landed another way is settled in the repository or
  not at all.
- Create a milestone, or treat one card's container as evidence for another's.
- Record a decline anywhere, or let a run of approvals turn the next ask into a formality.

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, the command loader, or
`phil:issue-board`'s body-relevant sections change.
