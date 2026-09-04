---
name: nwave-issue-board
description: Use for any GitLab or GitHub board or tracker work in an nWave repo — one holding `.nwave/` or `docs/feature/` — including putting a feature on the tracker as a single card, generating the slice roster and current-slice step table inside it, ordering those rows to match the roadmap, recording which wave a feature is in, or deciding what a story, feature, slice, and step each become in a forge, putting a multi-feature story on the board as one card. Read this before `phil:issue-board` whenever those directories exist. Covers only the mapping; `phil:issue-board` owns the forge mechanics and `phil:nwave-slice-status` owns the status.
---

# nWave Features on a Forge Board

nWave keeps the truth on disk and renders it locally. This skill maps those artifacts onto forge
objects so other people can see them. It adds **only the mapping and the publishing discipline** —
two things it deliberately does not own:

- **REQUIRED BACKGROUND: `phil:issue-board`** — every forge mechanic. Naming the target with `-R`,
  tier gating, label swaps versus board lists, Projects v2 being a separate API, sub-issue and
  dependency-link commands, absolute URLs, two-pass seeding, reading back the end state. Do not
  guess any of it from here.
- **REQUIRED BACKGROUND: `phil:nwave-slice-status`** — how to read a feature's artifacts and derive
  a status. It owns the vocabulary, the precedence between sources, and the cases where the honest
  answer is `unknown`.

**Never derive a status here.** Ask `nwave-slice-status` and publish what it returns. Two
derivations over the same files drift apart; that drift is why this skill exists separately.

**This direction is one-way.** The forge is a projection of the artifacts. Nothing read from an
issue is ever written back into `docs/feature/`.

## The mapping

| nWave artifact | Forge object |
|---|---|
| Story — several features declaring one slug | **One issue**, where any feature declares membership. The card that moves. |
| Feature — `docs/feature/<id>/` | **One issue** where it declares no story; **a row in the story's feature roster** where it does. Carries the wave either way. |
| Slice — `slices/slice-NN-*.md`, or roadmap phase `NN` | A row in the feature's generated roster. Never its own issue. |
| Step — `roadmap.json` step `NN-MM` | A row in the feature's step table, **for the current slice only**. Never its own issue. |

**The feature is the card because the feature is what somebody owns.** A slice is never independently
assignable to a second developer, so slice cards crowd a shared board with N items nobody but the
feature's owner can pick up — while the one thing a teammate needs, *which features are in flight and
who has them*, is the thing the board does not say.

**This reverses the earlier mapping, and the reversal is a premise correction rather than a change of
taste.** Slices were the cards because *"nWave is worked one feature at a time"* — true, but that is a
property of a **developer**, not of a repo. With several developers each owning a feature, several are in
flight, and every conclusion drawn from the single-card premise has to be re-derived. The full record is
in `docs/feature/single-issue-per-feature/feature-delta.md`.

**A board may already carry slice cards, and this mapping does not itself clean them up.** Boards shaped by
the retired mapping — or by grooming advice that followed it — hold a feature's slices as separate issues, and
under the rules here those should be roster rows. That consolidation is a **grooming** operation with ranked
evidence, three target shapes and a rollup hazard: `phil:groom-set`, under *Consolidate a decomposed feature*.
Do not improvise it from this side; a consolidation done wrong closes real cards.

**A slice is never its own issue under this mapping, and there is no exception clause here.** Two people
working one feature at once is the case `phil:issue-board` covers under *Choosing what becomes an issue*,
and a repo that needs it has left this mapping rather than found a branch inside it. Do not read that rule
as licence to create slice cards while following this one: every rule below — no rollup, no per-slice
position, no sub-issue — assumes there are none, and a mixed application resurrects all of them at once.

Steps and slices both stay rows for the reason steps always did: a 22-phase feature would otherwise mint
hundreds of issues, and that size is real. **The inverted form of that argument binds too** — every step
of every slice in one description is unreadable in a different way, which is why the step table is scoped
to the current slice.

`roadmap.json` supplies **ids and order** — of the steps inside a slice, and of the slices
themselves. It is not the status source, but neither is it
forbidden as one: a project that maintains a per-step `status` field is a case
`nwave-slice-status` already handles. Take whatever it returns.

## The roster is generated, and it is the same instrument as the step table

Slices are not issues, so **no sub-issue relationship is created for them and no forge rollup applies.**
Both forges' parent-completion mechanisms — GitHub's `subIssuesSummary`, GitLab's
`taskCompletionStatus` — count children this mapping no longer creates. `phil:issue-board` still owns
what they measure; nothing here reads them.

**An earlier version of this skill forbade a hand-written roster, and that ban does not transfer.** It
was scoped to the case where the forge already computed the roster from sub-issues, making a written copy
a second tally that would disagree. Once slices stop being issues, nothing computes it — and a
**generated, delimited, timestamped** roster is the same instrument as the step table that already ships,
carrying the same guarantees.

Both forges are now identical **on the roster**, which removes the asymmetry the old design had to work
around: no epics, no second seeding pass, and no per-forge rollup divergence.

**The tier still matters elsewhere, so do not read that as "no tier question".** Scoped labels — which the
wave label uses — and real dependency links are both Premium-gated, per `phil:issue-board`. What retired is
the tier question about *hierarchy*, not the tier probe itself.

**Never write the roster as `- [ ] ` checkboxes**, on either forge. GitLab will report a completion count
from them and GitHub will count them under `trackedIssues`, so the temptation is real and the mechanism
works. **A checkbox is ticked by hand while work completes on its own**, so the two diverge the first time
anyone forgets, and what the feature then displays is the state of the checkboxes rather than the state of
the work. Plain rows with generated glyphs, always.

