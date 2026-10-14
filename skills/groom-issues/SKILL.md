---
name: groom-issues
description: Skill bundle for the phil:groom-issues, phil:groom-fix, phil:groom-set and phil:groom-ask commands — reads a whole issue board in one list call per forge — plus one GraphQL call on GitHub for the parent/child edges that call cannot return — and reports what is wrong with it against a stated standard, applies the mechanical fixes inside a scope the user picks, resolves the defects between issues (merge, split, close, group, consolidate a feature decomposed under retired rules or a story spread across feature cards) by asking before each one, and fills in a card that says too little from the user's answers and its own suggestions, labelling where every field's words came from. Derives the defect table fresh every run and stores no grooming marker, so a declined candidate returns. For where the board STANDS rather than what is wrong with it — what is blocked, what is in flight, the next few queued — use phil:board-snapshot instead.
---

# Groom issues — say what is wrong with a board

A board accumulates cards that someone filed half-finished. Reading them one at a time finds the
sloppy ones and misses the expensive ones, because the costly defects live *between* issues.

**Four commands, and the splits between them are the guarantee.**

- `/phil:groom-issues` reads and reports. It holds no `Write` and no `Edit`, so it cannot touch a file.
  Its forge calls must be reads, and since 2026-09-04 that half is a promise, not a scoping: reading a
  parent/child edge needs `gh api graphql`, which also accepts a mutation document. The invariants below
  carry that promise, and nothing else does. Wound: without the grant, the decomposed-feature check
  reported clean on every board it was written for.
- `/phil:groom-fix` applies the mechanical column inside a scope the user picks, and changes no card's
  existence.
- `/phil:groom-set` resolves the defects between issues — merge, split, close, group, consolidate — and
  asks before every one.
- `/phil:groom-ask` fills in a card that says too little, asking, suggesting, and writing what the user
  sanctions.

Run each exactly as its section or file says; improvise none of them.

**The splits buy three things.**

- **A structural re-read.** One command carrying the report in context computes writes against
  remembered text. Separate commands must re-read.
- **Separate blast radii.** `/phil:groom-fix`'s edits each undo in one edit; `/phil:groom-set` changes
  **which cards exist**, and neither a merge nor a split reverses cleanly. One consent over both trains
  the habit formed on the many reversible changes onto the few irreversible ones.
- **Separate provenance.** `/phil:groom-ask` writes what no artifact holds — why a card is wanted. It
  needs consent **plus provenance**: did the human sanction this claim, and does the card record whose
  words carried it. No scoping enforces either.

**REQUIRED BACKGROUND: `phil:issue-board`.** Every forge mechanic — `-R` targeting, label semantics,
absolute-URL rules, dependency links, generated blocks — lives there. Do not guess any of it here.

## The four commands

Each command runs from one place. **Read the command's file whole before its first step**; this file
governs all four.

| Command | Runs | Read |
|---|---|---|
| `/phil:groom-issues` | the scan and its report | this file, whole |
| `/phil:groom-fix` | the mechanical column | `references/fix.md` |
| `/phil:groom-set` | the set-level candidates | `references/set.md` |
| `/phil:groom-ask` | the semantic column | `references/ask.md` |

**Every ask in this skill follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`. Load it
before the first `AskUserQuestion` call.**

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

   **`wave: *` is single-valued by default, with no declaration.** In a repo holding `.nwave/` or
   `docs/feature/`, `phil:nwave-issue-board` makes it so: *"the wave label is single-valued and must be
   swapped, not added"*. A feature walked DISCUSS→DELIVER otherwise carries four wave labels, and every
   command reports success while the record of where it stands becomes unreadable. Report the
   accumulation as a mechanical defect. A project overrides this only by declaring `wave: *`
   multi-valued in as many words.

   Match a family on the prefix before `::` or `: ` — `wave::deliver` where scoped labels exist and
   `wave: deliver` where they do not are the same family, and a board may carry both spellings.

   **A declaration is a bullet under the project's `## Issue board` section in `CLAUDE.md`** naming a
   family and calling it single-valued or multi-valued, per the setup block in `phil:issue-board`.
   Neither a label's own description nor the labels in use counts: the first is not authoritative, and
   inferring the rule from the board's habits lets the board audit itself.
