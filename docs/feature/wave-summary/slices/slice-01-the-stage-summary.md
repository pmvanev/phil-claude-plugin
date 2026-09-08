# Slice 01 — The stage summary, against the largest artifact in the repo

**Goal:** Ship `/phil:nwave-wave-summary <feature>`, turning one finished feature delta into 200 words of
plain English with no internal handles.

**Stories:** S1
**Answers:** issue #39's naming, scale and enforcement questions, at the stage level

## Learning hypothesis

**Disproves the feature if 9,447 words cannot become 200 that a reader acts on.** Forty-fold compression
is the real ask, and the failure mode is not length — it is a summary that is short, fluent and useless,
saying *what the stage was about* rather than *what it decided*.

**Confirms**, if it works, that the compression is the deliverable and slice 02 is a variation on a
solved problem rather than a second problem.

**The cheaper failure is worth naming too:** if the output is 200 words of accurate abstraction that
nobody can act on, the ceiling is not the constraint that matters and the design should optimise for
*decisions named* rather than for length.

## IN scope

- One command and one skill, per `plugin-dev` at authoring time.
- Reading one `docs/feature/<id>/feature-delta.md`. **[D6]** — a name may be given; with none, the most
  recently completed.
- **[D4]** — the 200-word ceiling, counted with `scripts/plain_language.py`. Fourth consumer of the
  module; the counter is imported, never re-derived.
- **[D5]** — the strictest vocabulary list in the repo: portable classes plus bare handles, **and card
  numbers forbidden too**. This surface has no column to put a number in.
- **[D11]** — where a decision matters, state the decision, never its number.
- **[D9]** — a stage that recorded nothing is reported as recording nothing.
- **[D7]** — `mutates: false`, verified by `scripts/check-readonly-commands.py`. No forge, no network.
- The command names which artifact it read.
- **A fixture against the largest real delta, currently `story-spans-features` at 9,447 words**, plus one
  against a feature whose artifact is absent or empty.
- Version bump.

## OUT scope

- The slice summary and its `--slice` argument — slice 02.
- Any status derivation. **[D8]**, and the reason is drift, not cost.
- Writing into `docs/feature/`, or publishing to a card.
- Editing the source artifact. A summary is not a licence to shorten what it read.
- Summarising anything other than a feature delta. Other artifacts exist; none was measured.

## Acceptance criteria

S1's five. KPI-1 and KPI-3 are the numbers; KPI-2 is the vocabulary.

## Dependencies

`scripts/plain_language.py`, shipped 2026-09-08.

## Effort

Half a day. One file read, one composition, two fixtures, one import.

## Reference class

`board-snapshot` slice 01 — a read-only command over a new skill, shipped in one slice with its fixtures
and a driver.

## Dogfood moment

Same day: summarise `board-snapshot`'s own delta — written this week, so its accuracy is checkable by the
person reading the summary. **Name the plugin version the run exercised**, per `CLAUDE.md`.

## Taste tests

- **Ships 4+ new components?** No — one command, one skill.
- **Depends on a new abstraction?** No. The one it needs already exists and has three consumers.
- **Disproves a pre-commitment?** Yes — that 200 words can carry a stage's decisions at all.
- **Synthetic data only?** No. Fifteen real deltas, and the fixture uses the largest.
- **Identical to another slice but for scale?** Slice 02 differs in input and in question, not in scale
  alone — it folds git history the stage summary never reads.

## Pre-slice SPIKE

None. The input is a file in the repo and the compression is the work.