**Per-row status is a glyph, generated from what `phil:nwave-slice-status` returns and never typed.** That
skill owns the vocabulary and defines **seven** values; this table is a rendering of them and nothing more:

| Its status | Glyph |
|---|---|
| `done` | `✓` |
| `current` | `▶` |
| `next` | `→` |
| `not started` | `·` |
| `blocked` | `!` |
| `deferred` | `⊘` |
| `unknown` | `?` |

**The feature roster renders a DIFFERENT vocabulary, and conflating them is a defect.** Slice rows carry
the seven step statuses above; feature rows carry the **six** values `phil:nwave-slice-status` folds —
there is no `next` at feature level, and `current` is `in progress`:

| Feature state | Glyph |
|---|---|
| `done` | `✓` |
| `in progress` | `▶` |
| `to do` | `·` |
| `blocked` | `!` |
| `deferred` | `⊘` |
| `unknown` | `?` |

**Two glyphs are reused, not one.** `▶` is `current` at slice level and `in progress` at feature level;
`·` is `not started` at slice level and `to do` at feature level. **`·` is the more dangerous reuse**,
because it is the degrade target the no-glyph rule below exists to forbid. Both are safe only because
the vocabularies never share a table — which is the second ground for refusing an indented tree — and
because every row prints its state word beside the glyph. **The property to preserve is the one the slice vocabulary
already carries: every value the owner can return has a glyph.** A value with no glyph must **fail**,
never degrade to `·` — that is the unknown-published-as-not-started defect at feature scale, and it is
worse here because a feature row stands for a whole feature.

**A value added to the owner's vocabulary needs a glyph added here**, or the generator faces a status it
cannot render. Never invent a glyph for a value the owner does not define; never render a value by
omitting its row.

**Every roster row carries a two-line description of what that slice does** — not just its name. The
name is a label the owner recognises; a reader inheriting the feature needs to know what the slice
achieves without opening its brief. Measured 2026-08-14: a reader named a card's wave and current
position inside thirty seconds against a roster carrying those descriptions.

**Summarise what you link.** Where the block or the surrounding description points at artifacts — the
delta, the slice briefs, the journey — give each a clause saying what it holds. Observed in the same
read: *"I like that the artifacts are all linked **and summarized**."* Six bare URLs would have consumed
the whole thirty-second budget the projection exists to fit inside.

### Compose the block's own sentences against the clarity standard

**The standard is `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`. Name it and compose against it; do not run an
editor as a step.** `phil:eos` applies these same principles when a human invokes it, and is deliberately
**not** a stage in this skill's flow — a pass over the block is what the one-writer rule below forbids.

**The bound cannot see this.** *Generate into a delimited block* states the bound **as its purpose** —
the thirty-second read — and this skill enforces it **as a count**, rows enumerated versus rows linked.
That gap is the whole reason this section exists: a block can satisfy every count the skill can check and
still spend the entire budget the bound was written to protect, because the budget is spent on words.
**Nothing here detects a padded row.** Measured 2026-09-04: twelve board-family files named no prose
standard, while `writing.md` passed its reachability check on five other surfaces' citations.

**The standard is eleven principles of composition, and concision is one of them.** Active voice, positive form,
definite and concrete language, parallel structure for coordinate ideas, and the emphatic word last are
**invisible to a word count**. A row can improve materially with zero words removed. Read this section as
*compose well*, never as *compose short*.

**Composed sentences only — never a rendered value.** In: the two-line descriptions; the summarising
clause on each linked artifact; the `Notes` sentence this skill writes itself when it records that a
hand-set state was replaced and what it said (*Publishing does not overwrite what it cannot know*); the
stage-1 sentence about what granularity will exist; the no-routing-row explanation; and the statement
that a column was left untouched.

Out: glyphs, header lines, timestamps, table scaffolding, status words returned by
`phil:nwave-slice-status`, `Notes` text that owner supplied, the verbatim-fixed `Wave note:` clause — and
**the projected `Why` / `Next` / `Stack`**. That last one is the trap: it reads like prose because it is
prose, but `phil:session-handoff` step 9 *hands* it here with its capture timestamp. This skill renders
it. Editing it would make the block a non-deterministic function of an unchanged snapshot, published
under that snapshot's own timestamp — the projection asserting a fidelity it does not have, which
fixture 19 gate-fails.

**The discriminator, for any sentence neither list names:** where this skill composes the words, the
standard applies; where it renders words another owner composed, they pass through untouched.
Enumerations lag as the block grows; the discriminator does not. *Silence in a rule is a gap, not a
permission* — so apply the discriminator rather than reading an absent line as an exemption.

**That boundary is what makes a prose standard compatible with one writer.** The block regenerates whole
from a single writer, and a standard that writer applies to its **own** sentences adds no second author.
There is nothing to edit in a glyph, so a pass over one could only be a second author — which *Project
the reasoning, not just the position* forbids outright.

**Judging is taste; generating is not.** Nothing here licenses flagging prose a human wrote. Applying a
house standard to text this skill composes itself polices nobody. (`phil:groom-issues` refuses to rewrite
a rule that passed, under *A rule that passed is never rewritten*, and states the taste/style framing
itself under *Judging prose is taste; composing it is not*.)

**Brevity is a principle here, not a count.** No word ceiling is set, and fixtures 30 and 31 assert none
— a fixture counting words would pin one of the eleven principles of composition and license nine failures. **The cost,
stated because it is real:** those two fixtures are the only things pinning this section, so they must
test composition rather than length. Fixture 30 supplies a brief and no candidate text for exactly that
reason.