5. **A `## Chain` section when blocked or related** — the edge *and* the reason it exists, **on both
   ends**. `phil:issue-board` puts the prose line on both issues even where the forge writes the
   reverse edge itself, because the forge records the edge and never the reason. A chain naming an
   issue that does not name back is therefore half-written, and it is the half a reader lands on that
   decides whether they learn why. Cheap to check: the reciprocal is derivable from the same payload.

And it does **not** contain:

- **Session scratch or working state *typed outside a generated region*.** A board is world-readable, and
  hand-written scratch belongs in the git-ignored local surface (ADR-013). Session state **inside** the
  `nwave:status` markers is intended: `/phil:handoff` projects the why, the next action and the
  diversion stack there. Reporting that generated projection as a body defect flags the correct shape.
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

### Judging prose is taste; composing it is not

**Rules 1, 2 and 5 check that a purpose, a done-condition and a reason are PRESENT. None of the five
items asks how anything READS.** The discriminator is who composed the words:

- **Judging prose a human wrote is taste. It stays out.** A scan that flagged someone's style would be
  the taste-policing this standard's opening sentence refuses, and no rule here licenses it. Presence is
  all those rules check — never whether what is present is well written.
- **Composing prose yourself is not taste at all.** Applying a house standard to text this command family
  writes polices nobody.

**So the standard for composed text is `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`**, and it reaches only
what the commands this skill bundles compose onto a card: the fields elicitation writes (per the
provenance clause in `references/ask.md`) and the comments `groom-set` leaves on an irreversible operation.
`groom-issues` and `groom-fix` compose nothing that reaches a card and say so in their own files;
`phil:rank-issues` owns its own surface and its own citation. **Concision is one of the standard's
eleven principles of composition** — active voice, positive form, concrete language, parallel structure
and the emphatic word last are the others that bear here. Read it as *compose well*, never as *compose
short*.

**Naming the standard is the mechanism, and naming is not running an editor as a step.** Nothing here
authorises a pass over a body already written; the standard governs composition at the moment text is
drafted.

**The scan is unchanged. No style rule is added to it, and adding one would be a misreading.** A style
item in the scan is judging, which the first bullet forbids.

**Two citations have no fixture yet:** `groom-set`'s comments on an irreversible operation, and
`phil:rank-issues`' recorded basis. `self-test/44` pins the third, a `you wrote` field left untouched.

## Scan once, derive fresh

**One call per forge**, bodies included:

```sh
gh issue list -R <owner/repo> --state open --json number,title,body,labels,milestone --limit 200
glab issue list -R <group/project> --output json --per-page 100
```

On `glab issue list` the JSON flag is `-O`/`--output`, **not `-F`** — `phil:issue-board` owns the
mechanism, in its `references/gitlab-cli.md` under *`glab`'s JSON flag differs per subcommand — check before you type it*. Both commands
return bodies populated, so fetch no issue individually.

**Then one more call on GitHub, for the parent/child edges the first call cannot return.** `gh issue
list --json` exposes no `parent` and no `subIssues`, and no flag adds one; both are GraphQL-only. Without
this the decomposed-feature class loses the signal its own evidence table ranks first, and reports clean
on exactly the boards it exists for:

```sh
gh api graphql -f query='query($o:String!,$r:String!){ repository(owner:$o,name:$r){
  issues(first:100,states:OPEN){ nodes { number
    parent { number }
    subIssues(first:50){ nodes { number } } } } } }' -f o=<owner> -f r=<repo>
```

**One call, paginated if the board needs it — not one per issue.** The whole-board read is the design;
an N+1 here would reintroduce the cost the single list call exists to avoid.

**The query is copied from `phil:issue-board`'s `references/hierarchy.md` (*Writing a sub-issue edge is a flag; READING one is
GraphQL*) so the scan runs from this file alone. If the two ever disagree, `phil:issue-board` wins.**

**This call is a read and must stay one.** `gh api graphql` accepts a mutation document, so nothing in
the grant stops a write — only the invariants below do. Send `query` documents only — never a
`mutation` document — and hand anything the scan reported to the command that owns it.

