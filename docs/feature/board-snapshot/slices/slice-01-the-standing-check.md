# Slice 01 — The standing check, on a board that will barely fill it

**Goal:** Ship `/phil:board-snapshot` printing blocked, in flight and the next five, at or under 200
words, against this repo's real board.

**Stories:** S1
**Answers:** issue #34's open questions on N, on empty sections, and on where the drift check belongs

## Learning hypothesis

**Disproves [D1]'s default — that the standing check is the read people want most — if running it on
this board produces something nobody reads twice.** This board has zero blocked and zero in flight, so
the output is one sentence saying so plus five queued titles. If that reads as useless rather than as
reassuring, the card's own specification is the wrong default and slice 02 becomes the feature.

**Confirms**, if it reads as reassuring, that an almost-empty board is the *normal* case and the ceiling
is generous rather than tight — which changes what slice 02 has to fit into.

**This slice exists to be able to fail.** It is the cheapest possible test of the card's central claim,
and the claim has never been exercised because nobody has ever run it.

## IN scope

- One command file and its knowledge, wherever `plugin-dev:command-development` says it belongs. Whether
  a new skill is warranted or `phil:issue-board` absorbs it is decided at authoring, not here.
- The project-items read, **as a GraphQL document using variables** — the interpolated form failed to
  parse on 2026-09-08 and a command cannot write a temp file inside its grant.
- Three sections, in order: blocked, in flight, queued. Board order consumed, never computed, and the
  output says where the order came from.
- **[D5]** — one leading sentence naming empty sections; no empty headings.
- **[D6]** — N defaults to 5, is an argument, and a ceiling breach prints fewer plus the count withheld.
- **[D7]** — the drift line: an open card in Done, or a closed one outside it, in one line, only when it
  fires, counting against the budget, pointing at the audit.
- **[D8]** — slice-card inflation reported in one line, never consolidated, never refused.
- **`UNCOLUMNED`, added to this slice's scope after the brief was written.** A card on the project with no
  Status belongs to none of the three sections, so it vanishes from a read whose whole purpose is saying
  what is there. It comes free from the same call as the drift line and costs one line. Recorded here
  rather than discovered later — an addition nobody wrote down is indistinguishable from scope creep.
- **[D9]** — `mutates: true`, read-only intent in prose, `scripts/check-readonly-commands.py` passing.
- **A fixture pinning KPI-1 on a synthetic board large enough to breach the ceiling** — at least one
  blocked, one in flight, five queued. The card demands this and it is the only test that tests anything.
- Version bump.

## OUT scope

- The per-card table and its flag — slice 02. Shipping both here would mean a failed hypothesis wasted
  the second mode too.
- The shared checker — slice 02's precursor, per [D12]. This slice counts its own words inline, and that
  duplication is deliberate: extracting against one call site is speculation.
- Stripping internal vocabulary — slice 03. Section headings and card titles pass through as they are.
- Any write to the forge, any fix to anything the read reveals.

## Acceptance criteria

S1's five, unchanged. KPI-1 is the one that can fail the feature.

## Dependencies

None. The board constants are in `CLAUDE.md` and the `project` scope is present.

## Effort

Half a day. One forge call already proven by hand, one composition step, one fixture.

## Reference class

`phil:nwave-slice-status` — a read-only command over an existing skill, shipped in one slice.

## Dogfood moment

Same day: run it against this board, in the session that ships it, and paste the output into the card.
**The dogfood must name the plugin version it exercised**, per `CLAUDE.md` — a run against the cached
snapshot is a claim about that snapshot, not about the working tree.

## Taste tests

- **Ships 4+ new components?** No — one command, optionally one skill.
- **Depends on a new abstraction?** No, deliberately. That is [D12].
- **Disproves a pre-commitment?** Yes — the card's default mode.
- **Synthetic data only?** No. The live board is the input; the synthetic board exists only to breach the
  ceiling, which this board cannot do.
- **Identical to another slice but for scale?** No.

## Pre-slice SPIKE

None needed. The uncertain mechanic — reading Status and board order in one call — was executed by hand
on 2026-09-08 and its failure mode recorded.