## Wave is a label on the feature card

**Record the wave as a label** — `wave::deliver`, or `wave: deliver` where scoped labels are
unavailable — and restate it in the generated block. The routing table below is keyed on the
`wave: <name>` form, so use that form wherever the label is written or read.

**On a story card the label is the CURRENT FEATURE's wave** — still exactly one, still swapped never
added. A story does not have a wave of its own; its members do, and the current one is the only member
whose wave a reader can act on.

**It is therefore NOT monotonic, and that is correct output rather than a bug.** When the current
feature finishes and the next begins, the label steps **backwards** — DELIVER to DISCUSS — because a new
feature starts at the beginning.

**Every story block carries this clause, verbatim, on its own header line — not only the blocks where a
backwards step just happened:**

```
Wave note: a story's wave is its current feature's, so it moves backwards when one feature finishes and
the next begins. That is correct.
```

**On every story block, and the alternative reading is the one that fails.** A clause emitted only at the
transition is gone by the next refresh — and the reader who "corrects" the label forwards is by
construction a *later* reader, so a transition-only clause is absent at exactly the moment it exists for.
The block is regenerated whole, so there is nowhere for such a clause to persist anyway. Fixed wording,
because the block is generated and never typed; a clause each run invents is a clause that drifts.

*Rejected: `wave: mixed`.* It names no command, so the routing line dies with it, and it hides which
member is actually moving — the one fact the label exists to carry.

*Rejected: multi-valuing the label on story cards.* It resurrects the measured four-accumulated-labels
failure and breaks the single-valued declaration `phil:groom-issues` rule 4 reads, which is normative in
every nWave repo. **If the story tier needed that declaration changed, the story tier would be wrong.**

**The wave label is single-valued and must be swapped, not added.** Where scoped labels are
unavailable, nothing enforces that, so a feature walked from DISCUSS to DELIVER accumulates four
wave labels and the record of where it stands becomes unreadable while every command reported
success. Remove the old wave in the same call that adds the new one.

Keep **blocked** off the wave label. When the blocker is another issue, use the forge's dependency
link and leave the chain line, both per `phil:issue-board`. A label carries only what no link can
express — waiting on a person, a decision, or an outside event.

**The wave is never a column. Settled 2026-08-14, and the reason is about the board's other readers.**
A board carries non-nWave work too — ordinary stories, bugs, chores — and seven wave columns are noise to
everyone filing those. They partition a board along an axis that does not apply to most of what sits on it.
So the columns stay one generic family, `to do · in progress · blocked · done`, legible to every reader,
and **the block is the only place a feature's wave appears** beyond its label.

**This upholds the 2026-08-10 decision after that decision's stated reason had been refuted, and the
sequence is the lesson.** Wave columns were originally rejected because *"nWave is worked one feature at a
time, so those columns hold a single card between them."* That reason is wrong — it describes a developer,
not a repo — and correcting it looked like grounds to reverse the decision. It was not. The decision was
right for a reason its record never captured, and refuting a recorded rationale does not refute the ruling
it was offered for. **Before reversing a decision, ask what else could have justified it.**

Board columns therefore hold the **feature-level state** from `phil:nwave-slice-status`, not the wave.

**A story card's column comes from `--story-state`, asked for exactly as the feature state is.** Same
rule, same reason, one level up: the fold across features is a derivation, it lands with
`phil:nwave-slice-status`, and a fold written here would be this skill's recurring defect committed a
second time in the same file that documents it. Nothing in this skill computes a state — feature or
story. The six states and the four columns below apply unchanged to a story card, `deferred` and
`unknown` included.

**Do not fold a feature-level state here. Ask for one.** `phil:nwave-slice-status` owns every derivation
over these files and, as of 2026-08-14, exposes a feature-level state on request under *The feature-level
state, on request* — `blocked` · `done` · `in progress` · `deferred` · `unknown` · `to do`, folded over
**every** slice. Publish what it returns.

A fold written here instead would be this skill's recurring defect in its exact historical form: a
derivation invented by the skill that had just delegated derivation away. It was written here, once, on
2026-08-14, and removed the same day — while the owner had no such fold at all, so the delegation pointed
at nothing and the local copy was the only description available. Both halves are fixed; the shape is worth
remembering, because a delegation to a capability that does not exist reads exactly like a delegation that
works.

**Or over none.** A feature never decomposed has an empty roster, and the owner's fold returns `unknown` for
it — a guard added 2026-08-31. Nothing changed here: the mapping below already refuses a column for
`unknown`, and fixture `18` takes the state as its *input*, so it holds whatever produced it. Checked, not
assumed. The fold's owner is `phil:nwave-slice-status`; if the two disagree, it wins.

**Six states, four columns — and two of them must never be coerced.** The fold returns `blocked`, `done`,
`in progress`, `deferred`, `unknown` and `to do`; a board carries four:

| State | Column |
|---|---|
| `blocked` | Blocked |
| `done` | Done |
| `in progress` | In Progress |
| `to do` | Todo |
| `deferred` | **no column — do not write one** |
| `unknown` | **no column — do not write one** |

**Leave the card's column untouched for those two and say so in the block.** Writing `Todo` for an
`unknown` feature is the cardinal lie of the sibling skill committed at feature scale: it reports work
nobody has assessed as work nobody has started, in the one place the whole team reads. `deferred` fails the
same way more quietly — `Todo` invites someone to pick up a feature its own artifacts set aside.