**On GitLab the parent edge stays unreadable, so report the check unevaluated, per *Reporting*.**
GitLab has no stable issue-to-issue parent edge: epics are Premium, and the work-item hierarchy is an
*Experiment* (`phil:issue-board`'s `references/hierarchy.md`, *A parent's "N of M done" counts different things on each forge*). So
`glab api` is not granted; it would widen the promise for an oracle that does not exist.

**Re-read a card immediately before writing it, on every writing command.** Fetch the issue being
edited rather than acting on any earlier copy. If its body moved since that read, report what moved
and when, and overwrite nothing: the forge records the session as last author, and whoever's paragraph
vanished cannot see that a groom run did it. Each command's file says what it re-reads beyond the card.

**Derive the defect table fresh every run, and store no grooming marker** — no `groomed` label, no
timestamp block, no state file. A stored marker becomes a second authority the moment somebody edits a
groomed issue, which `phil:issue-board` forbids under *One system of record per scope*.

**So a declined candidate returns next run, and the report says so plainly.** Unstated, it reads as the
tool forgetting, and the user asks for the marker this rule refuses.

## The defect table

Every finding names the rule it violates and quotes the evidence. A finding without both is an
opinion, and this skill does not report opinions.

Classify each, because the columns have different actors: `/phil:groom-fix` acts on the mechanical column,
and `/phil:groom-ask` on the semantic one (*Eliciting the semantic content*, in `references/ask.md`).
Neither crosses.

| Mechanical — one right answer | Semantic — needs a human |
|---|---|
| A relative file link (404s on GitHub) | No purpose stated |
| An issue reference wrapped in markdown that should be bare | No way to tell when it is done |
| A single-valued family carrying two values — `wave: *` always, a project-local family where declared | Session scratch typed **outside** a generated region |
| A missing cross-reference whose target is unambiguous | A second copy of forge-kept state the body's argument leans on |
| A second copy of forge-kept state that only restates it | Deciding which of those two a copy is |
| A `## Chain` line naming an issue that does not name back | Which end of a one-sided chain is right |

**A one-sided chain is the cheapest finding here and the easiest to write.** Detection is pure
derivation: collect every `#N` inside a `## Chain` section, and flag any whose target is open and
carries no reciprocal line. It is mechanical because the missing half is *stated on the other issue* —
nothing has to be invented, only mirrored. What is **not** mechanical is which end is right when the
two disagree about the reason; that is a human's.

Expect it from careful authors: on one real run, three of four chains written by an author who had
just read this rule were one-sided.

**The cross-reference row needs two things, and only one of them is a command away.** First, a
discriminator, because "unambiguous" alone made this row a judgement call wearing a mechanical label:
a reference is a finding when it names **a specific file a reader would open to follow the argument**.
A repository-root file (`CLAUDE.md`), a bare directory (`rules/`, `agents/`), a glob (`commands/*.md`)
and an ambiguous basename (`SKILL.md`, where twenty exist) are **not** findings — the first two are one
click from any page, and the last two have no single target to link. Without that line, two references
in the same body get opposite treatment and the column stops meaning "one right answer".

Second, the check itself. "Unambiguous" also means the target exists and is pushed, which
`phil:issue-board` establishes with
`git ls-tree origin/<default-branch> -- <path>` — outside the scan's grant, which holds no `git` verb,
and deliberately so. A bare file path in a body is therefore a **candidate**, not a
finding: report it as unverified and say what would settle it. Promoting it anyway produces the failure
`phil:issue-board` warns about from the other direction — a link that renders, passes a read-back, and
404s for everyone else.

**A stale copy of forge state is two defects wearing one name.** Where the copy only restates what the forge holds — a prose
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

**A missing `Work this with:` line is not a body defect.** `phil:nwave-issue-board` generates it into
the delimited block; its absence is a publishing question, and hand-writing it would be typing into a
generated region.

## Cross-issue candidates — the scan surfaces, never acts

These cannot be found by reading one issue, which is why the scan is whole-board. `/phil:groom-issues`
reports each with its evidence and stops; resolving them is `/phil:groom-set`, and is ask-first there.

- **Duplicates** — quote the overlapping content from both. Partial overlap is the real case and is
  not automatically a merge; it may be a split or a dependency.
