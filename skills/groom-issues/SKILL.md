---
name: groom-issues
description: Skill bundle for the phil:groom-issues, phil:groom-fix and phil:groom-set commands — reads a whole issue board in one call per forge and reports what is wrong with it against a stated standard, applies the mechanical fixes inside a scope the user picks, and resolves the defects between issues (merge, split, close, group) by asking before each one. Derives the defect table fresh every run and stores no grooming marker, so a declined candidate returns.
---

# Groom issues — say what is wrong with a board

A board accumulates cards that someone filed half-finished. Reading them one at a time finds the
sloppy ones and misses the expensive ones, because the costly defects live *between* issues.

**Three commands, and the splits between them are the guarantee.** `/phil:groom-issues` reads and
reports — it holds no write tool at all, so read-only is enforced rather than declared.
`/phil:groom-fix` applies the mechanical column inside a scope the user picks, and can change no card's
existence. `/phil:groom-set` resolves the defects between issues — merge, split, close, group — and asks
before every one. Do not improvise any of them.

The splits are not tidiness. A single command carrying the report in context is the design where a write
gets computed against remembered text instead of read text, and where read-only holds only as long as
nobody adds a tool. Separating them makes the re-read structural and the guarantee mechanical.

They also separate two different blast radii. `/phil:groom-fix` edits bodies and labels; every change it
makes is one edit to undo. `/phil:groom-set` changes **which cards exist** — a merge closes one, a split
creates several, and neither reverses cleanly. Handing both to one command would put the reversible and
the irreversible behind the same consent, and the reversible ones are far more numerous, so the habit
formed on them is the habit carried into the others.

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
4. **Correct labels**, with single-valued families carrying exactly one value — **checkable only where
   the project declares which families are single-valued.** Nothing in a label's name says whether it
   excludes a sibling; GitHub has no scoped labels at all. `documentation` + `enhancement` on one issue
   is a defect or two orthogonal facts depending on a convention no forge records. Absent a declaration
   in the project's `CLAUDE.md`, report this rule **unevaluated**. Do not infer the family from the
   labels in use — that makes the most common pairing the rule, and then the board's habits audit
   themselves.
5. **A `## Chain` section when blocked or related** — the edge *and* the reason it exists, **on both
   ends**. `phil:issue-board` puts the prose line on both issues even where the forge writes the
   reverse edge itself, because the forge records the edge and never the reason. A chain naming an
   issue that does not name back is therefore half-written, and it is the half a reader lands on that
   decides whether they learn why. Cheap to check: the reciprocal is derivable from the same payload.

And it does **not** contain:

- **Session scratch or working state.** It belongs in the git-ignored local surface (ADR-013); a
  board is world-readable.
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

On `glab`, the JSON flag is **`-O`/`--output`**. `-F` is `--output-format` and takes
`details|ids|urls` — hand it `json` and it silently returns the human-readable table. Both commands
return bodies populated, so there is no N+1 and no reason to fetch issues individually.

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

Classify each, because `/phil:groom-fix` acts only on the first column:

| Mechanical — one right answer | Semantic — needs a human |
|---|---|
| A relative file link (404s on GitHub) | No purpose stated |
| An issue reference wrapped in markdown that should be bare | No way to tell when it is done |
| A single-valued label family carrying two values, where the project declares the family | Session scratch in the body |
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
- **Oversized** — a card carrying work that cannot be demonstrated on its own. Name the seam.
- **Overcome by events** — the work landed another way, or the decision behind it was reversed.
- **Ungrouped effort** — a card belonging to a larger effort that says so nowhere. A milestone is a
  goal (`phil:issue-board`); do not invent a second convention.

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

**Closing sets Status on a project board.** Where the project has the closed-item workflow enabled — it
is on for this repo — the card lands in Done by itself, and this command holds no `gh project
item-edit` to put it anywhere else. Say so when you close; a card the user expected to keep triaging
has just left the queue.

### Split

**Numbers are assigned at creation, so the cross-references are a second pass.** Create the new cards
first, collect the numbers the forge hands back, then write the `## Chain` lines. Writing a reference
during creation means writing a number that does not exist yet, and the forge will render it as a link
to whatever else claims it.

**Nothing is inherited.** Labels, milestone, and the chains that pointed at the original do not follow
the split — they are carried deliberately or not at all, and both are decisions. State what you are
carrying to each new card as part of the ask, not after.

**Then decide the original.** A split leaves a card that no longer describes work: it is closed as
superseded, or kept as the container the new cards hang under. That is a second question, and the split
is not finished until it is answered — an original left open beside its own pieces is now the
duplicate this command exists to find.

**A created issue is not a board card.** `gh issue create` puts an issue in the repo and nowhere on the
project; a card that was never `item-add`ed has no Status and is invisible in a kanban grouped by it.
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

On approval, close with the reason **in the same call** (`gh issue close -c`). A comment posted after
the close is silently dropped once the project's close workflow has run, so the reason vanishes and the
card carries no account of why it went.

### Ungrouped effort

A card belonging to a larger effort that says so nowhere. **A milestone is a goal** — #7's convention,
owned by `phil:issue-board`. Consume it; a second grouping convention invented here would make the two
disagree and neither authoritative.

**Joining an existing container and creating a new one are different questions.** Joining is the only
reversible operation in this whole section — one `--milestone` away from undone — so it can be offered
over a group of cards at once, provided the evidence for each is shown beside it. Creating a container
cannot: a goal is a commitment about what the board is for, and this command deliberately cannot make
one. Propose it, hand over the exact call, and stop.

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
wherever the project declares no label family, and the cross-reference row wherever a target cannot be
confirmed pushed. Both then produce no findings, and no findings reads as compliance. Name them, with
the reason:

```
rules 1, 2, 3, 5 evaluated · rule 4 unevaluated (no label family declared in CLAUDE.md)
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

## What this skill must never do

All three commands:

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

`/phil:groom-set` (the set-level loop) additionally:

- Offer a yes-or-no over a finding whose evidence admits more than two outcomes.
- Choose the surviving card of a merge, by number or by any other proxy for the user's judgement.
- Leave references pointing at an issue it closed.
- Write a cross-reference to a card the forge has not yet numbered.
- Leave a split's original open beside its own pieces, or its new cards off the project board.
- Close on board prose alone. The claim that work landed another way is settled in the repository or
  not at all.
- Create a milestone, or treat one card's container as evidence for another's.
- Record a decline anywhere, or let a run of approvals turn the next ask into a formality.

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, the command loader, or
`phil:issue-board`'s body-relevant sections change.