A mapping from more states to fewer columns is exactly where a coercion looks like tidiness. There is no
column that means *I do not know*, and inventing one is not this skill's call; the honest move is to write
nothing and let the timestamped block carry what is true.

## The order of the cards is the order of the work

`roadmap.json` fixes both orders: `phases[]` for the roster rows, `phases[].steps[]` for the step rows
inside the current slice. Publish both.

**Slice order is now a table fact, not a board fact**, and that retires a whole class of work the old
mapping needed. There is no per-slice card to position, so **the two-orders problem is gone**: GitHub's
board column and sub-issue list no longer disagree, because there is no sub-issue list, and GitLab needs
no second seeding pass, because there are no slice numbers to wait for. Both ordering mutations the old
design depended on — `reprioritizeSubIssue` and its GitLab counterpart — **were never exercised against a
real board**, and nothing here needs them now.

What remains is the order of the **feature** cards within a column, which is `phil:issue-board`'s under
*A column is a queue, so its order is a claim*.

- **At the story tier the order is the declared `position`, and the line says so:**
  `Order: feature position as declared · slice order <as below>`. Where a member declares no position it
  **sorts last and the line says that too** — `phil:nwave-slice-status` returns it that way and never
  invents one. Where two members claim one position the owner returns `contested`; see below.
- **Array order, not id order.** Where anything else implies a different sequence — the slice numbers, a
  dependency noted in a slice file — the array still decides.
- **Before `/nw-roadmap` there is no schedule.** Order the roster rows by slice file number ascending,
  the best available guess, and say so beside them: `Order: slice number, provisional until /nw-roadmap`.
  A provisional order that admits it gets corrected; one that does not gets worked. When the roadmap
  lands, replace that line with the array order rather than leaving both standing.
- **Where `/nw-roadmap` will never run, say that instead of promising it.** A repo that authors prose
  rather than executing DELIVER has no roadmap coming, so `provisional until /nw-roadmap` describes a
  correction that will never arrive. Write `Order: slice number — final; /nw-roadmap does not run in this
  repo`. Observed in this plugin's own repo, where the build path is authoring with `plugin-dev`.
- **A deferred slice takes a row and a `⊘` glyph, not a position.** It is visible as deferred rather than
  absent — an improvement on the old mapping, where a deferred slice took no card and so left no trace
  at all.

Reposition on the boundaries in *Refresh at boundaries* below — including a roadmap that was
resequenced, which is a boundary precisely because nothing else about the feature moved. Order and
status go stale together, and a card whose column changed but whose roster did not is the half-updated
case.

## Publishing does not overwrite what it cannot know

The vocabulary is `nwave-slice-status`'s. Two of its cases matter especially when writing to a
forge, because the forge copy has the widest audience:

- **`unknown` is not `not started`.** Publish it as `unknown`. Reporting work you cannot assess as
  untouched is a claim someone will act on.
- **A human-set state outranks a regenerated one.** Someone marking an issue *awaiting input* has
  recorded something no artifact contains. A refresh that replaces it with a derived value reports
  success while destroying the only record of why work stopped. Preserve it and note the derived
  state beside it.
- **A human-set state that contradicts what the artifacts own is replaced — and the replacement is
  recorded.** The discriminator is the same one, read the other way: *awaiting input* adds something
  no artifact can hold, while a hand-typed `done` overwrites something they do. Publish the derived
  value, and note in `Notes` that a hand-set value was replaced and what it said. This disagreement
  is between the forge and the artifacts, so `nwave-slice-status` cannot see it and will not record
  it — written here or written nowhere.

## Generate into a delimited block

Publish `nwave-slice-status`'s table **with its `Notes` column intact**. Notes is where drift,
disagreeing sources, and missing artifacts are recorded, and dropping it on the way to the forge
sends the cleanest-looking version of the table to the largest audience.

**At most one feature's slices are enumerated, and — where a `roadmap.json` exists — at most one
slice's steps. Every other FEATURE is a row with a link.** That is the bound, stated as its purpose
rather than as a count, because a count does not survive the story tier and a purpose does.

**It bounds from above only.** *At most* is deliberate and load-bearing: a feature before `/nw-roadmap`
publishes a roster and **no step table at all**, and a card with no slices yet publishes neither. Written
as *exactly one*, this sentence would make those cards non-compliant — it would convert a ceiling into a
floor and demand tables the artifacts cannot supply. Two shipped fixtures occupy that branch.

**"Every other feature" means features, and only features.** The bound is scoped at the feature tier
because that is the only tier a story adds. Non-current *slices* are governed where they always were —
they are rows in the roster with links to their briefs, unchanged. Naming the tier matters: read as
ranging over slices, this sentence would put links in a feature-tier roster that has never carried them
and would break the identity claim below.

**At the feature tier this produces exactly what it always did**, unchanged: one feature, so its slices
are the one enumerated roster, and its current slice — *if a roadmap exists* — the one enumerated step
table. A card carrying no story declaration renders byte-identically to what shipped before the story
tier existed. That identity is the test of a faithful restatement, not a happy accident, and a fixture
pins it on **both** branches, with and without a roadmap.

At the story tier the same sentence yields the feature roster, the current feature's slice roster, and —
where a `roadmap.json` exists — the current slice's steps.

**Refusals, written as refusals because a bound stated only positively gets read as a minimum:**

- **No slice roster for any feature but the current one.** Four features of six slices is 24 slice rows
  on top of the 4 feature rows — 28 — where the bound gives 10. The budget is the **thirty-second read**
  measured on the predecessor, not a row count: `phil:nwave-slice-status` fixture 17 publishes 26 rows
  legitimately, because 22 of them are one feature's roster and the bound is about *what is enumerated*,
  not about how many rows result.