- **Oversized** — a card carrying work that **cannot be demonstrated on its own**. Name the seam.

  **Judge demonstrability, never size.** A card holding a whole feature is large and demonstrable, so it
  passes; on a board where one issue *is* one feature, it is the intended shape. A story card holding
  several features passes too: one owner works them in sequence. Judged by size, every correct card
  would be proposed for splitting every run, and with no marker a declined split returns forever.
  `phil:issue-board`'s split clause is about concurrency — two halves in different columns at once —
  and the concurrency class below catches the wrong story shape.
- **Two or more features in flight on one story card** — two or more rows **of the feature roster**
  carry the state word `in progress`. **Quote every such feature by name, with its roster row.**

  **Read the state WORD in the feature roster, never the `▶` glyph.** A story block's slice roster uses
  `▶` for `current`, so a correct story card with one member in flight renders two `▶` rows
  (`phil:nwave-issue-board`, *two glyphs are reused, not one*). Two or more members, not exactly two.

  **The scan reports this and never offers.** Confirming the state words against the artifacts needs
  the fold, which the scan cannot run; name `/phil:groom-set`. Two members in flight means two people,
  which is `phil:issue-board`'s split clause — *"two halves sit in different columns at the same time
  only when two people are working them at once."* Resolution offered: split into feature cards under a
  goal.
- **Overcome by events** — the work landed another way, or the decision behind it was reversed.
- **Ungrouped effort** — a card belonging to a larger effort that says so nowhere. A milestone is a
  goal (`phil:issue-board`); do not invent a second convention.

  **A goal holds *cards*; a story holds *feature directories*.** A goal is a milestone: it has a due
  date and groups unrelated work by design. A story is itself a card and never holds another. Milestones
  do not nest, a story is not a milestone, and neither replaces the other.
- **Features of one story, carded separately** — several open cards that are each a whole **feature**, whose
  `docs/feature/<id>/feature-delta.md` files declare the **same `Story:` slug**. Directly parallel to
  *decomposed feature* one level up: the unit that should be one card has been spread across several.

  **Where nothing on the forge groups these cards, *ungrouped effort* also fires, and this class
  supersedes it.** (Members sharing a milestone are grouped, so ungrouped effort does not fire.) Its
  resolution proposes a milestone, a goal; the right container is a story card. Where this class's
  evidence reaches offer tier, offer only this one.

  **Evidence is ranked as decomposed-feature's is**, because consolidating is irreversible: a `Story:`
  line at column 0 in each member's delta, **confirmed on the default branch with `git ls-tree`**,
  licenses an **offer**; a shared title prefix or a common milestone licenses a **report only**.

  **`git ls-tree` is `/phil:groom-set`'s grant, not the scan's**, so the scan reports the candidate and
  names that command; it never offers here.

  **The directory decides which class fires.** Cards whose bodies name the **same** `docs/feature/<id>/` are a *decomposed feature* —
  slices of one feature. Cards naming **different** feature directories that declare the **same** `Story:`
  slug are this class. At most one holds; where the scan cannot tell which, report both and offer
  neither.
- **Decomposed feature** — several open cards that are **slices of one feature**, on a board where one issue
  is one feature (`phil:nwave-issue-board`). Report the set with the evidence that ties them together.

  **The retired granularity rule made these cards, and no other class fires on them** — not duplicates,
  not oversized, not overcome by events, and, where a parent groups them, not ungrouped. Without this
  class a board full of them reports clean.

  **In shape (c) *ungrouped effort* also fires, and this class supersedes it.** With no parent and no
  closed original, nothing groups the cards; ungrouped effort would propose a milestone where the right
  answer is a feature card. Where decomposed-feature evidence reaches offer tier, offer only this one.

  **The evidence is ranked, because consolidating is irreversible:**

  | Signal | What it licenses |
  |---|---|
  | A real parent/child edge (sub-issues) | **Offer.** The forge asserts it; nothing is inferred. |
  | Bodies naming the same `docs/feature/<id>/`, **confirmed present in the repo** | **Offer**, once confirmed. |
  | `slice NN` in the titles | **Report, never offer.** A naming convention is a habit, not a fact. |
  | A shared milestone | **Nothing at all.** A milestone is a goal and holds unrelated work by design. |

  **Read tier 1 on GitHub; the scan's GraphQL call returns it.** A ranking whose top row is unreadable
  inverts the class, firing only on weak evidence. Wound: until 2026-09-04 every properly parented board
  came back clean.

  **On GitLab tier 1 is unreadable: report it unevaluated, and evaluate tiers 2 and 3 as normal.** Say
  the class was weakened, not dark.

  **Tier 2 needs the repository, not the body's word for it.** *Overcome by events* (`references/set.md`) already refuses to treat
  board prose as evidence about the world — the claim "is settled in the repository or not at all" — and a body
  naming a path is board prose. Confirm the directory exists with `git ls-tree`, which `/phil:groom-set` holds.
  Unconfirmed, tier 2 drops to report-only alongside a title.

  Quote the evidence rather than characterising it. *"These look like slices of one feature"* is the finding
  restating its own conclusion.

