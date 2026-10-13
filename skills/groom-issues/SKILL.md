---
name: groom-issues
description: Skill bundle for the phil:groom-issues, phil:groom-fix, phil:groom-set and phil:groom-ask commands — reads a whole issue board in one list call per forge — plus one GraphQL call on GitHub for the parent/child edges that call cannot return — and reports what is wrong with it against a stated standard, applies the mechanical fixes inside a scope the user picks, resolves the defects between issues (merge, split, close, group, consolidate a feature decomposed under retired rules or a story spread across feature cards) by asking before each one, and fills in a card that says too little from the user's answers and its own suggestions, labelling where every field's words came from. Derives the defect table fresh every run and stores no grooming marker, so a declined candidate returns. For where the board STANDS rather than what is wrong with it — what is blocked, what is in flight, the next few queued — use phil:board-snapshot instead.
---

# Groom issues — say what is wrong with a board

A board accumulates cards that someone filed half-finished. Reading them one at a time finds the
sloppy ones and misses the expensive ones, because the costly defects live *between* issues.

**Four commands, and the splits between them are the guarantee.** `/phil:groom-issues` reads and
reports — it holds no `Write` and no `Edit`, so it cannot touch a file, and its forge calls **must** be
reads, which since 2026-09-04 is a promise rather than a scoping.

**Half of that is enforced and half is now a promise, which is a downgrade and is recorded as one.**
Until 2026-09-04 the whole guarantee was mechanical: no write tool of any kind, and a `Bash` scoped to
`gh issue list` and `glab issue list`. Reading a **parent/child edge** needs `gh api graphql`, which
accepts a mutation document, so granting it removed the forge half of the enforcement. The trade was made
deliberately for issue #30, because the alternative was a decomposed-feature check that reports clean on
every board it was written for — see *Cross-issue candidates*. `Write` and `Edit` are still absent, so
the file half stays mechanical; the forge half now lives in this skill's never-do list and the command's
prose, and nothing but those forbids a mutation. A helper script was rejected rather than overlooked: no
grant names one script, only its interpreter, and an interpreter cannot honestly join the read-only verb
list in `scripts/check-readonly-commands.py`.
`/phil:groom-fix` applies the mechanical column inside a scope the user picks, and can change no card's
existence. `/phil:groom-set` resolves the defects between issues — merge, split, close, group, consolidate — and asks
before every one. `/phil:groom-ask` fills in a card that says too little, asking, suggesting, and
writing what the user sanctions. Do not improvise any of them.

The splits are not tidiness. A single command carrying the report in context is the design where a write
gets computed against remembered text instead of read text, and where read-only holds only as long as
nobody adds a tool. Separating them makes the re-read structural, and it keeps `Write` and `Edit` out of
the scan's reach whatever happens to its forge calls.

**That last clause used to read "and the guarantee mechanical", and the grant change makes the shorter
sentence false.** It is narrowed rather than deleted: the separation still buys the re-read and still
buys the file half. What it no longer buys is a scan that could not write to the forge if it tried.

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

### Judging prose is taste; composing it is not

**Rules 1, 2 and 5 check that a purpose, a done-condition and a reason are PRESENT. Not one of the five
items asks how anything READS**, and a body can satisfy every item while being passive, padded and twice
the length it needs. (Rules 3 and 4 ask neither question: a link's form and a family's cardinality are
not prose at all.) That gap is deliberate on one side and was an oversight on the other, and the
discriminator is checkability:

- **Judging prose a human wrote is taste. It stays out.** A scan that flagged someone's style would be
  the taste-policing this standard's opening sentence refuses, and no rule here licenses it. Presence is
  all those rules check — never whether what is present is well written.
- **Composing prose yourself is not taste at all.** Applying a house standard to text this command family
  writes polices nobody. That is the half nothing covered until 2026-09-04, when twelve board-family
  files were measured naming no prose standard while `rules/writing.md` was cited by five other surfaces.

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