- **No step table for any slice but the current one.** Unchanged from the feature tier.
- **No slices indented as sub-rows of the feature roster.** This is the wrong reading of "demoted a
  level" and it looks like the right one: an indented tree in one table renders the same N×M, flat, with
  better typography. The correct answer and the failure are one word apart. **Two independent grounds
  refuse it, and the second survives where the first does not:** it breaches the bound at scale, *and* it
  puts both glyph vocabularies in one table — `▶ in progress` on a feature row directly above `▶ current`
  on a slice sub-row — which is exactly the collision the vocabularies are only safe without. The second
  ground holds even at two features of one slice, where the scale argument evaporates.
  **The remedy: slices move to a second table scoped to the current feature.** A refusal that does not
  say what to do instead gets worked around.
- **No collapsed or `<details>`-wrapped rows.** A disclosure widget does not discharge the bound. Rows a
  reader must expand are still rows, and a forge that does not render the widget shows all of them.
- **No per-feature `Why` / `Next` / `Stack`.** A story card carries exactly one, because **a stack
  belongs to a person, not to a feature**, and the person is the same across the whole story.

**The current feature is bolded *and* linked, exactly like a sibling.** Only its slices are
enumerated; that is what "current" buys, and it is no reason to withhold its delta from a reader who
wants the detail behind the roster. Found by regenerating a real card from this rule on 2026-09-04 and
diffing it against the hand-build: the rule said *every sibling* gets a link and was silent on the
current row, so the two renderings disagreed. Silence in a rule is a gap, not a permission.

**Every sibling link is summarised, not bare** — one clause saying what it holds. Promoted to a rule
from the predecessor's slice 01, where a reader volunteered *"I like that the artifacts are all linked
**and summarized**"* and nothing required it. Six bare URLs consume the whole read budget.

Header lines precede the tables:
`Wave:`, the generation timestamp, `Work this with:` where the routing table has a row, and `Order:`.
**A story block additionally carries `Story:` and `State:` above them and the `Wave note:` clause below
`Wave:`** — five header lines rather than three, and all five are mandatory there. Below
them, when a snapshot has been projected, come the `Why` / `Next` / `Stack` sections described under
*Project the reasoning, not just the position*.

```
<!-- nwave:status:begin -->
Wave: DELIVER · generated 2026-08-10T21:04Z
Work this with: /nw-execute

| Slice | What it does | Status | Notes |
|---|---|---|---|
| 01 | Captures a masked url_shape and derives a page ref from it.<br>Disproves the masking approach if the ref cannot be rebuilt. | ✓ done | |
| 02 | Maps a captured payload onto its projection.<br>The first slice to cross a context boundary. | ▶ current | |
| 03 | Backfills historical captures.<br>Deferred until the projection settles. | ⊘ deferred | out of scope, per its brief |

Current slice 02 — steps:

| Step | What it does | Status | Notes |
|---|---|---|---|
| 02-01 | Maps a captured payload to its projection | ✓ done | |
| 02-02 | Rejects a payload whose shape has drifted | ▶ current | ⚠ no commit found |
<!-- nwave:status:end -->
```

**A story card carries one more table and one more header line.** Same markers, same generation
discipline, same refusals:

```
<!-- nwave:status:begin -->
Story: chat-everywhere · 4 features · generated 2026-09-04T17:30Z
State: in progress — from `phil:nwave-slice-status --story-state chat-everywhere`
Wave: DESIGN · current feature chat-in-web-ui
Wave note: a story's wave is its current feature's, so it moves backwards when one feature finishes and
the next begins. That is correct.
Work this with: /nw-design · feature chat-in-web-ui
Order: feature position as declared · slice order by slice number — provisional until /nw-roadmap

| # | Feature | What it does | State | Notes |
|---|---|---|---|---|
| 01 | [aws-bedrock-setup](…) | Stands up the model endpoint the other three call.<br>Nothing else can be demoed until this answers. | ✓ done | |
| 02 | **chat-in-web-ui** — [delta](…) | Puts a chat surface in the web client.<br>The first feature a user can see. | ▶ in progress | |
| 03 | [saved-sessions](…) | Persists a conversation across reloads.<br>Depends on 02's transcript shape. | · to do | |
| 04 | [chat-ui-in-extension](…) | Ports the web surface into the extension.<br>Last, because it consumes 02's settled shape. | · to do | no wave declared yet |

Current feature 02 chat-in-web-ui — slices:

| Slice | What it does | Status | Notes |
|---|---|---|---|
| 01 | Renders a transcript from a canned response.<br>Disproves the streaming assumption if it fails. | ✓ done | |
| 02 | Streams a live response into the transcript. | ▶ current | |
| 03 | Handles a mid-stream disconnect.<br>The first error path a user can hit. | · not started | |
| 04 | Persists the transcript for the session's life. | · not started | |
| 05 | Renders markdown in a streamed response. | · not started | |
| 06 | Adds the stop-generating control. | · not started | |
<!-- nwave:status:end -->
```

**Ten rows for a four-feature story** — four features plus the current feature's six slices, and no
third table because this feature has no `roadmap.json`. The unbounded rendering is 4 + 24 = **28**. The
other three features contribute one row and one summarised link each, which is the bound doing its work:
enumerating their slices too would cost eighteen more rows and buy nothing a reader asked for. This is
the scenario fixture `20` pins, and the two must agree.