## Reporting

Lead with the shape of the board, not the findings:

```
57 issues read · 51 clean · 3 with body defects · 2 duplicate candidates · 1 oversized ·
1 decomposed feature (4 cards)
```

Then the defects, grouped by issue, each citing its rule and evidence. Then the cross-issue
candidates. Then, if anything was declined on a previous run, the note that it will reappear.

**A clean board is reported clean, with only the findings the board holds.** A manufactured finding
teaches people to stop running the tool.

**A partial read may never make a completeness claim.** If pagination failed, the forge was
unreachable, or the limit truncated the list, say the read was partial and report *only* what was
found. "52 clean" over a partial scan is the single most misleading thing this skill can emit,
because it is a claim about issues nobody looked at.

**A rule that could not be evaluated is not a rule that passed.** Three checks go dark routinely: rule 4
wherever a **project-local** family is undeclared, the cross-reference row wherever a target cannot be
confirmed pushed, and **the decomposed-feature parent edge on every GitLab board**, which has no stable
edge to read. All three then produce no findings, and no findings reads as compliance. Name them, with
the reason:

```
rules 1, 2, 3, 5 evaluated · rule 4 partly unevaluated (`wave: *` checked — normative;
  `documentation`/`enhancement` undeclared in CLAUDE.md)
· 6 unlinked paths unverified (target check needs git, out of scope here)
· decomposed feature: tiers 2 and 3 checked; parent edge unread (GitLab has no stable
  issue parent to read — on GitHub this tier is read)
```

The last line is owed **only on GitLab**, and only where the class had a candidate to settle. On GitHub
the edge is read, so saying it was not is a false caveat — which erodes the caveats that are true.

It is the partial-read failure one rule narrower, and it hides better: the issue count is honest, so
nothing in the summary looks incomplete.

**Say a check went dark only when it had something to decide.** A board where no issue carries two
labels does not need rule 4's oracle, and reporting it unevaluated there is boilerplate — which is how
a caveat stops being read by the run that needs it. The note is owed when a candidate existed and the
check could not settle it: two labels and no declared family, an unlinked path and no way to confirm
the target. No candidate, no note.

## Decision outcomes

Report the outcome by name, every run. Each command draws from its own row:

| Command | First, before any write | Then exactly one of | Alongside, when it applies |
|---|---|---|---|
| `/phil:groom-issues` | — | `REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL` | `REPORT-UNEVALUATED` · `SURFACE-CANDIDATE` · `NOT-A-DEFECT` · `NO-MARKER` · `READ-ONLY` |
| `/phil:groom-fix` | `SCOPE-FIRST` | `APPLY-MECHANICAL` · `STALE-REREAD` · `REFUSE-GENERATED` | `LEAVE-SEMANTIC` |
| `/phil:groom-set` | `ASK-SET-LEVEL` | `APPLY-MERGE` · `APPLY-SPLIT` · `APPLY-CONSOLIDATE` · `DECLINE-NO-TRACE` · `REFUSE-UNVERIFIED` · `REFUSE-CONCURRENT` · `REFUSE-RESLICE` · `REFUSE-UNGRANTED` | `REDERIVE-BETWEEN` |
| `/phil:groom-ask` | `ASK-CONTENT` | `WRITE-ELICITED` · `WRITE-PARTIAL` · `DECLINE-NO-TRACE` · `STALE-REREAD` · `REFUSE-GENERATED` — or `ASK-CONTENT` again | — |

