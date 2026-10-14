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
  guess any of it from here; read it there.
- **REQUIRED BACKGROUND: `phil:nwave-slice-status`** — how to read a feature's artifacts and derive
  a status. It owns the vocabulary, the precedence between sources, and the cases where the honest
  answer is `unknown`.

**Ask `nwave-slice-status` for every status and publish what it returns; derive none here.** Two
derivations over the same files drift apart.

**This direction is one-way.** The forge is a projection of the artifacts. Nothing read from an
issue is ever written back into `docs/feature/`.

## The mapping

| nWave artifact | Forge object |
|---|---|
| Story — several features declaring one slug | **One issue**, where any feature declares membership. The card that moves. |
| Feature — `docs/feature/<id>/` | **One issue** where it declares no story; **a row in the story's feature roster** where it does. Carries the wave either way. |
| Slice — `slices/slice-NN-*.md`, or roadmap phase `NN` | A row in the feature's generated roster. Never its own issue. |
| Step — `roadmap.json` step `NN-MM` | A row in the feature's step table, **for the current slice only**. Never its own issue. |

**The feature is the card because the feature is what somebody owns.** A slice is never assignable to
a second developer, so slice cards crowd a shared board with items only the feature's owner can pick up,
while the board fails to say what a teammate needs: which features are in flight, and who has them.

**A board may already carry slice cards from the retired mapping; consolidating them is grooming, not
this skill.** Use `phil:groom-set`, under *Consolidate a decomposed feature*; a consolidation done wrong
closes real cards.

**A slice is never its own issue under this mapping, with no exception.** Two people working one feature
at once is `phil:issue-board`'s case under *Choosing what becomes an issue*, and a repo that needs it has
left this mapping. Every rule below — no rollup, no per-slice position, no sub-issue — assumes no slice
cards exist.

**On a story card, read `references/story-cards.md` whole before writing anything to it.** It holds
the story tier's wave rule, feature order, block layout and routing. Every rule here applies to a story
card too, except where that file names a story-tier exception.

Steps and slices stay rows because a 22-phase feature would otherwise mint hundreds of issues. The step
table is scoped to the current slice because every step of every slice in one description is
unreadable too.

`roadmap.json` supplies **ids and order** — of the steps inside a slice, and of the slices themselves.
A per-step `status` field in it is a status source `nwave-slice-status` already handles; take whatever it
returns.

## The roster is generated, and it is the same instrument as the step table

Slices are not issues, so **no sub-issue relationship is created for them and no forge rollup applies.**
Both forges' parent-completion mechanisms — GitHub's `subIssuesSummary`, GitLab's
`taskCompletionStatus` — count children this mapping no longer creates. `phil:issue-board` still owns
what they measure; nothing here reads them.

**Nothing computes the roster, so this skill generates it** — delimited and timestamped, the same
instrument as the step table. Both forges are identical on the roster: no epics, no second seeding pass.

**The tier still matters elsewhere.** Scoped labels, which the wave label uses, and real dependency
links are both Premium-gated, per `phil:issue-board`.

**Write the roster as plain rows with generated glyphs, never as `- [ ] ` checkboxes**, on either forge.
Both forges count checkboxes, so the temptation is real; but a checkbox is ticked by hand while work
completes on its own, and the card then shows the checkboxes' state rather than the work's.

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
`·` is `not started` at slice level and `to do` at feature level. Both are safe only because the
vocabularies never share a table and every row prints its state word beside the glyph.

**Every value the owner can return has a glyph; a value with none fails loudly.** Degrading it to `·`
publishes unknown as not started, for a whole feature. A value added to the owner's vocabulary needs a
glyph added here. Invent no glyph for a value the owner does not define, and never omit a row to avoid
rendering its value.

**Every roster row carries a two-line description of what that slice does** — not just its name. A
reader inheriting the feature needs to know what the slice achieves without opening its brief; with
those descriptions, a reader named a card's wave and position inside thirty seconds (2026-08-14).

**Summarise what you link.** Give each linked artifact — the delta, the slice briefs, the journey — a
clause saying what it holds. Six bare URLs consume the whole thirty-second read.

### Compose the block's own sentences against the clarity standard

**Compose against `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` as you write; run no editor pass afterwards.**
`phil:eos` applies the same principles when a human invokes it, and is not a stage here: a pass over the
block is a second writer.

**The bound counts rows; only composition protects the words.** A block can satisfy every count and still
spend the thirty-second read on padding, and nothing here detects a padded row.