**`State:` carries what `--story-state` returned, verbatim.** It is a header line rather than a column
because it describes the card, not a row. Two of the six states — `deferred` and `unknown` — write **no
column**, and the block is where that gets said, exactly as at feature tier.

**Where the owner returns a contested or absent current feature, render that and enumerate nothing.**
`phil:nwave-slice-status` refuses to resolve a position collision, and where every member is `done` it
omits the current feature entirely. Both cases reach here, and in both the heading becomes a statement
instead of a subject:

```
Current feature: contested — position 02 claimed by chat-in-web-ui and saved-sessions. No slice roster.
Current feature: none — every member is done.
```

**The header lines follow the same rule: no current feature, no wave label and no routing line.** Both
derive from the current feature and nothing else, so where the owner withholds it the card writes
neither, and the block says which case it is. Writing a wave taken from a contender is the same
invention as expanding that contender's slices, one line higher up and easier to miss.

**Picking one of the contenders so a slice roster can be rendered is this skill's recurring defect in
its newest costume** — the renderer inventing the exact fact the deriver deliberately withheld. An
absent slice roster is the honest rendering of an unresolved order.

Replace only what is between the markers. Both forges appear to replace a description wholesale on
update, so regenerating without markers destroys any prose a human added — confirm that against
your forge before relying on it. When the markers are absent, append the block rather than rewriting
the description.

Roster order is `phases[]` array order; step order is `phases[].steps[]`. A step's `deps` may imply a
different order and does not override it.

**Only the current slice's steps appear.** Every step of every slice in one description is the
hundreds-of-issues problem inverted — one page nobody can read instead of one hundred cards nobody can
scan. Other slices link to their briefs from the roster.

## Project the reasoning, not just the position

Everything above tells a reader **where** a feature is. None of it says **why it stopped there**, and that
is the half no artifact holds — which is exactly why `/phil:handoff` records it locally. Publish it here so
a reader who is not its author can act on it.

`phil:session-handoff` hands over three things from `.session-handoff.md`, each with the snapshot's capture
timestamp: the **why** (decisions reached, approaches ruled out), the **next action**, and the **work
stack** — the diversion chain, innermost last. Render them below the tables:

```
Why (captured 2026-08-14T02:07Z)
- Ruled out re-running JTBD for the slice: a second job statement over a validated job is the
  duplicate-authority defect this feature exists to detect.
- Work stopped mid-dogfood, deliberately, not because it failed.

Next — finish the dogfood on #2, asking only the missing done-condition.

Stack
1. Slice 04 elicitation · the task in hand · open since 2026-08-13T21:10Z · crossed 2   ⚠ stale
2. └ The observed population · it was partial, so the rule needed changing first · open since 2026-08-14T02:02Z · crossed 0
```

**One writer owns the whole block, and it regenerates it entire from two sources.** Position comes from
`phil:nwave-slice-status`; the reasoning comes from `.session-handoff.md`. **A partial refresh is
forbidden** — a writer that updates the position and leaves the reasoning alone, or the reverse, is a second
writer in one delimited region, and the next full regeneration silently drops whatever the other one put
there. Where a source is absent, render its section `unknown` rather than omitting it or preserving a stale
copy: that is what keeps *whole-block regeneration* from destroying anything.

Found by the first live run, 2026-08-14: a handoff refreshed the reasoning by **appending inside the
markers** and preserving the position content by hand. It worked, and it worked for the wrong reason — the
region had two writers and only care kept them from colliding.

Five rules, and the first is the one that makes this legal:

- **Write-only, like everything else in the block.** `/phil:resume` reads the local snapshot; nothing reads
  this. The local file stays the single authority, so no second authority exists to drift — which is the
  whole reason the reasoning can live on a board at all.
- **Absent renders as `unknown`, never as empty.** A card whose owner never ran `/phil:handoff` has no
  projection: say `Stack: unknown — no snapshot projected`. **Empty asserts there were no diversions**,
  which is a claim about the work; `unknown` is a claim about the record.
- **A frame whose `crossed` is 2 or more is marked `⚠ stale`.** A push that survived two wind-downs is
  stale, and a stale stack is worse than none for the same reason a stale snapshot is: the next reader
  trusts it.

  **The rule's source is `skills/session-handoff/SKILL.md` § The snapshot**, which owns the stack and the
  counter. Stated again here because the projection must be able to explain its own markings; if the two
  disagree, the recorder wins.

  **The threshold is two, not one, and that is the whole rule.** Every frame carried across a wind-down
  has survived one, so marking at one marks the normal case. `crossed` is stored per frame — written `0`
  by `push`, incremented by `CAPTURE` — because no comparison against the header can recover the count.
  **Render `crossed` verbatim; never compute it here.** The block is a projection.
- **The capture timestamp is the snapshot's, not the block's.** They differ whenever a refresh happens
  without a capture, and a reader deciding whether to trust the reasoning needs the age of the reasoning.

**The accepted cost:** a teammate sees only what the last capture projected. That is the price of one
authority, it is smaller than it looks — a projection can only lag if work continued after the handoff —
and it is stated rather than discovered.

## A card that does not say how to work it gets worked the wrong way

A card describes work. An agent handed a work description does the work — inline, in the session,
skipping the wave command that owns it. That skips the TDD cycle `/nw-execute` dispatches and the
artifact writes that make the work resumable, so the *next* session's reconstruction finds artifacts
that were never written. The failure is silent: inline work looks productive and produces plausible
output.

The wave label already on the feature issue determines the owning command, so **emit a
`Work this with:` line into the generated block**, directly under the `Wave:` line. It inherits the
block's properties — generated, never typed; delimited; timestamped — so it cannot drift from the
wave it was derived from.

