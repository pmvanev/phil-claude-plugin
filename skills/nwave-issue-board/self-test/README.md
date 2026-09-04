# phil:nwave-issue-board — Acceptance Self-Test

The `phil:nwave-issue-board` **publisher** is the software under test. Its bugs are worse than its
sibling's, and for one reason: `nwave-slice-status` renders a wrong table into a terminal, where one
person reads it and moves on. This skill writes the wrong table into an issue description, where the
team reads it, for as long as it stands.

Every failure here ships as a clean, well-formed, timestamped table. A dropped `Notes` column looks
tidier than the honest version. A regenerated block that erased "blocked — waiting on Sam" reads as
healthy progress. A wave label that accumulated instead of swapping still renders. None of these look
like failures. They look like a board that is up to date.

These fixtures feed the skill known project and forge states and assert each produces the correct
**decision outcome** (`PUBLISHED` / `NOTES-PRESERVED` / `UNKNOWN-PUBLISHED` / `HUMAN-STATE-KEPT` /
`BLOCK-DELIMITED` / `WAVE-SWAPPED` / `NO-ROWS-BEFORE-ROADMAP` / `DEFERRED-ROW-NOT-OMITTED` /
`GENERATED-ROSTER` / `ONE-WAY` / `OWNER-DECIDES` / `ROSTER-ORDER-FOLLOWS-ROADMAP` /
`ORDER-STATED-AS-PROVISIONAL` / `ROSTER-NOT-CHECKBOXES` / `ROUTING-LINE-DERIVED` /
`PROJECTION-BOUNDED` / `NO-COLUMN-WRITTEN` / `WHOLE-BLOCK-REGENERATED` / `STORY-BLOCK-BOUNDED` / `FEATURE-TIER-UNCHANGED` /
`INDENTED-TREE-REFUSED` / `UNRENDERABLE-STATE-FAILS` / `CONTESTED-CURRENT-NOT-RESOLVED` /
`ONE-LABEL-CURRENT-FEATURE` / `BACKWARDS-STEP-EXPLAINED` / `NO-ROUTING-ROW-STATED` /
`TWO-IN-FLIGHT-VISIBLE` / `CURRENT-FEATURE-FROM-OWNER` / `PROSE-STANDARD-APPLIED` /
`DERIVED-CELLS-UNTOUCHED`).

This suite is the **acceptance + regression gate** for `skills/nwave-issue-board/SKILL.md`. Run it
whenever that file changes, and whenever either skill it delegates to changes — `phil:issue-board`
or `phil:nwave-slice-status` — because this skill's correctness is defined partly by theirs. Format
and intent mirror `skills/nwave-slice-status/self-test/`.

## Why the numbering skips 10

`10-gitlab-roster-second-pass` was **retired on 2026-08-14**. It pinned a roster written in a second pass as
bare `#N` references, because slice numbers existed only once the slice issues had been created. Slices are
no longer issues, so there is nothing to wait for and no second pass to get wrong.