**Read the standard as *compose well*, never *compose short*.** Concision is one of its eleven principles;
active voice, positive form, concrete language, parallel structure and the emphatic word last are
invisible to a word count.

**Composed sentences only — never a rendered value.** In: the two-line descriptions; the summarising
clause on each linked artifact; the `Notes` sentence this skill writes itself when it records that a
hand-set state was replaced and what it said (*Publishing does not overwrite what it cannot know*); the
stage-1 sentence about what granularity will exist; the no-routing-row explanation; and the statement
that a column was left untouched.

Out: glyphs, header lines, timestamps, table scaffolding, status words returned by
`phil:nwave-slice-status`, `Notes` text that owner supplied, the verbatim-fixed `Wave note:` clause — and
**the projected `Why` / `Next` / `Stack`**. That last one is the trap: it reads like prose because it is
prose, but `phil:session-handoff` CAPTURE step 10 *hands* it here with its capture timestamp. This skill
renders it; editing it would publish words the snapshot never held, under the snapshot's timestamp
(fixture 19).

**The discriminator, for any sentence neither list names:** where this skill composes the words, the
standard applies; where it renders words another owner composed, they pass through untouched.
Apply the discriminator wherever the lists are silent; silence in a rule is a gap, not a permission.

**That boundary keeps one writer.** A standard the writer applies to its **own** sentences adds no second
author; a pass over a glyph could only be a second author, which *Project the reasoning, not just the
position* forbids.

**Apply it to text this skill composes, and flag no prose a human wrote.** Judging is taste; composing is
not.

**Set no word ceiling.** Fixtures 30 and 31 pin this section and assert none; fixture 30 supplies a brief
and no candidate text, so it tests composition rather than length.

## Wave is a label on the feature card

**Record the wave as a label** — `wave::deliver`, or `wave: deliver` where scoped labels are
unavailable — and restate it in the generated block. The routing table below is keyed on the
`wave: <name>` form, so use that form wherever the label is written or read.

**On a story card the wave label follows its own rule:** *The wave label on a story card*, in
`references/story-cards.md`.

**The wave label is single-valued and must be swapped, not added.** Remove the old wave in the same
call that adds the new one. Without scoped labels nothing enforces this, and a feature walked from
DISCUSS to DELIVER otherwise carries four wave labels while every command reports success.

Keep **blocked** off the wave label. When the blocker is another issue, use the forge's dependency
link and leave the chain line, both per `phil:issue-board`. A label carries only what no link can
express — waiting on a person, a decision, or an outside event.

**The columns stay `to do · in progress · blocked · done`; the wave is never a column** (settled
2026-08-14). A board carries non-nWave work too, and seven wave columns are noise to everyone filing it.
**The block is the only place a feature's wave appears** beyond its label.

Board columns therefore hold the **feature-level state** from `phil:nwave-slice-status`, not the wave.

**Ask `phil:nwave-slice-status` for the feature-level state, and for a story card's state with
`--story-state`; fold neither here.** It exposes the feature state under *The feature-level state, on
request*, in its `references/states.md` — `blocked` · `done` · `in progress` · `deferred` · `unknown` · `to do`, folded over **every**
slice, and `unknown` for a feature with no slices. Publish what it returns; if this skill and
`phil:nwave-slice-status` disagree, the owner wins. The six states and four columns below apply unchanged
to a story card. Wound: a fold was written here on 2026-08-14, while the owner had none, and removed the
same day.

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

**Leave the card's column untouched for those two, and say so in the block.** `Todo` for an `unknown`
feature reports work nobody has assessed as work nobody has started; for a `deferred` one, it invites
someone to pick up work its artifacts set aside. No column means *I do not know*, and inventing one is
not this skill's call.

## The order of the cards is the order of the work

`roadmap.json` fixes both orders: `phases[]` for the roster rows, `phases[].steps[]` for the step rows
inside the current slice. Publish both.

**Slice order is a table fact, not a board fact**: with no slice cards there is nothing to position,
no sub-issue list to disagree with the column, and no second seeding pass.

What remains is the order of the **feature** cards within a column, which is `phil:issue-board`'s under
*A column is a queue, so its order is a claim*, in its `references/ordering.md`.

- **On a story card, feature order follows *Card order at the story tier***, in `references/story-cards.md`.
- **Array order, not id order.** Where anything else implies a different sequence — the slice numbers, a
  dependency noted in a slice file — the array still decides.