| Wave label | Work this with |
|---|---|
| `wave: discover` | `/nw-discover` |
| `wave: diverge` | `/nw-diverge` — optional wave, between DISCOVER and DISCUSS |
| `wave: discuss` | `/nw-discuss` |
| `wave: design` | `/nw-design` |
| `wave: devops` | `/nw-devops` |
| `wave: distill` | `/nw-distill` |
| `wave: deliver` | `/nw-deliver` for the wave; `/nw-execute` for a single step |

Verified 2026-08-12 against the wave declarations in `~/.claude/skills/nw-*/SKILL.md`, not against
the command descriptions — which is the correction that matters. A first draft assembled from
descriptions **omitted DEVOPS entirely** (it is wave 4 of 6) along with DISCOVER and DIVERGE, and
would have cited `nw-design`'s declared `**Command**: *design-architecture` as the user entry point,
when that is the internal agent dispatch and `/nw-design` is what a person runs.

Three rules:

- **The wave label is the source.** Derive the line from the label at generation time; never carry a
  routing line the label does not support.
- **On a story card there is no member label to read, so the source is the member's own artifact.** A
  story member has no card — it is a roster row — so it carries no label and the roster has no wave
  column. Take the wave from the current feature's `docs/feature/<id>/feature-delta.md` header, which is
  where an nWave feature records it. **`phil:nwave-slice-status` does not return a wave**; asking it for
  one gets a state. And never derive the routing line from the *story card's own* label, which is this
  rule's output.
- **No label, no line.** A card outside a wave gets no `Work this with:` line — emit nothing rather
  than guess. Most cards on a mixed board are not nWave work.
  **This is the one rule that does NOT transfer unchanged to the story tier.** Its licence for silence is
  that the card may not be nWave work at all — and a story card is nWave work by definition, so that
  explanation can never apply there. **A story card with no wave says why it has none**, exactly as the
  no-row branch does.
- **No row, no line — and say why.** This table covers the seven nWave waves and nothing else. A repo
  whose build path leaves those waves has no owning command here, so emit no line **and state that the
  table does not cover it**, rather than leaving a reader to wonder whether the line was omitted or
  forgotten. Observed in this plugin's own repo 2026-08-14: it runs DISCUSS and then authors prose with
  `plugin-dev`, so a post-DISCUSS feature has no row, and the card says so in as many words. **The
  routing table does not cover the build path of the repo that owns it.**
- **On a story card the line names the command AND the feature it applies to** —
  `Work this with: /nw-design · feature chat-in-web-ui`. A bare command on a multi-feature card asserts
  the command owns the *story*, and none of them does.
- **No line ever names a command for the story.** There is no story-scoped wave command, and inventing
  one — or letting a bare command imply it — sends a reader to run something over a scope it was never
  written for. The three rules above apply unchanged at this tier: the label is still the source, no
  label still means no line, and no row still means no line **with the reason stated**. This repo is
  its own example at the story tier too: both members of its one real story are past DISCUSS on a build
  path the table has no row for, so its card carries no routing line and says why.
- **Where two members are `in progress` at once, the label is still the current feature's wave — and
  this skill does not decide which that is.** `phil:nwave-slice-status` § *The story-level state* already
  defines it: **the first member, in `position` order, whose state is not `done`** — which is not
  necessarily the first member that is `in progress`. **Every other in-flight member's Notes cell carries
  `⚠ also in flight`.**

  **Do not write "the first in-flight member" here.** That is a second definition of `current feature`,
  and it disagrees with the owner's on a roster like `01 to do · 02 in progress · 03 in progress`, where
  the owner answers **01** and a first-in-flight rule answers **02**. The block would then name one
  feature in its header, expand another's slices, and route to a third state of affairs entirely. **A
  fixture whose roster makes both rules agree pins neither**, which is why the disagreeing roster has a
  fixture of its own.

  The block neither hides the ambiguity nor resolves it. Two features genuinely in flight is a defect in
  the card, which `phil:groom-issues` **will** report — that check lands in this feature's slice 05, and
  **until then the block is the only place the state is visible at all**, which is a stronger reason to
  render it faithfully, not a weaker one.
- **This line names; it does not launch.** It tells a reader which command owns the work. Nothing
  here runs anything.

## This is a projection, not a sync

`phil:issue-board` forbids syncing a local file and a forge board, because two authorities over one
fact drift. This skill does not create a second authority: the block is generated, never typed;
delimited, so it cannot swallow anything a human wrote; timestamped, so staleness is visible; and
never read back. The artifacts remain the only place a status is decided.

## Fill in two stages

Step rows cannot exist before `/nw-roadmap` writes `roadmap.json` in DELIVER — earlier waves have no
step ids at all. Do not invent them.

1. **Before DELIVER** — the feature issue, its wave label and column, and the **roster**, generated as
   soon as `slices/slice-NN-*.md` exists. Before that, say the roster is not yet known.
2. **After `/nw-roadmap`** — add the current slice's step table, and refresh it as the current slice
   changes.

A card in stage 1 **says that its step table arrives with the roadmap**. A card carrying neither a table
nor that line reads as a feature with no steps, which is the same false impression the invented rows
would have given, arrived at by omission.

**Where `/nw-roadmap` will never run, that sentence becomes a promise nothing will keep — so do not write
it.** A repo that authors prose rather than executing DELIVER gets no `roadmap.json` ever, and a card
saying the table is coming misinforms every future reader. Write instead that the roster is the finest
granularity that will exist, and let it carry the two-line descriptions the step table would have carried.
Observed in this plugin's own repo 2026-08-14. **Stage 2 is conditional on DELIVER running, and the
two-stage rule was written assuming it always would.**