Retired rather than renumbered: renumbering would invalidate every reference to fixtures 11 through 19 in
this file, in `SKILL.md`, and in the feature's slice briefs, to save one integer. The gap is a question, and
this section is its answer.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected outcome |
|---|---|---|---|
| `01-publish-happy-path/` | feature, two slices, roadmap and log agree; GitHub (**walking skeleton**) | publishes the block as one card, writes nothing back | `PUBLISHED` |
| `02-notes-column-survives/` | a step is recorded done with no commit touching its files | the `Notes` drift marker reaches the forge, not just the terminal | `NOTES-PRESERVED` |
| `03-unknown-published-as-unknown/` | roadmap present, no status recorded anywhere | publishes `unknown`; never `not started` | `UNKNOWN-PUBLISHED` |
| `04-human-state-outranks-refresh/` | issue says *awaiting input — waiting on Sam*; log says the step ran | preserves the human state; does not overwrite with a derived one | `HUMAN-STATE-KEPT` |
| `05-no-markers-append/` | issue description is hand-written prose, no `nwave:status` markers | appends the block; never rewrites the description | `BLOCK-DELIMITED` |
| `06-wave-swaps-not-accumulates/` | feature moves DISTILL → DELIVER on a forge without scoped labels | removes the old wave in the same call that adds the new | `WAVE-SWAPPED` |
| `07-no-rows-before-roadmap/` | feature is in DESIGN; `slices/` exists, `roadmap.json` does not | generates the roster, invents no step rows, and says whether a table is coming **or never will be** | `NO-ROWS-BEFORE-ROADMAP` |
| `08-deferred-slice-is-a-row/` | slice 03 is marked DEFERRED and is positionally next | gives it a `⊘` row rather than omitting it, and points at 04 | `DEFERRED-ROW-NOT-OMITTED` |
| `09-generated-roster-no-subissues/` | GitHub, where native hierarchy is available and tempting | creates no slice issue; generates the roster instead | `GENERATED-ROSTER` |
| `11-forge-never-writes-back/` | issue was hand-edited to `done`; the log disagrees | treats the artifacts as authoritative; changes no file | `ONE-WAY` |
| `12-owner-decides-status/` | `roadmap.json` carries a per-step `status` field (**the real edd-loop case**) | publishes what `nwave-slice-status` returns, not a local fold | `OWNER-DECIDES` |
| `13-roster-order-follows-roadmap/` | `phases[]` reads 01, 03, 02, 04; the slice numbers ascend and agree with each other | orders the roster rows by array order, not by the numbers that agree | `ROSTER-ORDER-FOLLOWS-ROADMAP` |
| `14-guessed-order-says-so/` | DESIGN wave, three slices, no `roadmap.json`; GitLab | orders by slice number and marks the order provisional | `ORDER-STATED-AS-PROVISIONAL` |
| `15-roster-not-checkboxes/` | two of four slices done, a slices-done count is wanted | keeps generated glyphs; manufactures no hand-ticked count, on either forge | `ROSTER-NOT-CHECKBOXES` |
| `16-routing-line-from-wave-label/` | a labelled card, an unlabelled one, and **a wave the routing table does not cover** | derives the line, withholds it, or withholds it *and says the table does not cover this path* | `ROUTING-LINE-DERIVED` |
| `17-projection-bounded-to-current-slice/` | 22 phases, 94 steps, slice 07 current | renders 22 roster rows plus 4 step rows; never all 94 | `PROJECTION-BOUNDED` |
| `18-unknown-state-writes-no-column/` | the owner folds `unknown`; the board offers Todo, In Progress, Blocked, Done and nothing that means it | leaves the card's column untouched and says so in the block | `NO-COLUMN-WRITTEN` |
| `19-block-has-one-writer/` | a slice boundary refreshes the position; the handoff feeding the reasoning has not changed | regenerates the whole block from both sources; edits neither region alone | `WHOLE-BLOCK-REGENERATED` |
| `20-story-block-four-features/` | four features declare one story, six slices each, on **GitLab Free** | renders 4 feature rows + the current feature's 6 slice rows = **10**, never the 24 the product would give | `STORY-BLOCK-BOUNDED` |
| `21-feature-tier-block-unchanged/` | fixture 01's exact input, replayed against the **restated** bound | a single-feature card renders byte-identically to what shipped before the story tier existed | `FEATURE-TIER-UNCHANGED` |
| `22-indented-tree-refused/` | fixture 20's story as **one** table with 24 slices indented as sub-rows | refuses it — the bound counts enumerated slices, not tables; the old count-form would have passed this | `INDENTED-TREE-REFUSED` |
| `23-feature-state-without-glyph-fails/` | the owner returns a feature state the glyph table does not cover | fails loudly, naming the value; never degrades it to `·` | `UNRENDERABLE-STATE-FAILS` |
| `24-contested-current-feature-not-resolved/` | the owner returns `current feature contested` because two members claim one position | renders the roster and **no** slice roster; never picks a contender to expand | `CONTESTED-CURRENT-NOT-RESOLVED` |
| `25-three-waves-one-label/` | four members across three waves, one label slot | carries exactly one `wave:` label — the **current feature's** — and swaps rather than adds | `ONE-LABEL-CURRENT-FEATURE` |
| `26-backwards-step-is-correct/` | the current feature finishes; the next sits in an **earlier** wave | steps the label `design` → `discuss` and explains why in the block; the monotonic "fix" reintroduces accumulation | `BACKWARDS-STEP-EXPLAINED` |
| `27-story-no-routing-row/` | this repo's own story — both members past DISCUSS, on a path the table has no row for | emits no routing line **and says the table does not cover it**; never names a command for the story | `NO-ROUTING-ROW-STATED` |
| `28-two-in-flight-both-visible/` | two members `in progress` at once — a defect in the card | renders both `▶` rows with `⚠ also in flight`, rather than hiding or refusing the defect | `TWO-IN-FLIGHT-VISIBLE` |
| `29-current-feature-not-first-in-flight/` | `01 to do · 02 in progress · 03 in progress` — the **discriminating** roster | takes the current feature from the owner (01), not from a local "first in-flight" rule (02); 28's roster makes both answer the same and so pins neither | `CURRENT-FEATURE-FROM-OWNER` |
| `30-composed-description-under-standard/` | a slice brief with enumerable facts and **no candidate text** — the block must compose the description | composes against `rules/writing.md`: every fact present, no expletive construction, no nominalisation, active voice. **No word count is asserted** | `PROSE-STANDARD-APPLIED` |
| `31-derived-cells-not-edited/` | one block holding all three kinds of text — composed, rendered, and a `Notes` sentence this skill writes itself | applies the standard to what it composes, leaves rendered values byte-unchanged, and treats its own `Notes` note as composed | `DERIVED-CELLS-UNTOUCHED` |