- **Before `/nw-roadmap` there is no schedule.** Order the roster rows by slice file number ascending,
  the best available guess, and say so beside them: `Order: slice number, provisional until /nw-roadmap`.
  A provisional order that admits it gets corrected; one that does not gets worked. When the roadmap
  lands, replace that line with the array order rather than leaving both standing.
- **Where `/nw-roadmap` will never run, say that instead of promising it.** A repo that authors prose
  rather than executing DELIVER has no roadmap coming, so `provisional until /nw-roadmap` describes a
  correction that will never arrive. Write `Order: slice number — final; /nw-roadmap does not run in this
  repo`, as this plugin's own repo does.
- **A deferred slice takes a row and a `⊘` glyph, not a position.** It stays visible as deferred rather
  than absent.

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
  recorded something no artifact contains. Preserve it and note the derived state beside it; replacing
  it destroys the only record of why work stopped.
- **A human-set state that contradicts what the artifacts own is replaced — and the replacement is
  recorded.** The discriminator is the same one, read the other way: *awaiting input* adds something
  no artifact can hold, while a hand-typed `done` overwrites something they do. Publish the derived
  value, and note in `Notes` that a hand-set value was replaced and what it said. `nwave-slice-status`
  cannot see a forge/artifact disagreement, so record it here or nowhere.

## Generate into a delimited block

Publish `nwave-slice-status`'s table **with its `Notes` column intact**. Notes is where drift,
disagreeing sources, and missing artifacts are recorded, and dropping it on the way to the forge
sends the cleanest-looking version of the table to the largest audience.

**At most one feature's slices are enumerated, and — where a `roadmap.json` exists — at most one
slice's steps. Every other FEATURE is a row with a link.** That is the bound, stated as its purpose
rather than as a count, because a count does not survive the story tier and a purpose does.

**It bounds from above only.** A feature before `/nw-roadmap` publishes a roster and no step table,
and a card with no slices yet publishes neither; *exactly one* would demand tables the artifacts cannot
supply.

**"Every other feature" means features only.** Non-current *slices* stay rows in the roster with links
to their briefs.

**A card with no story declaration renders byte-identically to the feature tier before stories
existed**: one enumerated roster and, where a roadmap exists, one step table. Fixture `21` pins both
branches.

**Refusals, written as refusals because a bound stated only positively gets read as a minimum:**

- **No slice roster for any feature but the current one.** Four features of six slices would be 28 rows
  where the bound gives 10. The bound is about *what is enumerated*, not a row count: one feature's
  22-slice roster is legitimate.
- **No step table for any slice but the current one.** Unchanged from the feature tier.
- **No slices indented as sub-rows of the feature roster; put the current feature's slices in a
  second table.** An indented tree breaches the bound at scale, and at any scale puts both glyph
  vocabularies in one table — `▶ in progress` directly above `▶ current`.
- **No collapsed or `<details>`-wrapped rows.** A disclosure widget does not discharge the bound. Rows a
  reader must expand are still rows, and a forge that does not render the widget shows all of them.
- **No per-feature `Why` / `Next` / `Stack`.** A story card carries exactly one, because **a stack
  belongs to a person, not to a feature**, and the person is the same across the whole story.

Header lines precede the tables:
`Wave:`, the generation timestamp, `Work this with:` where the routing table has a row, and `Order:`.
A story block carries more, per *The story block* in `references/story-cards.md`. Below
them, when a snapshot has been projected, come the `Why` / `Next` / `Stack` sections described under
*Project the reasoning, not just the position* and laid out in `references/projection.md`.

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

**A story card's block — its feature roster, its `Story:` and `State:` lines, and what it renders when
no current feature exists — follows *The story block*, in `references/story-cards.md`.**

Replace only what is between the markers. Both forges appear to replace a description wholesale on
update, so regenerating without markers destroys any prose a human added — confirm that against
your forge before relying on it. When the markers are absent, append the block rather than rewriting
the description.

Roster order is `phases[]` array order; step order is `phases[].steps[]`. A step's `deps` may imply a
different order and does not override it.

**Only the current slice's steps appear.** Other slices link to their briefs from the roster.

## Project the reasoning, not just the position

Everything above tells a reader **where** a feature is. None of it says **why it stopped there**, and that
is the half no artifact holds — which is exactly why `/phil:handoff` records it locally. Publish it here so
a reader who is not its author can act on it.

