---
name: nwave-issue-board
description: Use when an nWave feature needs to exist on a GitLab or GitHub board — putting a feature and its slices on the tracker, opening an issue per slice, recording which wave a feature is in, refreshing the step table inside a slice's issue, or deciding what a feature, slice, and step each become in a forge. Covers only the mapping; `phil:issue-board` owns the forge mechanics and `phil:nwave-slice-status` owns the status.
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

`roadmap.json` supplies step **ids and order**. It is not the status source, but neither is it
forbidden as one: a project that maintains a per-step `status` field is a case
`nwave-slice-status` already handles. Take whatever it returns.

## Attach slices to the feature natively

GitHub carries the feature→slice edge as a real sub-issue relationship; the commands and the `gh`
version they were verified against are in `phil:issue-board` under *Dependencies depend on the
tier*. Use them rather than describing the hierarchy in prose.

Where the forge maintains the parent's rollup, **do not also hand-write a slice roster table into
the feature description** — that is a second copy of something the forge already keeps, and the
hand-written copy is the one that goes stale.

`glab issue update` exposes no parent or child flag, and GitLab hierarchy means epics, which are
Premium and group-scoped. So on GitLab the feature description carries a roster table of bare `#N`
references, and that is the only *project-scoped* rollup available. Two things govern it:

- Keep the references **bare**. `#N` renders live state; a markdown link freezes it. The reasoning
  is in `phil:issue-board` under *Link what the forge cannot resolve*.
- Slice numbers exist only after the issues are created, so the roster is a **second pass** — see
  *Bulk seeding needs two passes* in `phil:issue-board`.

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

## Publishing does not overwrite what it cannot know

The vocabulary is `nwave-slice-status`'s. Two of its cases matter especially when writing to a
forge, because the forge copy has the widest audience:

- **`unknown` is not `not started`.** Publish it as `unknown`. Reporting work you cannot assess as
  untouched is a claim someone will act on.
- **A human-set state outranks a regenerated one.** Someone marking an issue *awaiting input* has
  recorded something no artifact contains. A refresh that replaces it with a derived value reports
  success while destroying the only record of why work stopped. Preserve it and note the derived
  state beside it.

## Generate into a delimited block

Publish `nwave-slice-status`'s table **with its `Notes` column intact**. Notes is where drift,
disagreeing sources, and missing artifacts are recorded, and dropping it on the way to the forge
sends the cleanest-looking version of the table to the largest audience.

```
<!-- nwave:status:begin -->
Wave: DELIVER · generated 2026-08-10T21:04Z

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

A slice file marked `DEFERRED` or out of scope is not a card. Honor the marker; `nwave-slice-status`
treats it as overriding every other source.

## Refresh at boundaries

Slice start, slice end, wave change. Not every step — a per-step write turns each TDD cycle into a
forge round-trip, and a missed one is invisible. Between refreshes, `/phil:nwave-slice-status`
answers "where are we" locally and writes nothing.

Timestamp the generated block. A projection that states when it was made is honestly stale; one that
does not is indistinguishable from current.