**What each outcome claims:**

- **`REPORT-UNEVALUATED`** — a rule had a candidate and no oracle. A parent edge that cannot be read,
  on every GitLab board, reports here; it has no outcome of its own.
- **`SURFACE-CANDIDATE`** — a cross-issue candidate reported, not acted on. Additive; it never stands
  alone. **A board carrying a surfaced candidate is not clean, so the terminal is `REPORT-DEFECT`.
  `REPORT-CLEAN` is unavailable on any run that surfaced a candidate.** Fixtures `07` and `45` pin it.
- **`NOT-A-DEFECT`** — something that looks like a finding and is not.
- **`NO-MARKER`** — the run read and wrote no grooming marker, and re-derived everything; a candidate
  that reappears says why (fixture `06`).
- **`REFUSE-UNVERIFIED`** — a candidate whose evidence would not confirm, such as overcome by events
  with nothing in the repository behind it. Reported with the check that ran, and never put to a vote.
- **`READ-ONLY`** — every forge call this run made was a read. The grant permits a mutation, so this
  is a claim about the run, not about the tool list.
- **`LEAVE-SEMANTIC`** — a semantic defect was reported and left.
- **`REDERIVE-BETWEEN`** — an apply invalidated a later candidate.
- **`APPLY-CONSOLIDATE`** — names the shape it took, because each has a different blast radius: for a
  decomposed feature, an open parent, a reopened closed original or a newly created card; for a story,
  a reopened closed story card or a newly created one. It also states what the parent's rollup now
  shows, since nobody reading the card can tell inflation from completion.
- **`REFUSE-CONCURRENT`** — members in flight at once, so consolidating them is refused on verified
  evidence. Nobody declined, and the evidence is good.
- **`REFUSE-RESLICE`** — a split was asked for over a *feature*, which means re-slicing its roadmap, not
  changing which cards exist. Name the operation asked for and the one that would be needed.
- **`REFUSE-UNGRANTED`** — the resolution needs a call this command does not hold: shape (b)'s reopen, a
  Status write, or a rollup read. **Hand over the exact calls and stop.** It refuses to act, never to
  report. A run that silently does less than it said, or reports `APPLY-CONSOLIDATE` for a shape it could
  only half-complete, is the failure it prevents.
- **`DECLINE-NO-TRACE`, `STALE-REREAD` and `REFUSE-GENERATED` mean the same on every command** — a
  decline that stores nothing, a body that moved since the read, and a write whose target belongs to a
  generator. At `/phil:groom-ask`, a card can carry a generated `nwave:status` block and still state no
  purpose; where the generated region is the whole body, elicited prose has no room outside the
  markers, so refuse rather than approximate.
- **`WRITE-ELICITED` and `WRITE-PARTIAL` need provenance on every written field** — one of `you wrote` ·
  `you accepted my suggestion` · `you edited my suggestion` · `I rephrased your answer` — and an
  unlabelled field fails the outcome however the body reads. Beside `I rephrased your answer` or
  `you edited my suggestion`, show the answer next to the written form.

**The first column is a precondition, not an alternative.** An apply that reports only its terminal
outcome has not said whether it asked, and *did it ask* is the property the writing commands exist to
guarantee. `REFUSE-UNVERIFIED` is the exception: an unconfirmed candidate is not put to a vote, so
nothing was asked.

**`ASK-CONTENT` collects content, not consent** — the content is the deliverable. A run reporting
`WRITE-ELICITED` without `ASK-CONTENT` wrote a body nobody sanctioned.

**`ASK-CONTENT` alone is a legal terminal, and the only one that resolves nothing.** A run that asked and
received no answer, edit, replacement or decline reports `ASK-CONTENT` again and stops — fixtures `32`
and `29`. Report `DECLINE-NO-TRACE` only when the user refused; a user who has not answered yet did not.

## Invariants

All four commands:

- Store no grooming marker in any form, including a record of what was declined, and read none.
- Give every finding the rule it violates and the evidence for it.
- Claim completeness only over a complete read.
- Keep a rule that could not be evaluated distinct from one that was satisfied, wherever either is
  reported.
- Leave a missing generated line out of the body defects.
- Merge, split, close, group or consolidate only on an explicit answer to a question that offered that
  outcome.