**Whenever the block renders reasoning from `.session-handoff.md` — handed over at a capture or re-read
on a refresh — read `references/projection.md` whole before rendering it.** It holds the sections' layout, why the projection is write-only, the `⚠ stale` mark, and
whose timestamp the sections carry. Two rules apply on every refresh, whether a snapshot was handed over
or not:

- **One writer regenerates the whole block from two sources**: position from `phil:nwave-slice-status`,
  reasoning from `.session-handoff.md`. Refresh both or neither — updating one half and preserving the
  other makes a second writer in one region, and the next full regeneration drops what it wrote. Where a
  source is absent, render its section `unknown`; never omit it or keep a stale copy.
- **Absent renders as `unknown`, never as empty.** A card whose owner never ran `/phil:handoff` has no
  projection: say `Stack: unknown — no snapshot projected`. **Empty asserts there were no diversions**,
  which is a claim about the work; `unknown` is a claim about the record.

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

When editing this table, verify it against the wave declarations in `~/.claude/skills/nw-*/SKILL.md`,
never the command descriptions (verified 2026-08-12). Wound: a draft built from descriptions omitted
DEVOPS, DISCOVER and DIVERGE.

The rules:

- **The wave label is the source.** Derive the line from the label at generation time; never carry a
  routing line the label does not support.
- **No label, no line.** A card outside a wave gets no `Work this with:` line — emit nothing rather
  than guess. Most cards on a mixed board are not nWave work.
- **No row, no line — and say why.** This table covers the seven nWave waves and nothing else. A repo
  whose build path leaves those waves has no owning command here, so emit no line **and state that the
  table does not cover it**, rather than leaving a reader to wonder whether the line was omitted or
  forgotten. This plugin's own repo is the example: it runs DISCUSS, then authors prose with `plugin-dev`.
- **On a story card, routing follows *Routing a story card***, in `references/story-cards.md`: the
  source, the line's form, and which feature counts as current all change at that tier.
- **This line names; it does not launch.** It tells a reader which command owns the work. Nothing
  here runs anything.

## This is a projection, not a sync

`phil:issue-board` forbids syncing a local file and a forge board, because two authorities over one
fact drift. This skill does not create a second authority: the block is generated, never typed;
delimited, so it cannot swallow anything a human wrote; timestamped, so staleness is visible; and
never read back. The artifacts remain the only place a status is decided.

## Fill in two stages

Step rows exist only once `/nw-roadmap` writes `roadmap.json` in DELIVER; earlier waves have no step
ids, so write no step rows before then.

1. **Before DELIVER** — the feature issue, its wave label and column, and the **roster**, generated as
   soon as `slices/slice-NN-*.md` exists. Before that, say the roster is not yet known.
2. **After `/nw-roadmap`** — add the current slice's step table, and refresh it as the current slice
   changes.

A card in stage 1 **says that its step table arrives with the roadmap**. A card carrying neither a table
nor that line reads as a feature with no steps, which is the same false impression the invented rows
would have given, arrived at by omission.

**Where `/nw-roadmap` will never run, write instead that the roster is the finest granularity that will
exist**, and let it carry the two-line descriptions. Promising a table nothing will deliver misinforms
every future reader; stage 2 happens only where DELIVER runs.

A slice file marked `DEFERRED` or out of scope **takes a `⊘` row and is never pointed at as current or
next.** Honor the marker; `nwave-slice-status` treats it as overriding every other source. Omitting the
row erases a slice that existed and was set aside (fixture `08`).

## Refresh at boundaries

Slice start, slice end, wave change, roadmap resequenced. Not every step — a per-step write turns
each TDD cycle into a forge round-trip, and a missed one is invisible. Between refreshes,
`/phil:nwave-slice-status`
answers "where are we" locally and writes nothing.

Timestamp the generated block. A projection that states when it was made is honestly stale; one that
does not is indistinguishable from current.

**Nothing compares the timestamp to the artifacts**, so refreshing on boundaries is a discipline. No
hook, check or scan evaluates a block's age; `phil:groom-issues` reports a stale card as clean. Wound:
on 2026-08-14 a card five slices stale misinformed its own author for most of a day.

**Read the timestamp before trusting anything below it, and treat a block older than the last thing you
did on the feature as unread.**

---

## Self-test (regression gate)

`self-test/README.md` is the fixture register: what each fixture pins, the retired fixture 10, and how
to drive the suite. Drive it whenever this skill or its `references/`, `phil:issue-board` or `phil:nwave-slice-status`
changes, since this skill's correctness is partly theirs. Every failure mode here is silent: the wrong
answer arrives as a clean, timestamped table the whole team reads.