**A citation is meant to ship a fixture with it, because a mention that changes nothing is this repo's
recorded defect — and two of this family's citations do not yet have one.** `self-test/44` pins a
`you wrote` field left untouched; `groom-set`'s comments on an irreversible operation, and
`phil:rank-issues`' recorded basis, are cited and unpinned. Named rather than implied: an unstated gap
in a rule about unenforced mentions is that rule failing in its own terms.

## Scan once, derive fresh

**One call per forge**, bodies included:

```sh
gh issue list -R <owner/repo> --state open --json number,title,body,labels,milestone --limit 200
glab issue list -R <group/project> --output json --per-page 100
```

On `glab issue list` the JSON flag is `-O`/`--output`, **not `-F`** — the mechanism and its silent
failure are `phil:issue-board`'s, under *`glab`'s JSON flag differs per subcommand — check before you
type it*. **Scoped to this subcommand deliberately**: that section retired the blanket rule this line
used to cite, and the claim survives only for `glab issue list`, which is the only one the scan uses. Both commands return
bodies populated, so there is no N+1 and no reason to fetch issues individually.

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

**The query is duplicated from `phil:issue-board` (*Writing a sub-issue edge is a flag; READING one is
GraphQL*) on purpose, and that skill owns it.** This file's own rule is that every forge mechanic lives
there and none is guessed here — so a second copy needs a reason. It is this: the scan must be runnable
from this file alone, and a reader who has to load the reference skill to learn the shape of a call the
scan makes on every GitHub board is one indirection away from skipping it. **If the two ever disagree,
`phil:issue-board` wins.**

**This call is a read and must stay one.** `gh api graphql` accepts a mutation document, so nothing in
the grant stops a write — only the never-do list below does. Never send a document whose operation is
`mutation`, and never reach for this call to *do* something the scan reported.

**On GitLab tier 1 stays unreadable, and that is not the grant being stingy.** GitLab has no stable
issue-to-issue parent edge to read: epics are Premium, and the work-item hierarchy that would carry one
is an *Experiment* — both per `phil:issue-board`, under *A parent's "N of M done" counts different things
on each forge*. So `glab api` was **not** granted, because widening the promise buys an oracle that does
not exist. On GitLab the parent-edge check has no oracle and is **reported unevaluated**, per *Reporting*.

Stated rather than left to be discovered: a class that works on one forge and goes silently dark on the
other is this skill's own recurring defect, and the whole point of issue #30 was that the dark half
reported clean.

**Re-read a card immediately before writing it, on every writing command.** Fetch the issue being
edited rather than acting on any earlier copy. If its body moved since that read, report what moved
and when, and overwrite nothing: the forge records the session as last author, and whoever's paragraph
vanished cannot see that a groom run did it. Each command's file says what it re-reads beyond the card.

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
`git ls-tree origin/<default-branch> -- <path>` — outside the scan's grant, which holds no `git` verb,
and deliberately so. A bare file path in a body is therefore a **candidate**, not a
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

  **A story card is the same argument one level up, and the paragraph is extended rather than edited.**
  A card holding several nWave features is larger still, holds several demonstrable things, and **passes**
  — the features are worked sequentially by one owner, so no two of them occupy different columns at
  once. The oscillation reasoning transfers verbatim: judged by size a story card would be proposed for
  splitting every run, the family stores no marker, and a declined split has to be declined forever while
  an accepted one only has to be accepted once. **The wrong shape is caught by the concurrency signal
  below, which is a different oracle reaching a different verdict — not by loosening this one.**
