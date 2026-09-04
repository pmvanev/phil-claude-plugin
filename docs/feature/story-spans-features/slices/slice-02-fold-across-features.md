# Slice 02 — The fold across features lands with its owner

**Goal:** Give `phil:nwave-slice-status` a story-level state folded across features, plus the membership
declaration it reads, so a caller placing a story card never invents a column.

**Stories:** S3 (place a story card in a column without inventing its state)
**Answers:** issue #36's question 2

## Learning hypothesis

**Disproves C5** — *derivation stays with its owner* — if the fold cannot be written without the deriver
knowing forge facts. If `--story-state` needs to read a card to learn what a story contains, the
ownership split is wrong and the membership decision ([D9]) has to move before anything else is built.
**Confirms**, if it passes, that the story tier costs one new flag and one declared line, and that the
mapping skill stays a renderer.

Second on learning leverage because everything downstream assumes a story has a derivable state, and this
is the cheapest place to find out that it does not.

## IN scope

- **The membership declaration** ([D9]): `Story: <slug> · position NN` on the header line of
  `docs/feature/<id>/feature-delta.md`. Documented in `nwave-slice-status` as an input, and applied to
  both members of slice 01's story. **This edits
  `docs/feature/single-issue-per-feature/feature-delta.md`, which the DISCUSS pass was forbidden to
  touch** — a one-line header addition, not a content change, and it is named here so the commit is not
  the first place anyone learns of it.
- **Membership discovery**: scan `docs/feature/*/feature-delta.md`; the story's roster is the features
  declaring that slug, ordered by `position`. A missing position sorts last and says so; a collision is
  named in Notes, never silently resolved.
- **`--story-state <slug>`** in `commands/nwave-slice-status.md` and the skill, with the fold table:

  | Test, applied in order | State |
  |---|---|
  | The roster is empty — no feature declares this slug | `unknown` |
  | The current feature is `blocked` | `blocked` |
  | Every feature that is not `deferred` is `done` | `done` |
  | Any feature is `done` or `in progress` | `in progress` |
  | Every feature is `deferred` | `deferred` |
  | Any feature is `unknown`, and none is `done` or `in progress` | `unknown` |
  | Otherwise — every feature `to do` | `to do` |

- The output line: `Story: <slug> — <state> · N of M features done · current feature <id>`, with **no
  count on the empty-roster case**.
- Fixtures pinning: the fold over mixed states; the **empty-roster guard**; a position collision named
  rather than resolved.

## OUT scope

- Any rendering. The mapping skill's block is slice 03.
- The wave label — that is per-feature and is slice 04.
- A validator for the declaration. Recorded as a `check-invariants.py` candidate in the delta; a script
  is not this feature's deliverable.
- Cross-repository membership.

## Acceptance criteria

1. `/phil:nwave-slice-status --story-state the-boards-unit-of-work` emits the state line for slice 01's
   real story, from the two real deltas.
2. **The empty-roster guard fires**: a slug no feature declares folds to `unknown`, never `done`, and
   carries no count. Pinned by a fixture.
3. The fold is written **once**, as the feature fold with features substituted for slices —
   `current` reading as `in progress`, `next` absent. If the two folds are written twice, they will
   drift, which is the exact reason this skill owns both.
4. A `--story-state` combined with a slice number is refused as a contradiction, in the style of the
   existing `--feature-state` row.
5. Nothing in this slice reads a forge.
6. The skill's `description` frontmatter gains the story question, so the skill is reachable from
   *"what state is this story in"*.

## Dogfood moment

Run `--story-state` against slice 01's real story and compare the answer to the column that card was
hand-placed in. **A disagreement is the finding**, not a bug in the fixture.

## Why the guard is called out as its own AC

Fixtures 14 and 15 exist in this skill because the feature fold shipped without an empty-roster guard:
every universal below it is vacuously true over an empty set, so it answered `done`, `done` maps to the
Done column, and auto-close turns the rendering into a **closed issue**. That fold reached production
before the hole was found. **The story fold has the identical shape and would fail identically, one level
up, where the closed card holds N features.** It is inherited only if it is re-pinned; a shared shape is
not a shared test.

Fixture 15's lesson transfers too: the guard must be tested on its **conjunction**. A story with declared
members but no readable deltas and a story with readable deltas but no members must resolve differently,
or a guard weakened to one clause stays green.

## Dependencies

- Slice 01's read passes, or its failure has redirected the design.

## Effort

~1 day. Reference class: the feature-level fold added to this skill on 2026-08-14, which was one table,
one output line and three fixtures.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one flag, one fold table, one declaration convention, in one skill. |
| Depends on a new abstraction? | On the membership declaration, which ships **inside this slice** rather than being assumed by it. |
| Disproves a pre-commitment? | Yes — that the ownership split survives a fold whose input type changed. |
| Synthetic data only? | No — the real deltas of two real features, plus synthetic fixtures for the guard, which is the only way to build an empty roster on purpose. |
| Duplicate of another slice at scale? | No. This derives; 03 renders. The whole point is that they are different skills. |
