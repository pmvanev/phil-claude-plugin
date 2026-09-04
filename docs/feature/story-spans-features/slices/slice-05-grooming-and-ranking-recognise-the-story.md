# Slice 05 — Grooming and ranking recognise the story

**Goal:** Stop the silent failure. Make `groom-issues` pass a correct story card, report the one shape
that is genuinely wrong, and offer a story card where it would have offered a milestone; make
`rank-issues` know that the ranked unit is the card.

**Stories:** S4 (groom without false positives, and catch the real defect), S5 (rank a board whose unit
may be a story), S6 (tell a story from a goal on sight — the prose half)
**Answers:** issue #36's question 4, and its *"Plus"*

## Learning hypothesis

**Disproves C10** — *extend a shipped oracle at the new scale, never loosen it* — if the only way to make
grooming see a story card is to weaken the demonstrability rule. That is the `keep-a-backlog-trustworthy`
anxiety (F) firing: *"An oracle loosened to stop the false positives stops catching the real ones."* If
it fires, the story tier has bought a worse board.
**Confirms**, if it passes, that a vacuously-passing rule is closed by adding a rule that fires, not by
adjusting the one that passes.

## IN scope

### `groom-issues` / `groom-set`

- **The oversized paragraph is extended, not edited** ([D13]). A story card is large, holds several
  demonstrable things, and passes. The `Do not "fix" this rule toward size` sentence gains the story
  case, with the same oscillation reasoning: the family stores no marker, so a declined split returns
  forever and only has to be accepted once.
- **New set-level signal: two features in flight on one story card** ([D12]). Evidence is the fold's
  output and the block's two `▶` rows, quoted. Resolution offered: split into feature cards under a
  goal. Derived from `issue-board:616-625`'s concurrency reading — **not a new granularity rule.**
- **New set-level class: features of one story, carded separately.** Directly parallel to the shipped
  *decomposed feature* class, one level up, and it **supersedes *ungrouped effort* the same way** —
  that class proposes a milestone, which is a goal, where the right container is a story card. Evidence
  ranked as decomposed-feature's is: a `Story:` line in the deltas, **confirmed present in the repo** with
  `git ls-tree`, licenses an offer; a shared title prefix licenses a report only.

### `rank-issues`

- **The ranked unit is the card: a feature or a story.** A story holds one position; its member features
  hold none.
- **The stop condition narrows to slice cards.** A story card does not stop the session.
- A story card and a member-feature card both open: say so and stop, naming `/phil:groom-set`. **Reuses
  grooming's oracle rather than duplicating it** — two detectors over one defect drift.

### The discriminator ([D5], story S6)

Stated where a reader meets it, in one sentence each: **a goal holds cards; a story holds feature
directories.** In `issue-board` beside *a milestone is a goal*, and in `groom-issues` at the
ungrouped-effort supersession. Milestones do not nest; a story is not a milestone; neither replaces the
other.

## OUT scope

- Migrating any existing card. There are no multi-feature cards on this board to consolidate, and
  retro-consolidating closed ones is refused in the delta.
- A `check-invariants.py` validator for the membership declaration. Named as a candidate; a script is not
  this feature's deliverable.
- Any loosening of the demonstrability rule. If that becomes necessary, this slice has failed.

## Acceptance criteria

1. **KPI-4, both sides, pinned by an adjacent fixture pair that resolves opposite ways** — in the style
   of 04/11: a correctly-shaped story card produces **zero** findings; a two-in-flight story card
   produces **one**, quoting both feature names. Getting one right by a rule that gets the other wrong is
   a gate failure.
2. No oversized finding and no split proposal against a correct story card, **verified without modifying
   the rule's demonstrability text**.
3. Several cards that are features of one story are reported as a set, and the offered container is a
   story card — never a milestone. A fixture pins the milestone offer as wrong.
4. `/phil:rank-issues` ranks a board holding a feature card and a story card without stopping, and gives
   each exactly one position.
5. `/phil:rank-issues` **does** stop on a slice card, unchanged.
6. **KPI-5's prose half:** the discriminator sentence appears in both surfaces, and a reader applying it
   to slice 01's card and its goal gets the right answer.
7. Every never-do list that mentions the feature card is checked for whether it now needs to mention the
   story card. A never-do that names one tier and not the other is read as permission at the unnamed one.

## Dogfood moment

Run `/phil:groom-issues` against the real board after slice 01's card exists. **The predecessor measured
this and the number was zero findings on a clean board** — so the informative outcome here is whether the
new check fires when it should, which needs a deliberately wrong card. Build one, scan it, close it.

