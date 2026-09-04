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

---

## Result — 2026-09-04

**Hand-driven.** The installed plugin is 0.73.0 and this tree is 0.79.0, so this exercised the **prose**,
not the command. `plugin-dev:skill-development` and `command-development` were consulted **before** the
files were written, per `CLAUDE.md`; `skill-reviewer` and `plugin-validator` ran over the result.

### The dogfood — AC1

Applied `--story-state the-boards-unit-of-work` by hand against the two real deltas:

1. **Discovery.** `grep -l '^Story: ' docs/feature/*/feature-delta.md` returns exactly two features —
   `single-issue-per-feature` (position 01) and `story-spans-features` (position 02). The other eleven
   feature directories declare no story and are correctly absent from the roster.
2. **Member states**, each from the *feature* fold over that member's own roster:
   - position 01 → **`done`**. Six slices done; slice 06 is retired, so *"every slice that is not
     `deferred` is `done`"* holds.
   - position 02 → **`in progress`**. Slice 01 is current.
3. **Story fold** — *"any feature is `done` or `in progress`"* → **`in progress`**.

```
Story: the-boards-unit-of-work — in progress · 1 of 2 features done · current feature story-spans-features
```

**This matches the line the feature-delta predicted at authoring time, character for character**, which
is a weaker check than it looks — the same author wrote both. The load-bearing comparison is the next one.

**Against the hand-placed column: AGREES.** Issue #36 was placed in **In Progress** by hand in slice 01,
before this fold existed. The fold independently answers `in progress`. The brief says a disagreement
would have been the finding; there is none, so the derivation and the human judgement concur on the one
case available.

### Acceptance criteria

| AC | Verdict |
|---|---|
| 1 — emits the state line for the real story | **met**, above; agrees with the hand-placed column |
| 2 — empty-roster guard fires, no count, pinned | **met** — fixture 17, pinned on its conjunction |
| 3 — the fold is written **once** | **met** — expressed as the feature fold plus a four-row substitution table (`slice`→`feature`, slice status→feature state, `current`→`in progress`, `next`→absent). No second seven-row table exists. |
| 4 — `--story-state` with a slice number refused as a contradiction | **met** — scope-table row, in the style of the `--feature-state` row |
| 5 — nothing reads a forge | **met** — discovery is a grep over `docs/feature/`; membership is declared in the artifacts |
| 6 — `description` frontmatter gains the story question | **met** — *"what state is this story in"*, *"how far through the story are we"* |

### Learning hypothesis: C5 HOLDS

**Confirmed.** The fold needed no forge fact. Membership is declared per-feature in `docs/feature/`, so
`--story-state` is a pure artifact read and the mapping skill stays a renderer. The story tier cost
exactly **one flag and one declared line**, as predicted. [D9] does not have to move.

### Findings

1. **Slice 01's finding 2 is now fixed where it belongs.** The retired-slice-06 case is pinned by fixture
   16, which asserts the *count* rather than the state — because the story answer is `in progress` either
   way, so a wrong member state is invisible in the verdict and visible only in `1 of 2`. A fixture
   asserting only the state would have passed over the defect.
2. **`argument-hint` was prose-laden and is now a bare token list.** Flagged by the baseline validator,
   and `plugin-dev:command-development` confirms the convention is `[token] [token]`. Fixed while editing
   the field rather than left as a known deviation.
3. **The membership declaration is still unvalidated.** Fixture 18 pins that a collision is *named*, which
   is this skill's honest boundary — but nothing prevents one. The `check-invariants.py` candidate
   recorded in the delta is now the only remaining guard, and it is uncommitted to.

### Out of scope, confirmed untouched

No rendering. No wave-label logic. No forge read. No validator script.

### Review round — `plugin-dev`, 2026-09-04

`skill-reviewer` returned **Needs Improvement** with 2 critical and 5 major findings;
`plugin-validator` returned **PASS** with 5 documentation-consistency regressions. They agreed
independently on two of them, which is the corroboration worth having. All are fixed.

**The two criticals were both "a fixture asserting what the prose does not say" — the exact class this
slice's fixtures exist to prevent, committed while writing them.**

| # | Finding | Fix |
|---|---|---|
| C1 | **Fixture 18's expected output performed the silent tie-break its own gate list forbids.** It named `current feature chat-in-web-ui` where two members claim position 02 — "first" only by alphabetical directory name. Worse, `current feature` was **defined nowhere in the skill**; it appeared once, inside the render template. | Defined it (`the first member, in position order, whose state is not done`), and settled the contested case: the state answers, **the ordinal does not** — `current feature contested — position NN claimed by <a> and <b>`. Fixture 18 rewritten, and its gate list now names `chat-in-web-ui` as the *plausible* wrong answer. |
| C2 | **Fixture 16 gated on a retirement marker Step 2 did not document.** It required slice 06 to fold `deferred` on `— SUBSUMED BY SLICE 07`, while the prose recognised only `**Status:**` and `DEFERRED` / `OUT of v<N>`. A reader following the skill correctly **fails the fixture**. | Widened Step 2 to cover `RETIRED` / `SUBSUMED BY <slice>` in the heading and `Retired <date>` / `Superseded by <slice>` in the body, citing the measured case. This is slice 01's finding 2, now actually fixed rather than only recorded. |

**Majors.** The substitution table was incomplete in two ways, and the second mattered: `not started` →
`to do` was missing (leaving the final row's condition unmatchable), and **the empty-roster guard row
does not survive a literal substitution at all** — "no slice files and no roadmap phases" is meaningless
at story scale, so the instruction *"apply with exactly these substitutions"* could not derive the very
row fixture 17 exists to test. Both rows added. Discovery was under-specified: the scan is now
**anchored at column 0**, because `story-spans-features/feature-delta.md` holds seven `Story:` matches
and only one is a declaration — one decoy reads `Story: the-boards-unit-of-work · 2 features` and would
parse as a conflicting second declaration of the same slug. The anchor was in this brief and never made
it into the skill.

**Both reviewers independently caught the same stale claim.** The skill and the suite README each said
fixture 14 was *the only* fixture whose failure mutates. Fixture 17 falsified that on the day it was
added, and **both sentences were byte-identical to the version where they had been true** — which is how
a stale claim survives review: nothing about it changed. Corrected in both, with the retired sentence
quoted and dated rather than deleted, and `17` added to the README's safety core it had been nominated
for and omitted from.

**One validator finding was a real portability catch:** fixture 17's `expected_state` read
`"unknown (both cases)"`, not one of the six state tokens. `tests/test_ux_review_fixtures.py` does
exactly that token check for a sibling suite, so a harness modelled on this repo's own pattern would
have failed on it. Now a bare `unknown`, with the conjunction moved to `expected_guard`.

**Also fixed:** fixture 16's manifest pointed at a live in-flight feature and was already stale in the
commit that added it — the rosters are now frozen with an expiry note, because when slices 03-05 land
the tree would fold position 02 to `done` and the fixture would fail for no defect. The stop instruction
covered only the table path, not the two folds. `Notes` had two shapes across the new fixtures and none
in the template. A pre-existing garbled sentence from 0.74.0 was repaired while in the file.

**Held, with evidence:** the fold is written once (a substitution table, not a duplicate — the reviewer
checked the fixtures for a shadow copy too); nothing reads a forge, and the reviewer noted this is
**structural rather than promised**, since the command's grant contains no route to `gh`; no rendering
crept in; the conjunction is genuinely pinned; the description is 764 chars, under the 1024 limit.