- **Two or more features in flight on one story card** — two or more rows **of the feature roster**
  carry the state word `in progress`. **Quote every such feature by name, with its roster row.**

  **Scope the evidence to the feature roster and read the state WORD, never the glyph.** A story block
  carries two tables and `▶` means different things in each — `in progress` in the feature roster,
  `current` in the slice roster (`phil:nwave-issue-board`, *two glyphs are reused, not one*). So a
  perfectly correct story card with **one** member in flight already renders two `▶` rows: one for that
  member, one for its current slice. **A check counting `▶` fires on every correct story card**, which is
  the false positive this class exists not to produce.

  **Stated for any number, not exactly two.** Three concurrent members is reachable, and a rule written
  at arity two either misses the third or has to be re-derived to include it.

  **The scan reports this and never offers.** The state words are readable from the card's body, but
  confirming them against the artifacts needs the fold, which the scan cannot run. Report, and name
  `/phil:groom-set` — the same split as the unlinked-path candidate above. A story
  is worked sequentially by one owner, so two concurrent members means two people, which is exactly the
  case `phil:issue-board`'s split clause covers: *"two halves sit in different columns at the same time
  only when two people are working them at once."* Resolution offered: split into feature cards under a
  goal. **This is that shipped rule read at a new scale, not a new granularity rule** — which is what
  lets the oversized rule above stay untouched.
- **Overcome by events** — the work landed another way, or the decision behind it was reversed.
- **Ungrouped effort** — a card belonging to a larger effort that says so nowhere. A milestone is a
  goal (`phil:issue-board`); do not invent a second convention.

  **A goal and a story are both containers and they are not interchangeable. The discriminator:
  a goal holds *cards*; a story holds *feature directories*.** A goal is a milestone — it has a due date,
  groups unrelated work by design, and survives new cards arriving. A story is itself a card and can never
  hold another. Positionally: a list of issues is a goal; the inside of one issue is a story. Milestones
  do not nest, a story is not a milestone, and neither replaces the other.
- **Features of one story, carded separately** — several open cards that are each a whole **feature**, whose
  `docs/feature/<id>/feature-delta.md` files declare the **same `Story:` slug**. Directly parallel to
  *decomposed feature* one level up: the unit that should be one card has been spread across several.

  **Where nothing on the forge groups these cards, *ungrouped effort* also fires and this class supersedes
  it** — conditional, exactly as the decomposed-feature class states it, because members sharing a
  milestone *are* grouped and ungrouped effort then does not fire at all — but ungrouped effort's resolution proposes a **milestone**, which is a goal,
  and the right container here is a **story card**. Where this class's evidence reaches offer tier, offer
  only this one. Offering both invites a goal filed around work that needs a different kind of container,
  which is precisely the confusion the discriminator above exists to prevent.

  **Evidence is ranked as decomposed-feature's is**, because consolidating is irreversible: a `Story:`
  line at column 0 in each member's delta, **confirmed on the default branch with `git ls-tree`**,
  licenses an **offer**; a shared title prefix or a common milestone licenses a **report only**.

  **`git ls-tree` is `/phil:groom-set`'s grant, not the scan's.** The scan therefore reports the candidate
  and names the command that can confirm it; it never offers here. The scan surfaces, it never acts.

  **Which class fires is decided by the directory, and the test is written down here so it is not
  re-invented.** Cards whose bodies name the **same** `docs/feature/<id>/` are a *decomposed feature* —
  slices of one feature. Cards naming **different** feature directories that declare the **same** `Story:`
  slug are this class. At most one holds; where the scan cannot tell which, report both and offer
  neither.