## Dependencies

- Slices 02, 03 and 04 — the fold, the block and the label are what the new checks read.
- Slice 01's card, as the real correct-shape input.

## Effort

~1-1.5 days. Reference class: the predecessor's slice 05, which verified two shipped oracles held and
reversed one journey rule, at ~1.5 days.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | Three surfaces — `groom-issues`, `groom-set`, `rank-issues` — plus one sentence in `issue-board`. **Over the one-day test at ~1.5 days**, and kept whole because a check and the fixture that would have caught its absence must ship together, per this repo's fold-back rule. Stated as a failed test, not rounded off. |
| Depends on a new abstraction? | On 02-04, all shipped by then. |
| Disproves a pre-commitment? | Yes — that shipped oracles need only extension, not loosening. |
| Synthetic data only? | No — the real board for the clean case, one deliberately-wrong card for the firing case. |
| Duplicate of another slice at scale? | No. Every other slice makes the card *readable*; this makes the board *honest about it*. |

---

## Result — 2026-09-04

**Hand-driven; exercised the prose, not the commands.** Installed plugin is 0.73.0, tree is 0.82.0 —
running `/phil:groom-issues` would have exercised a version predating every rule in this slice, so the
scan below was applied by hand. `plugin-dev:skill-development` consulted this session; `skill-reviewer`
run over the result.

### Acceptance criteria

| AC | Verdict |
|---|---|
| 1 — KPI-4 both sides, adjacent pair resolving opposite ways | **met** — fixtures 41 (zero findings) and 42 (exactly one), on **different oracles**: 41 passes on demonstrability, 42 fires on concurrency |
| 2 — no oversized finding on a correct story card, **without modifying the rule** | **met** — the paragraph was extended; its demonstrability text is byte-unchanged |
| 3 — members carded separately reported as a set, container is a story card never a milestone | **met** — fixture 43 pins the milestone offer as the failure |
| 4 — ranks a board with a feature card and a story card, one position each | **met** — rank fixture 09 |
| 5 — still stops on a slice card | **met** — the stop narrowed, it did not move |
| 6 — the discriminator appears in both surfaces | **met** — `issue-board` beside *a milestone is a goal*, `groom-issues` at the ungrouped-effort supersession |
| 7 — never-do lists checked for tier-naming | **met, and one was found** — see below |

### C10 holds: the shipped oracle was extended, never loosened

The learning hypothesis said this slice fails if the only way to make grooming see a story card is to
weaken demonstrability. **It did not fire.** The oversized rule's text is unchanged; a story card passes
it for the same reason a feature card does, and the genuinely wrong shape is caught by a **different**
oracle — the concurrency signal, derived from `issue-board`'s shipped split clause rather than invented.

**Fixtures 41 and 42 are the proof, and they are built to be un-satisfiable by one tuned rule.** The two
cards are the same size and the same shape; only concurrency differs. A rule tuned to fire on 42 by size
reports 41 every run, and because the family stores no marker, a declined split returns forever while an
accepted one only has to be accepted once — one careless acceptance dismantles a correct story card
permanently.

### AC7 found a real one

`rank-issues` carried *"Re-derive over the **feature cards**; do not adjust"* — a never-do naming one
tier. **A never-do that names one tier and not the other is read as permission at the unnamed one**, and
consolidating features into a story produces exactly that situation one level up: an order that ranked
features over a board that now ranks stories. Widened to *"the cards that exist now — feature cards,
story cards, or both"*, with the reason stated so the next widening is not re-argued.

### The dogfood: the clean half is real, the firing half is not

**Applied the three new checks to the real board by hand:**

- **Two features in flight on one story card** — no. #36's members are `single-issue-per-feature` (done)
  and `story-spans-features` (in progress): **one** in flight.
- **Features of one story, carded separately** — no. Both members declare
  `Story: the-boards-unit-of-work` at column 0 and **both declarations are confirmed pushed**
  (`git ls-tree origin/story-spans-features`), and **neither member is open as a separate card** —
  `single-issue-per-feature`'s card #26 is closed, and `story-spans-features` has none.
- **Oversized / ungrouped effort** — no. #36 is large and demonstrable, and carries the goal
  `Board and session tooling`.

**Zero findings, which the brief predicted would be uninformative — and it was right.** The predecessor
already measured zero on a clean board; the informative case is whether the new checks *fire*.

