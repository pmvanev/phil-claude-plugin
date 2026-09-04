# Slice 03 — The mapping becomes normative

**Goal:** Turn slice 01's hand-built layout into a rule in `phil:nwave-issue-board` — the story tier, the
two-table bound, its refusal list, and the second glyph vocabulary — and re-measure at four features.

**Stories:** S1 (read both positions from one card)
**Answers:** issue #36's question 1

## Learning hypothesis

**Disproves the bound** if it holds only for one careful hand-build: if a written rule cannot be applied
to domain example 1's four-feature story and still produce a thirty-second read, the answer to question 1
is not "one expanded path" and the layout has to change before four more surfaces depend on it.
**Confirms**, if it passes, that the bound scales and that slices 04 and 05 can assume it.

## IN scope

- The mapping table gains the story row: **a card is a story where a feature declares membership, a
  feature otherwise** ([D2]). Slice and step rows unchanged.
- **The bound, restated as its purpose rather than as a count** ([D6]). Replaces
  *"the roster and the current slice's steps are the only tables in the block"* with: exactly one
  feature's slices and one slice's steps are enumerated; every sibling is a row with a link. **At the
  feature tier this must produce the original two tables verbatim** — that identity is the test of a
  faithful restatement, and it is an AC below.
- **The refusal list**, written as refusals because a bound stated only positively gets read as a
  minimum: no slice roster for any feature but the current one; no step table for any slice but the
  current one; **no slices indented as sub-rows of the feature roster** ([D7]); no per-feature `Why` /
  `Next` / `Stack` — a story card carries exactly one stack, because a stack belongs to a person.
- **The second glyph vocabulary.** The feature roster renders the fold's six values, not the slice
  table's seven. `in progress` → `▶`, `to do` → `·`, plus the four already mapped. `next` does not exist
  at feature level.
- The `Story:` header line, carrying the slug and the feature count.
- Fixtures: the two-table block at four features; the feature-tier block byte-unchanged; an indented tree
  refused; a feature-state value with no glyph failing rather than degrading to `·`.

## OUT scope

- The wave label and the routing line — slice 04.
- Grooming and ranking — slice 05.
- The fold — landed in 02 and consumed here, never recomputed.

## Acceptance criteria

1. A four-feature story (domain example 1) renders as one feature roster plus one slice roster, and the
   block is re-read against KPI-1 at that scale. **Slice 01's number is not inherited.**
2. **KPI-3:** rendered rows ≤ features + current feature's slices + current slice's steps. Never the
   product. Counted on the fixture.
3. **The feature-tier regression:** every existing `nwave-issue-board` fixture that renders a
   single-feature card passes unchanged. A restatement that alters the shipped output is a wrong
   restatement, whatever it says about stories.
4. A fixture pins an indented feature/slice tree as **refused**, with the reason.
5. Every one of the fold's six values has a glyph; a fixture supplies a seventh value and the generator
   fails rather than rendering `·`.
6. The block reads its state from `--story-state` and computes nothing ([D8]). A fixture pins a locally
   folded state as a gate failure — this skill's recurring defect, in the form it took on 2026-08-14.
7. Sibling links are **summarised, not bare** — one clause per link saying what it holds. Promoted from
   the predecessor's slice 01, where the reader volunteered it and nothing required it.

## Dogfood moment

Regenerate #36's block from the written rule rather than by hand, and diff it against slice 01's. **Any
difference is either a rule the hand-build got wrong or a rule that got written wrong**, and which one it
is has to be decided rather than reconciled.

## The trap this slice exists to avoid

Question 1's two candidates — *features with slices demoted a level* and *a per-feature roster section* —
sound like a layout choice. They are a scale choice: the second is `N × M` rows, which at four features
of six slices is 24 rows before the current slice's steps, against a budget measured at seven. **And
"demoted a level" has a wrong reading that looks like the right one** — indenting slices under features
in one table renders exactly the same `N × M`, flat. The refusal list exists because the correct answer
and the failure are one word apart.

## Dependencies

- Slice 02's `--story-state`, which this consumes.
- Slice 01's measured number, as the baseline the four-feature read is compared against.

## Effort

~1 day. Reference class: the predecessor's slice 02, which made a projection format normative across one
skill and realigned its fixtures.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | One skill, one bound, one refusal list, one glyph table — all in `nwave-issue-board`. |
| Depends on a new abstraction? | On slice 02's fold, which has shipped. |
| Disproves a pre-commitment? | Yes — that the bound survives being written down and applied at four features rather than two. |
| Synthetic data only? | Mixed, and deliberately: the regeneration of #36 is real; the four-feature story is a fixture, because no four-feature story exists in this repo to be real about. Stated rather than papered over. |
| Duplicate of another slice at scale? | No. 01 discovers the layout; this asserts it and re-measures where 01 could not. |
