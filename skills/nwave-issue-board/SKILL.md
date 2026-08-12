---
name: nwave-issue-board
description: Use for any GitLab or GitHub board or tracker work in an nWave repo — one holding `.nwave/` or `docs/feature/` — including putting a feature and its slices on the tracker, opening an issue per slice, ordering the slice cards so the board matches the roadmap, recording which wave a feature is in, refreshing the step table inside a slice's issue, or deciding what a feature, slice, and step each become in a forge. Read this before `phil:issue-board` whenever those directories exist. Covers only the mapping; `phil:issue-board` owns the forge mechanics and `phil:nwave-slice-status` owns the status.
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
| Feature — `docs/feature/<id>/` | Parent issue. Carries the wave. |
| Slice — `slices/slice-NN-*.md`, or roadmap phase `NN` | One issue each, child of the feature. **These are the cards that move.** |
| Step — `roadmap.json` step `NN-MM` | A row in that slice's issue. Never its own issue. |

Slices are the cards because a slice crosses columns in a day while a feature would sit still for
weeks. Steps stay rows because a 22-phase feature would otherwise mint hundreds of issues — that
size is real, not hypothetical.

`roadmap.json` supplies **ids and order** — of the steps inside a slice, and of the slices
themselves. It is not the status source, but neither is it
forbidden as one: a project that maintains a per-step `status` field is a case
`nwave-slice-status` already handles. Take whatever it returns.

## Attach slices to the feature natively

GitHub carries the feature→slice edge as a real sub-issue relationship; the commands and the `gh`
version they were verified against are in `phil:issue-board` under *Dependencies depend on the
tier*. Use them rather than describing the hierarchy in prose.

Where the forge maintains the parent's rollup, **do not also hand-write a slice roster table into
the feature description** — that is a second copy of something the forge already keeps, and the
hand-written copy is the one that goes stale.

On GitHub that rollup is free and exact: because slices are sub-issues, the feature issue reports
`N of M` and draws a bar without anything being published to it — the mechanism, and the count
observed from a three-slice parent, are in `phil:issue-board` under *A parent's "N of M done" counts
different things on each forge*. **Slices done over slices total is therefore already on the board,
and the generated block must not restate it** — a hand-written count is a second tally of a number
the forge computes, and it is the one that will disagree.

`glab issue update` exposes no parent or child flag, and GitLab hierarchy means epics, which are
Premium and group-scoped. So on GitLab the feature description carries a roster table of bare `#N`
references, and that is the only *project-scoped* rollup available. Two things govern it:

- Keep the references **bare**. `#N` renders live state; a markdown link freezes it. The reasoning
  is in `phil:issue-board` under *Link what the forge cannot resolve*.
- Slice numbers exist only after the issues are created, so the roster is a **second pass** — see
  *Bulk seeding needs two passes* in `phil:issue-board`.

**On GitLab there is no *project-scoped* slices-done count, and the obvious way to manufacture one is
a trap.** Writing the roster as `- [ ] #N` checkboxes does make GitLab report a completion count —
the mechanism is real, and `phil:issue-board` records it under *A parent's "N of M done" counts
different things on each forge*. But a checkbox is ticked by hand while a slice issue closes on its
own, so the two diverge the first time anyone forgets, and what the feature displays is the state of
the checkboxes, not the state of the work. Leave the roster as bare references: they render each
slice's live state, and an unsummed column of true states beats a summed count of stale ones. Where a
feature-level bar is genuinely wanted, put the slice issues in a **milestone** named for the feature;
what that buys and what it costs are in `phil:issue-board`, in the same section.

## Wave is a fact about the feature, not a column

Do not build a board with discuss · design · distill · deliver columns. nWave is worked one feature
at a time, so those columns hold a single card between them — a progress readout wearing a board's
clothes, and five columns to maintain for it.

Record the wave as a label on the feature issue — `wave::deliver`, or `wave: deliver` where scoped
labels are unavailable — and restate it in the generated block.

**The wave label is single-valued and must be swapped, not added.** Where scoped labels are
unavailable, nothing enforces that, so a feature walked from DISCUSS to DELIVER accumulates four
wave labels and the record of where it stands becomes unreadable while every command reported
success. Remove the old wave in the same call that adds the new one.

**The board that earns its keep is the slice board** — to do · in progress · blocked · done — because
slices are what cross columns inside DELIVER.

Keep **blocked** off the wave label. When the blocker is another issue, use the forge's dependency
link and leave the chain line, both per `phil:issue-board`. A label carries only what no link can
express — waiting on a person, a decision, or an outside event.

## The order of the cards is the order of the work

`roadmap.json` fixes both orders: `phases[]` for the slice cards, `phases[].steps[]` for the rows
inside one. Publish both. A to-do column in a different order is a second schedule, and the one
people act on is the one on the board. The mechanics for setting a position are in
`phil:issue-board` under *A column is a queue, so its order is a claim*.

- **Array order, not id order.** Where anything else implies a different sequence — the slice
  numbers, a dependency noted in a slice file — the array still decides, as it does for the rows.
