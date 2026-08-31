---
name: nwave-issue-board
description: Use for any GitLab or GitHub board or tracker work in an nWave repo — one holding `.nwave/` or `docs/feature/` — including putting a feature on the tracker as a single card, generating the slice roster and current-slice step table inside it, ordering those rows to match the roadmap, recording which wave a feature is in, or deciding what a feature, slice, and step each become in a forge. Read this before `phil:issue-board` whenever those directories exist. Covers only the mapping; `phil:issue-board` owns the forge mechanics and `phil:nwave-slice-status` owns the status.
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
| Feature — `docs/feature/<id>/` | **One issue. This is the card that moves.** Carries the wave. |
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

**Every value it can return has a glyph, and that is the property to preserve.** A value added there needs
one added here, or the generator faces a status it cannot render and will downgrade it — and downgrading
`blocked` or `unknown` to `·` is the *unknown-published-as-not-started* defect wearing a new costume. Never
invent a glyph for a value the owner does not define; never render a value by omitting its row.

**Every roster row carries a two-line description of what that slice does** — not just its name. The
name is a label the owner recognises; a reader inheriting the feature needs to know what the slice
achieves without opening its brief. Measured 2026-08-14: a reader named a card's wave and current
position inside thirty seconds against a roster carrying those descriptions.

**Summarise what you link.** Where the block or the surrounding description points at artifacts — the
delta, the slice briefs, the journey — give each a clause saying what it holds. Observed in the same
read: *"I like that the artifacts are all linked **and summarized**."* Six bare URLs would have consumed
the whole thirty-second budget the projection exists to fit inside.

## Wave is a label on the feature card

**Record the wave as a label** — `wave::deliver`, or `wave: deliver` where scoped labels are
unavailable — and restate it in the generated block. The routing table below is keyed on the
`wave: <name>` form, so use that form wherever the label is written or read.

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

**The roster and the current slice's steps are the only tables in the block.** Header lines precede them:
`Wave:`, the generation timestamp, `Work this with:` where the routing table has a row, and `Order:`. Below
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
- **No label, no line.** A card outside a wave gets no `Work this with:` line — emit nothing rather
  than guess. Most cards on a mixed board are not nWave work.
- **No row, no line — and say why.** This table covers the seven nWave waves and nothing else. A repo
  whose build path leaves those waves has no owning command here, so emit no line **and state that the
  table does not cover it**, rather than leaving a reader to wonder whether the line was omitted or
  forgotten. Observed in this plugin's own repo 2026-08-14: it runs DISCUSS and then authors prose with
  `plugin-dev`, so a post-DISCUSS feature has no row, and the card says so in as many words. **The
  routing table does not cover the build path of the repo that owns it.**
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

`skills/nwave-issue-board/self-test/` holds golden fixtures that pin these behaviors: the
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