**The firing case was NOT dogfooded, and that is a real gap.** The brief says *"build one, scan it, close
it."* Building a genuinely detectable wrong card needs **fabricated feature directories under
`docs/feature/`** — the checks read declarations from deltas on the default branch, so a fake card alone
would not trip them. That would pollute the SSOT which `check-product-ssot.py` and both folds read, to
test a rule already pinned by fixtures 42 and 43. **Declined deliberately and recorded here rather than
skipped quietly**, because a slice that omits its own dogfood reads afterwards exactly like one that ran
it.

### Open, raised with the reviewer rather than guessed

**Three supersession relationships now exist and I did not check whether they compose.** *Features of one
story* supersedes *ungrouped effort*; *decomposed feature* also supersedes *ungrouped effort*. Whether all
three can fire on one board, and what is offered then, is unconsidered.

### Review round — `plugin-dev:skill-reviewer`, 2026-09-04

**Verdict: Needs Major Revision — 5 critical, 10 major, the severest round of the five.** All fixed. The
reviewer was given the four defect shapes prior rounds had produced and found **new instances of four of
them**, including the worst one twice.

**C3 is the finding of the whole feature: my evidence spec fired on my own clean fixture.** The
two-in-flight check said *"the block renders two `▶` rows"*. But a story block carries **two tables**, and
slice 04 established that `▶` means `in progress` in the feature roster and `current` in the slice roster.
**So a correct story card with ONE member in flight already renders two `▶` rows** — one for the member,
one for its current slice. The check fires on fixture 41.

That is shape #5 again — a signal with two readings whose fixture pair cannot detect the disagreement,
exactly slice 04's defect. And it defeated the slice's own learning hypothesis: 41 and 42 were built to
prove the two oracles are separate, and as written **both passed under a broken rule**. Now scoped to the
feature roster, reading the **state word** and never the glyph, with 41 gate-failing a glyph count
explicitly — which is the only thing that makes the pair prove anything.

**C1/C2 — `/phil:rank-issues` contradicted itself, in the file and in the loader that precedes it.** Its
*two-level scheme* section still said *"the ranked unit is the FEATURE card"* and *"one issue is one
feature there"* — **eighteen lines above** the new rule, and it is the sentence this feature's own delta
lists as upstream change 3, quoted verbatim with the new assumption recorded beside it. **The amendment
was written down and never applied.** The command description carried it too — sites 11/12 of the
checklist that a prior audit already recorded as missed on five loaders.

**C4 — I specified evidence the scan cannot obtain.** The two-in-flight check's first conjunct is the
fold, which `/phil:groom-issues` cannot run; the new class's offer tier needs `git ls-tree`, which is
`/phil:groom-set`'s grant. And fixture 43 was written against the scan while demanding an *offer* the scan
is structurally forbidden to make. Both are now report-only for the scan on the shipped unlinked-path
pattern, and 43 moved to `/phil:groom-set`.

**M4 — three classes can now fire on one set and nothing ordered them**, which is the interaction I raised
without resolving. The discriminator existed in my head and nowhere on the page: **same feature directory
→ decomposed feature; different directories sharing one `Story:` slug → this class.** Written down.

**M5 — I imported a hazard its own premise makes impossible.** *Un-parent before closing* presupposes a
parent edge, which is decomposed-feature's defining evidence; this class is defined by the **absence** of
any forge grouping, so there is no edge to remove. Shape #3 in structural form.

**M6/M7 — the new operation had no shapes, no closed-card search, and three invented outcomes.** Its
`APPLY-CONSOLIDATE` rider demanded a shape name it could not supply, and the two-in-flight refusal was a
terminal stop with no outcome at all. Now two shapes, a mandated closed-card search, and
`REFUSE-CONCURRENT`. The fixtures use the declared vocabulary instead of three tokens the skill does not
have.

**AC7 was not met after all.** I audited for *"feature card"* and widened `rank-issues`, but missed two in
`groom-issues` — the oversized never-do and *"conclude that no feature card exists without searching closed
issues"*. Both now name each tier.

**Also fixed:** four false counts; *"story"* carrying two senses in one file, where the generic sense
positively licensed splitting a story card; the supersession asserted unconditionally where its model
states it conditionally and its premise can be false; arity-two phrasing where three members are
reachable; the two rank stops overlapping with the wrong one written first; the journey enumerations.

**Clean on independent check:** the demonstrability rule is byte-unchanged, so AC2 holds; the discriminator
sentence is verbatim across all six sites it now appears in.