- Leave a **generated** projection out of the body defects. Session state inside the `nwave:status`
  markers is intended; only typed scratch outside them is a finding.
- Judge a card oversized on demonstrability alone — never on its size, its section count or a generated
  block — and propose splitting no **feature card or story card** on size. A size-keyed reading
  oscillates the board.

`/phil:groom-issues` (the scan) also:

- **Writes nothing** — no issue edits, labels, comments or milestones. It holds no `Write` and no
  `Edit`, so a session that finds itself needing one has misread the command.
- **Sends only `query` documents through `gh api graphql`, never a `mutation` document.** No tool
  boundary backs this one. Refuse rather than improvise: a resolution that needs a forge write is
  `/phil:groom-set`'s, and handing it over is the design.
- **Confines the graphql grant to the parent edge alone.** Anything else it could reach is a check nobody
  has reasoned about, arriving without a rule, an evidence tier or a fixture.

`/phil:groom-fix` (the apply) also:

- Writes only after the user has picked a scope.
- Takes consent from the user's answer alone — never from the mechanical classification, or from a
  small population.
- Stays inside the chosen scope, even for a mechanical fix.
- Applies only edits computed against the issue's text as it stands after its last change.
- Writes nothing inside a generated region, nor just outside it to approximate the fix.
- Leaves every semantic defect untouched — no drafted acceptance criteria, rewritten purpose or decided
  granularity. It reports them and leaves them, every time.
- Starts every run with no scope. Nothing is stored between runs; a remembered scope is the marker this
  skill refuses, grown back in another shape.

`/phil:groom-ask` (the elicitation loop) also:

- **Writes only words the human has sanctioned.** Drafting is permitted; silence, "ok", or any reply
  that is neither an accept, an edit nor a replacement adopts no draft.
- **Labels every written field with its provenance**, and shows the answer beside the written form
  wherever it claims `I rephrased your answer` or `you edited my suggestion`.
- Presents the card and the rule that failed before every question.
- **Leaves a rule that passed as written.** A purpose already satisfying rule 1 is out of reach; only
  what this run elicited may be rephrased.
- Writes a partial answer partially. Offering the withheld half is permitted; writing it unasked is not.
- **Asks only about rules the scan reported failing.** The questions come from the findings.
- Works one card per run — no batch, no apply-to-all, no "the same again for the next card".
- Refuses to overwrite a body that moved since the read, and hands back the answers and any draft.
- **Writes elicited prose nowhere inside a generated region, nor just outside it to approximate
  placement.**
- Leaves mechanical defects, labels, links and which cards exist to their own commands.

`/phil:groom-set` (the set-level loop) also:

- Offers every outcome the evidence admits; a yes-or-no only where the evidence admits exactly two.
- Leaves the surviving card of a merge to the user — never to the lower number or any other proxy for
  the user's judgement.
- Re-points every reference to an issue it closed.
- Writes a cross-reference only to a card the forge has already numbered.
- Settles a split's original — closed as superseded, or kept as the container — and adds each new card
  to the project board.
- **Removes a child's parent edge before closing it.** A closed child still counts toward the parent's
  completion.
- **Searches closed issues before concluding that no feature card or story card exists.** A previous
  split may have closed the original as superseded, and minting a second one buries the first.
- **Treats title evidence alone as report-only.** `slice NN` in a title is a habit: it licenses a
  report, never an irreversible write. A shared milestone licenses nothing.
- **Hands over every reopen with its Status call.** `gh issue reopen` does not restore the field, so a
  card reopened alone sits OPEN in Done and no view flags it.
- Splits no feature into slice cards, and no story card on size. Splitting an ordinary card creates
  cards; splitting a feature means re-slicing its roadmap, which is not this command's to do.
- Closes an overcome-by-events candidate only on evidence from the repository. The claim that work
  landed another way is settled there or not at all; board prose alone settles nothing.
- Creates no milestone; where one is the right container, it proposes it and hands over the exact
  call. One card's container is no evidence for another's.
- Records no decline anywhere, and puts each ask to the user afresh however many approvals preceded it.

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, its `references/`, a command loader, or
`phil:issue-board`'s body-relevant sections change.