`01` is the single walking-skeleton scenario. The **safety core** is `02`, `03`, `04`, `05`, `11`,
`12` — the bug classes that ship silently because the published artifact is indistinguishable from a
correct one: honesty stripped on the way out, missing knowledge published as known absence, a human's
escalation erased by a refresh, hand-written prose destroyed by a whole-body write, artifacts
corrupted from the forge, and a status computed here instead of asked for.

Fixture `08` **inverted on 2026-08-14 and is worth reading as a pair with its own history.** It used to
carry the suite's worst failure: slices 01 and 02 done, slice 03 positionally next and marked deferred, and
a card for it would not misinform someone — it would assign them. There are no slice cards now, so the
danger is gone and the *opposite* defect appears: omitting the row erases a slice that existed, was
considered, and was set aside. The rule reversed because its mechanism did, which is the shape every
inverted fixture here takes.

Fixtures `13` and `14` belong with `08` rather than with the reporting fixtures, whatever their
numbering suggests. Position is an instruction to whoever reads the column next. An order nobody
wrote issues that instruction without anyone having decided it, and a provisional order issues it a
wave before anyone can.

Fixture `15` is the reporting counterpart to `08`. Both offer a number or a position that is
defensible on the day it is written and becomes an instruction nobody rechecks. A hand-ticked
checkbox is the roster equivalent of a card for deferred work: correct once, authoritative forever.

Fixtures `03` and `04` pin the two directions in which this skill can lie about *why* a status is what
it is. `03` is the machine having nothing to say. `04` is a person having said something the machine
cannot represent. Collapsing either into a derived value is a gate failure, because both are claims
about the evidence, not about the work.

## Layout

Each fixture is self-contained and manifest-driven — no sample repository is checked out and no forge
is contacted. The `manifest.json` describes the situation: the local artifacts, the existing forge
state, the invocation, and the `expected_outcome`. Some fixtures carry a payload key beside those —
`owner_returns` for what `phil:nwave-slice-status` hands over (23, 24, 29, 31), `cards` for existing
forge items (24), and `artifacts.<path>.enumerable_facts` for the facts a composed description must
cover (30, 31). **A fixture never supplies candidate prose to choose between**: selecting the shorter
of two given strings is not composing, and a suite that tested selection would be satisfied by the very
word ceiling the skill refuses. The `expected.md` states the decision the skill
must produce, the guard that produces it, the checkable assertions, and the gate-failure condition
that blocks the skill change.

Forge state is described, not created. A fixture asserting "removes the old wave label" is satisfied
by a command that would do so — no fixture requires a live GitLab or GitHub.

## How to drive it

For each fixture, run `skills/nwave-issue-board/SKILL.md` against the situation in `manifest.json`,
and compare the intended forge writes and rendered block against `expected.md`. Any fixture that
produces the wrong outcome is a gate failure — **block the skill change**.

Three assertions apply to every fixture and are not repeated in each file:

1. **Nothing under `docs/feature/` is written.** The projection is one-way.
2. **No status is derived here.** The value published is the one `phil:nwave-slice-status` returns.
3. **Every forge command names its target** with `-R`, per `phil:issue-board`.

Any fixture that violates one is a gate failure regardless of whether its table is correct.

## Fixtures 30 and 31 — the prose standard, added 2026-09-04

Added with the prose-standard section (issue #40, feature `board-prose-standard`, slice 01). They pin the
gap that *Generate into a delimited block* leaves open: the bound is stated as a **purpose** — the
thirty-second read — and enforced as a **count**, so nothing in the skill detects a padded row.

**They exist to kill three degenerate mechanisms, and each dies on a named assertion:**

| Mechanism | Dies on |
|---|---|
| Publish the shorter of two candidates | **30** — no candidate text is supplied, so it composes nothing and fails fact coverage |
| Leave every sentence alone | **30** assertions 3-5, and **31** assertion 5 |
| Run a pass over the whole block | **31** assertions 1-3, 6 and 7 — rendered values become a second author |

Only the scope boundary the skill states passes all three: **where this skill composes the words the
standard applies; where it renders words another owner composed, they pass through untouched.**

**The discriminator is who composed the words, never which column they sit in.** Fixture 31 makes that
concrete with `Notes`: row 03's note came from the owner and is rendered intact, while the note recording
that a hand-set state was replaced is composed *here* and is therefore in scope. An earlier draft of this
fixture exempted `Notes` wholesale and was wrong.

**Neither fixture asserts a word count**, because the standard is eleven principles of composition and concision is one.
A count would pin that one and license the other ten to fail. **The stated cost:** these two are the only
things pinning the section, which is why they must test composition rather than length.