- **Decomposed feature** — several open cards that are **slices of one feature**, on a board where one issue
  is one feature (`phil:nwave-issue-board`). Report the set with the evidence that ties them together.

  **This class exists because the retired rules produced it.** Under the old granularity rule a slice was
  independently demonstrable, so it was cardable — and this family's own split would have cut a feature into
  exactly these cards. **Grooming now meets the wreckage of its own earlier advice**, and none of the
  other classes above fires on it: not duplicates (a decomposition has no overlapping content to quote), not
  oversized (each card is small and demonstrable), not overcome by events, and — in shapes (a) and (b) — not
  ungrouped, because a parent groups them. A board full of them reports **clean**, correctly and uselessly.

  **In shape (c) *ungrouped effort* also fires, and this class supersedes it.** With no parent and no closed
  original, nothing on the forge groups the cards, so both are true — but ungrouped effort's resolution
  proposes a **milestone**, which is a goal, where the right answer is a feature card. Where
  decomposed-feature evidence reaches offer tier, offer only this one. Offering both invites a goal filed
  around work that needs a different kind of container.

  **The evidence is ranked, because consolidating is irreversible:**

  | Signal | What it licenses |
  |---|---|
  | A real parent/child edge (sub-issues) | **Offer.** The forge asserts it; nothing is inferred. |
  | Bodies naming the same `docs/feature/<id>/`, **confirmed present in the repo** | **Offer**, once confirmed. |
  | `slice NN` in the titles | **Report, never offer.** A naming convention is a habit, not a fact. |
  | A shared milestone | **Nothing at all.** A milestone is a goal and holds unrelated work by design. |

  **Tier 1 is readable on GitHub, and was not until 2026-09-04.** The edge is GraphQL-only; the scan now
  makes that read, per *Scan once, derive fresh*. **This was the whole of issue #30**: the table has ranked
  the edge first since 0.51.0 while the command could not see one, so every board whose slice cards were
  properly parented — the boards this class was written for — came back clean. A ranking whose top row is
  unreadable does not degrade to the rows below it; it inverts the class, firing only on the weak evidence
  and never on the strong.

  **On GitLab tier 1 remains unreadable, and is reported unevaluated rather than skipped.** There is no
  stable issue-to-issue parent edge there to read. Tiers 2 and 3 still evaluate normally, so the class is
  weakened on GitLab, not dark — say which it was.

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

**A clean board is reported clean.** Do not manufacture findings to justify the run — that is how a
grooming tool teaches people to stop running it.

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

This is the partial-read failure one rule narrower, and it hides better — the issue count is honest,
so nothing in the summary looks incomplete. A reader who is told the board is clean will not ask which
rules were awake.

**Say a check went dark only when it had something to decide.** A board where no issue carries two
labels does not need rule 4's oracle, and reporting it unevaluated there is boilerplate — which is how
a caveat stops being read by the run that needs it. The note is owed when a candidate existed and the
check could not settle it: two labels and no declared family, an unlinked path and no way to confirm
the target. No candidate, no note.

## Decision outcomes

Report the outcome by name, every run. Each command draws from its own set.

`/phil:groom-issues` (the scan) reports exactly one of:

`REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL`

and any of these **alongside** it: `REPORT-UNEVALUATED` (a rule had a candidate and no oracle) ·
`SURFACE-CANDIDATE` (a cross-issue candidate reported, not acted on) · `NOT-A-DEFECT` (something that
looks like a finding and is not) · `NO-MARKER` · `READ-ONLY`.

**A board carrying a surfaced candidate is not clean, so the terminal is `REPORT-DEFECT`.**
`SURFACE-CANDIDATE` is additive and never stands alone, and the pairing was undefined until fixture `45`
made the gap visible: a board with no body defects and four properly parented slice cards satisfies
`REPORT-CLEAN` by the letter and misreports itself. The defects that live *between* issues are defects —
the whole premise of the whole-board scan — and the summary line has always counted them beside the
per-issue findings. **`REPORT-CLEAN` is unavailable on any run that surfaced a candidate.**

Fixture `07` carries the same shape and predates the rule; it is correct under it, and was passing on
convention rather than on anything written down.

**`READ-ONLY` is now a claim about what the run did, not only about what it could do.** Before the
`gh api graphql` grant it was nearly tautological — the command held no tool capable of a write, so the
outcome restated the frontmatter. It no longer does: the grant permits a mutation document and only the
never-do list forbids one, so reporting `READ-ONLY` asserts that every forge call this run made was a
read. Keep reporting it, and mean the stronger thing.

**No new outcome was added for the parent-edge read, deliberately.** A read that succeeds produces
`SURFACE-CANDIDATE` like any other evidence, and a read that cannot be made — every GitLab board —
produces `REPORT-UNEVALUATED`, which is what that outcome is for. Minting a third would split one class
across two vocabularies and buy nothing.