- **Before `/nw-roadmap` there is no schedule.** Order the cards by slice file number ascending,
  which is the best available guess, and say so beside the roster on GitLab, or in the feature
  issue's description outside the status block on GitHub: `Order: slice number, provisional until
  /nw-roadmap`. A provisional order that admits it gets corrected; one that does not gets worked.
  When the roadmap lands, replace that line with the array order rather than leaving both standing.
- **GitLab** — the roster table rows carry the same order. It is the only rollup there, so it is
  also the only place the order is legible away from the board.
- **GitHub** — the board column and the parent's sub-issue list are two orders, and setting one
  leaves the other alone. Each needs its own write, per issue and per sub-issue; neither follows
  from the order the issues were created in. Both mutations are in `phil:issue-board`, which also
  records that neither has been exercised.
- **A deferred slice takes no position, because it takes no card.** The top of a to-do column
  assigns work to whoever reads it next.

Reposition on the boundaries in *Refresh at boundaries* below — including a roadmap that was
resequenced, which is a boundary precisely because nothing else about the feature moved. Order and
status go stale together, and a card whose column changed but whose row did not is the half-updated
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

```
<!-- nwave:status:begin -->
Wave: DELIVER · generated 2026-08-10T21:04Z
Work this with: /nw-execute

| Step | What it does | Status | Notes |
|---|---|---|---|
| 01-01 | Derives a page ref from a masked url_shape | done | |
| 01-02 | Maps a captured payload to its projection | current | ⚠ no commit found |
<!-- nwave:status:end -->
```

Replace only what is between the markers. Both forges appear to replace a description wholesale on
update, so regenerating without markers destroys any prose a human added — confirm that against
your forge before relying on it. When the markers are absent, append the block rather than rewriting
the description.

Row order is `phases[].steps[]` array order. A step's `deps` may imply a different order and does
not override it.

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

1. **Before DELIVER** — feature issue and wave label. Open slice issues as soon as
   `slices/slice-NN-*.md` exists and attach them to the parent. Before that, say the roster is not
   yet known.
2. **After `/nw-roadmap`** — generate each slice issue's step table.

A slice issue opened in stage 1 **says that its step table arrives with the roadmap**. An issue
carrying neither a table nor that line reads as a slice with no steps, which is the same false
impression the invented rows would have given, arrived at by omission.

A slice file marked `DEFERRED` or out of scope is not a card. Honor the marker; `nwave-slice-status`
treats it as overriding every other source.

## Refresh at boundaries

Slice start, slice end, wave change, roadmap resequenced. Not every step — a per-step write turns
each TDD cycle into a forge round-trip, and a missed one is invisible. Between refreshes,
`/phil:nwave-slice-status`
answers "where are we" locally and writes nothing.

Timestamp the generated block. A projection that states when it was made is honestly stale; one that
does not is indistinguishable from current.

---

## Self-test (regression gate)

`skills/nwave-issue-board/self-test/` holds sixteen fixtures that pin these behaviors: the
end-to-end publish (01, walking skeleton), the `Notes` column surviving the trip to the forge (02),
`unknown` published as `unknown` rather than `not started` (03), a human-set state outranking a
regenerated one (04), hand-written prose surviving a refresh that must replace the whole description
(05), a wave label swapped rather than accumulated (06), no step rows invented before `/nw-roadmap`
(07), a deferred slice never given a card (08), native sub-issues used instead of a hand-written
roster (09), the GitLab roster written in a second pass as bare references (10), the forge never
writing back to the artifacts (11), status decided by `nwave-slice-status` rather than folded here
(12), the column positioned in `phases[]` order rather than the creation order that looks just as
deliberate (13), an order guessed before `/nw-roadmap` published as a guess (14), and a GitLab roster
left as bare references rather than converted to checkboxes to manufacture a progress bar (15), and
the `Work this with:` routing line derived from the wave label — emitted for a labelled card, and
withheld entirely for one with no label rather than guessed (16).

Fixtures 04 and 11 are deliberately adjacent and resolve opposite ways: a person recording something
no artifact can hold is preserved; a person overwriting something the artifacts own is not. Getting
one of them right by a rule that gets the other wrong is a gate failure.

Fixture 08 is the sharpest case — positionally the deferred slice *is* next, and a card on a board
does not misinform someone, it assigns them. Fixtures 13 and 14 are the same mechanism weaker: a
position is an instruction, whether or not anyone chose it. Fixture 15 is that mechanism in the
reporting register — a hand-ticked checkbox, like a card for deferred work, is correct on the day it
is written and authoritative long after.

Fixtures 02 and 12 pin the two faults this skill actually shipped in its first draft: a three-column
block that dropped the drift warning, and a locally invented rule forbidding a status source its
owner permits.

Whenever this skill changes — or `phil:issue-board` or `phil:nwave-slice-status` changes, since this
skill's correctness is partly theirs — drive the fixtures per `self-test/README.md`. Every failure
mode here is silent: the wrong answer arrives as a clean, timestamped table that the whole team
reads.