A slice file marked `DEFERRED` or out of scope **takes a `⊘` row and is never pointed at as current or
next.** Honor the marker; `nwave-slice-status` treats it as overriding every other source.

*(This sentence read "is not a card" until 2026-08-14. There are no slice cards to withhold, and withholding
the **row** instead erases a slice that existed, was considered, and was set aside — see fixture 08.)*

## Refresh at boundaries

Slice start, slice end, wave change, roadmap resequenced. Not every step — a per-step write turns
each TDD cycle into a forge round-trip, and a missed one is invisible. Between refreshes,
`/phil:nwave-slice-status`
answers "where are we" locally and writes nothing.

Timestamp the generated block. A projection that states when it was made is honestly stale; one that
does not is indistinguishable from current.

---

## Self-test (regression gate)

`skills/nwave-issue-board/self-test/` holds golden fixtures that pin these behaviors. **Ten were added
2026-09-04 with the story tier**: the bound holding at four features — 10 rows where the product would
give 24 (20); a single-feature card rendering **byte-unchanged** against the restated bound, which is the
test that a restatement restated rather than replaced (21); an **indented** feature/slice tree refused,
which the bound's old count-form would have passed because it is one table (22); a feature state with
no glyph **failing** rather than degrading to `·` (23); and a **contested** current feature enumerating
nothing rather than picking a contender, which is the renderer inventing what the deriver withheld (24);
one wave label across three waves (25); the label stepping **backwards** as correct output, with the
explanation without which someone repairs it (26); this repo's own no-routing-row case at the story tier
(27); and two members in flight rendered rather than hidden or refused, because grooming's finding is
made from that evidence (28); and the roster where the owner's current feature is **not** the first
member in flight, which is the case fixture 28 cannot separate (29). The rest pin: the
end-to-end publish (01, walking skeleton), the `Notes` column surviving the trip to the forge (02),
`unknown` published as `unknown` rather than `not started` (03), a human-set state outranking a
regenerated one (04), hand-written prose surviving a refresh that must replace the whole description
(05), a wave label swapped rather than accumulated (06), no step rows invented before `/nw-roadmap`
**and no promise of a table where DELIVER will never run** (07), a deferred slice given a `⊘` row
rather than omitted (08), a generated roster with no sub-issue created even where native hierarchy is
available (09), the forge never writing back to the artifacts (11), status decided by
`nwave-slice-status` rather than folded here (12), roster rows ordered by `phases[]` rather than by the
slice numbers that agree with each other (13), an order guessed before `/nw-roadmap` published as a
guess — **or as final where no roadmap is coming** (14), a roster kept as generated glyphs rather than
converted to checkboxes to manufacture a progress bar (15), the `Work this with:` routing line derived
from the wave label — emitted for a labelled card, withheld for one with no label, and **withheld with
an explanation for a wave the table does not cover** (16), and the projection bounded to the roster plus
the current slice's steps on a 22-phase feature (17), an `unknown` feature state leaving the card's column
untouched rather than coerced into one the board happens to offer (18), and the block regenerated entire
from both its sources rather than one region edited in place (19).

**Two were added 2026-09-04 with the prose standard**: a composed roster description held to
`rules/writing.md` while a padded variant carrying the same facts **gate-fails** (30), and the standard
refused entry to the derived cells only one writer may render (31). They are adjacent on purpose and
resolve opposite ways — 30 fails a block whose sentences went unedited, 31 fails one whose glyphs did
not. A rule that gets one right by a mechanism that gets the other wrong is a gate failure.

**Numbering has a gap at 10, and it is deliberate.** `10-gitlab-roster-second-pass` was retired on
2026-08-14: it pinned a roster written in a second pass as bare `#N` references, because slice numbers
existed only after the issues were created. No slice issues are created now, so there is nothing to wait
for and no second pass to get wrong. Retired rather than renumbered, so the gap is a question a reader can
answer from `self-test/README.md` instead of a silent renumbering that makes every prior reference wrong.

Fixtures 04 and 11 are deliberately adjacent and resolve opposite ways: a person recording something
no artifact can hold is preserved; a person overwriting something the artifacts own is not. Getting
one of them right by a rule that gets the other wrong is a gate failure.

**Fixture 08 inverted on 2026-08-14 and is the clearest example of what a paradigm change does to a
suite.** It used to assert that a deferred slice gets *no card*, because a card on a board does not
misinform someone — it assigns them. With no slice cards the danger is gone and the opposite defect
appears: omitting the row erases a slice that existed, was considered, and was set aside. **The rule
reversed because its mechanism did, and its old reasoning was never wrong.** Fixtures 13 and 14 are the
same mechanism weaker: an order is an instruction whether or not anyone chose it. Fixture 15 is that
mechanism in the reporting register — a hand-ticked checkbox is correct on the day it is written and
authoritative long after. Fixture 17 is the size case: a bound is what keeps the read achievable at 94
steps.

Fixtures 02 and 12 pin the two faults this skill actually shipped in its first draft: a three-column
block that dropped the drift warning, and a locally invented rule forbidding a status source its
owner permits.

Whenever this skill changes — or `phil:issue-board` or `phil:nwave-slice-status` changes, since this
skill's correctness is partly theirs — drive the fixtures per `self-test/README.md`. Every failure
mode here is silent: the wrong answer arrives as a clean, timestamped table that the whole team
reads.