`/phil:groom-fix` (the apply) reports `SCOPE-FIRST` before any write, then exactly one of:

`APPLY-MECHANICAL` · `STALE-REREAD` · `REFUSE-GENERATED`

with `LEAVE-SEMANTIC` alongside whenever a semantic defect was reported and left.

`/phil:groom-set` (the set-level loop) reports `ASK-SET-LEVEL` before any write, then exactly one of:

`APPLY-MERGE` · `APPLY-SPLIT` · `APPLY-CONSOLIDATE` · `DECLINE-NO-TRACE` · `REFUSE-UNVERIFIED` ·
`REFUSE-CONCURRENT` (members in flight at once, so consolidating them is refused on good evidence) ·
`REFUSE-RESLICE` · `REFUSE-UNGRANTED`

with `REDERIVE-BETWEEN` alongside whenever an apply invalidated a later candidate.

**`REFUSE-RESLICE`** — a split was asked for over a *feature*, which means re-slicing its roadmap and not
changing which cards exist. Name the operation asked for and the one that would be needed.

**`REFUSE-UNGRANTED`** — the resolution needs a call this command does not hold: shape (b)'s reopen, a Status
write, or a rollup read. **Hand over the exact calls and stop.** This is the milestone pattern generalised —
*propose, hand over, stop* — and it refuses to **act**, never to **report**. A run that silently does less
than it said, or that reports `APPLY-CONSOLIDATE` for a shape it could only half-complete, is the failure
this outcome exists to prevent.

**For a story consolidation the shapes are two, not three** — a reopened closed story card, or a newly
created one; there is no open-parent shape, because the story card is what is being created.

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
- Merge, split, close, group, or consolidate without an explicit answer to a question that offered the
  outcome.
- Report a **generated** projection as a body defect. Session state inside the `nwave:status` markers is
  intended; only typed scratch outside them is a finding.
- Report a card as oversized on its size, its section count, or the presence of a generated block, or propose
  splitting a **feature card or a story card** on size. The rule is demonstrability, and a size-keyed reading oscillates the board.

`/phil:groom-issues` (the scan) additionally:

- **Write anything.** No issue edits, no labels, no comments, no milestones. It holds no `Write` and no
  `Edit`, so a session that finds itself needing one of those here has misread the command.
- **Send a `mutation` document through `gh api graphql`.** This is the one prohibition here that no tool
  boundary backs. The grant exists to read a parent edge and permits a mutation as a side effect; the
  scan may issue `query` documents only. **Refuse rather than improvise** — a resolution that needs a
  forge write is `/phil:groom-set`'s, and handing it over is the whole design.
- **Use the graphql grant to work around a missing read.** It was widened for the parent edge, not into
  a general forge API. Anything else it could reach is a check nobody has reasoned about, arriving
  without a rule, an evidence tier, or a fixture.

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
- **Conclude that no feature card or story card exists without searching closed issues.** A previous split may have closed
  the original as superseded, and minting a second one buries the first.
- **Consolidate on title evidence alone.** `slice NN` in a title is a habit; it licenses a report, never an
  irreversible write. A shared milestone licenses nothing.
- **Reopen a card and leave its Status unset.** `gh issue reopen` does not restore the field, so the card sits
  OPEN in Done and no view flags it.
- **Split a feature into slice cards, or a story card on size.** Splitting an ordinary card creates cards; splitting a feature means re-slicing
  its roadmap, which is not this command's to do.
- Close on board prose alone. The claim that work landed another way is settled in the repository or
  not at all.
- Create a milestone, or treat one card's container as evidence for another's.
- Record a decline anywhere, or let a run of approvals turn the next ask into a formality.

## Acceptance

`self-test/` holds the fixtures. Run them whenever this file, its `references/`, a command loader, or
`phil:issue-board`'s body-relevant sections change.
