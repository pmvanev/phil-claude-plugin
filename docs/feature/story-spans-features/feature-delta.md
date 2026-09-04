# Feature Delta — story-spans-features

Forge: issue #36 · Wave: DISCUSS ✓ (2026-09-04)
Story: the-boards-unit-of-work · position 02

> **Line references in this document are as of DISCUSS, 2026-09-04, and several have since moved** —
> slices 02-04 edited the files they point into. Where a citation matters the quoted text is given
> verbatim beside it; trust the quote, not the number. Recorded rather than rewritten: this is a dated
> record of what the skills said when the decisions were taken, and renumbering it would make it a
> record of something else.
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed — stated rather than implied)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is prose across five skills and two commands, and this repo settled twice that skills are
authored rather than waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path the predecessor took.

**This feature amends `docs/feature/single-issue-per-feature/`, which is shipped and self-tested.** It is
not a fold-back. Route 3 per `CLAUDE.md` *Where a finding about a standard goes* — the work exceeds a
paragraph, and the motivating finding is a scope correction on that feature's central claim, recorded as
[D2] below. Nothing under that directory is edited; every amendment is quoted verbatim under *Changed
Assumptions*, per the back-propagation contract.

---

## Wave: DISCUSS / [REF] Persona ID

**`morgan-feature-owner`, EXTENDED — not a new persona.** Registered at
`docs/product/personas/morgan-feature-owner.yaml`; extended 2026-09-04 with the story-tier goals,
frustrations and vocabulary.

**The owner of a story is the same developer who builds its features.** Not a planning role, not a
programme manager. Morgan already *"owns a whole feature end-to-end"*; this feature widens the unit of
ownership rather than introducing a second owner above it. A new persona would have asserted a second
reader of the same card, and a second reader is exactly the thing that would justify a second
authority — which C1 forbids.

**The rejected alternative is instructive and is the one the house pattern would have picked.** The
predecessor created `morgan-feature-owner` rather than extending Kai or Robin, because the *role* was
genuinely different. Here the role is identical and only the *scope* moved, so the same reasoning that
produced a new file then produces an extension now. Rules do not have preferred outcomes.

## Wave: DISCUSS / [REF] JTBD one-liner

**`make-in-flight-work-transferable`, EXTENDED — not a new job.** A second job statement over a
validated job is the duplicate-authority defect this repo has already recorded, and it is the same
defect the design itself is built against, one register up.

The job story is unchanged. Its `functional` dimension said *"One issue per feature"*; the story tier
generalises that to *one issue per unit of ownership*, and forces (D) and (E) both re-fire at the new
scale. Extended in `docs/product/jobs.yaml` with a dated *Story tier facet*, plus constraints C8-C10.
`keep-a-backlog-trustworthy` gains a second dated paradigm facet, because grooming's oracle changes
again and leaving that unrecorded is the SSOT drift this repo's standing check exists to catch.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **cross-cutting**. Five skills, two commands, one convention, and an amendment
  to a shipped feature's central claim. (Given)
- **[D2]** **A card MAY span several nWave features. The card's unit is the UNIT OF OWNERSHIP, not the
  feature.** This reverses the 1:1 mapping at `nwave-issue-board/SKILL.md:30`, and the correction has the
  same shape as the one that produced it: *"the feature is what somebody owns"* is true of a developer
  working one feature, and false of a developer carrying a multi-feature effort. **The predecessor's own
  [D2] refuted "nWave is worked one feature at a time" as a property of a developer rather than a repo;
  this one refutes "a feature is the whole of what somebody owns" the same way.** (User, recorded on
  issue #36)
- **[D3]** **The unit above a feature is a STORY.** Chosen over *initiative* and over *epic*. **Epic is
  rejected on a mechanism, not on taste:** GitLab sells a Premium, group-scoped feature by that name, and
  this design must work on Free — the predecessor's out-of-scope says so verbatim. A word that names a
  paid mechanism the design deliberately does not use is a standing invitation to reach for it. (User)
- **[D4]** **Persona and job are extended, never added.** See above. (Given)
- **[D5]** **Story and goal coexist, and the discriminator is what each can HOLD.** A goal is a
  milestone: it holds *cards*, has a due date, holds unrelated work by design, and survives new cards
  arriving. A story is a card: it holds *feature directories*, has no due date, and can never hold
  another card. One sentence a reader can apply on sight — **if it can hold a card it is a goal; if it
  can only hold a feature directory it is a story.** A second, positional test: looking at a *list of
  issues* is looking at a goal; looking *inside one issue* is looking at a story.
- **[D6]** **The block renders exactly ONE expanded path, and every sibling is a row with a link.** The
  feature roster, then the current feature's slice roster, then — only where `roadmap.json` exists — the
  current slice's step table. **No slice roster for any feature but the current one; no step table for any
  slice but the current one.** This is the predecessor's [D9] bound lifted one level, and the argument
  inverts identically: N features × M slices in one description is the hundreds-of-cards problem in its
  third costume.
- **[D7]** **"Slices demoted a level" means moved to a second table, never indented as sub-rows.** An
  indented tree in one table renders every slice of every feature and is the unreadable wall wearing a
  flat costume. Named because it is the tempting reading of the card's own question 1.
- **[D8]** **A story-level state is a fold ACROSS features, and `phil:nwave-slice-status` owns that
  derivation.** Not folded in the mapping skill. **This is not a judgement call — it is that skill's
  documented recurring defect**, committed on 2026-08-14 and reverted the same day
  (`nwave-issue-board/SKILL.md:156-161`). The fold ships as `--story-state`.
- **[D9]** **Story membership is declared per-feature, in that feature's own delta header:**
  `Story: <slug> · position NN`. Discovered by scanning `docs/feature/*/feature-delta.md`. No new file,
  no forge read-back, one authority per fact — a feature declares which story it belongs to and nothing
  else declares it for that feature. **The declaration and the block both carry the slug, never a prose
  title.** A human-readable name would need somewhere to live, and the only candidate is a story file —
  which is the alternative this decision rejected. The issue *title* is that name, and it is human prose
  outside the markers, where it already belongs.
- **[D10]** **The wave label stays single-valued and carries the CURRENT feature's wave.** Multi-valuing
  it would resurrect the exact failure `nwave-issue-board/SKILL.md:127-130` records: four accumulated wave
  labels and an unreadable record, with every command reporting success. **Consequence, stated because it
  reads as a bug: the wave label on a story card is NOT monotonic.** It steps backwards — DELIVER to
  DISCUSS — when the next feature begins, and that is correct.
- **[D11]** **The routing line names the command AND the feature it applies to:**
  `Work this with: /nw-design · feature <id>`. **A story has no owning command**, and a bare command on a
  multi-feature card asserts one. The three shipped routing rules survive untouched — the wave label is
  still the source, no label still means no line, and no row still means no line with the reason stated.
- **[D12]** **Two features in flight at once on one story card is a DEFECT, not a shape — and it is
  grooming's new check.** Derived rather than invented: `issue-board/SKILL.md:616-625` says two halves
  belong in different cards only when two people work them at once, and reads its own split clause as
  being about concurrency. A story worked sequentially by one owner is one card; a story with two
  features genuinely in parallel has already failed that rule.
- **[D13]** **A story card is never flagged oversized and never proposed for splitting on size.** The
  oscillation hazard at `groom-issues/SKILL.md:283-289` transfers verbatim one level up: the family stores
  no marker, so a declined split returns every run and only has to be accepted once. **The discriminator
  stays demonstrability, and the new check is [D12]'s concurrency signal, which is a different oracle
  reaching a different verdict.**
- **[D14]** **Walking-skeleton subject: the story over `single-issue-per-feature` + `story-spans-features`,
  hosted on this feature's own card (#36).** Self-hosting, per the predecessor's [D12]. It is a real story
  — the two features are the feature tier and the story tier of one effort — and its two members carry
  *different states and different waves*, which is exactly the hard case [D10] and the fold must survive.
- **[D15]** **Glanceability stays a measured KPI at the new depth.** The predecessor measured a
  thirty-second read of one roster. This feature adds a second roster above it, so the number is
  re-measured rather than assumed to survive. KPI-1, slice 01's oracle.

## Wave: DISCUSS / [REF] Domain examples

Real feature ids, real states, real waves. The first is the owner's own example from issue #36.

### 1. Happy path — *add chat to web UI and extension*, four features

A story built from four independent nWave features: `aws-bedrock-setup` (`✓ done`, post-DELIVER),
`chat-in-web-ui` (`▶ in progress`, DESIGN), `saved-sessions` (`· to do`, DISCUSS), `chat-ui-in-extension`
(`· to do`, no wave yet). One card. The block renders **four feature rows** plus
`chat-in-web-ui`'s own slice roster, and nothing else. The wave label reads `wave: design`; the routing
line reads `Work this with: /nw-design · feature chat-in-web-ui`. The fold answers `in progress`, so the
card sits in In Progress.

### 2. Mixed states and a backwards label — *the board's unit of work*, two features

Slice 01's subject. `single-issue-per-feature` (`✓ done`, past DISCUSS and authored with `plugin-dev`) +
`story-spans-features` (`▶ in progress`, DISCUSS). The fold names the second one current, so the card
reads `wave: discuss` and `Work this with: /nw-discuss · feature story-spans-features`.

**The non-monotonicity is real here but was not observed live, and the difference matters.** Position 01
finished past DISCUSS on a build path the routing table has no row for — the predecessor's slice 01
finding 1 — so it carried no routing line. Position 02 sits *at* DISCUSS, which does have a row. The
label therefore moves from *no line* to `/nw-discuss`, and in wave order that is **backwards**. Nobody
watched it happen, because 01 was already done when the card was built: this is a reconstruction from two
recorded states, not a measurement, and slice 04 says so rather than claiming a live observation.

### 3. Error / defect — two features in flight at once

The chat story with two developers: `chat-in-web-ui` and `chat-ui-in-extension` both `in progress`, both
rendering `▶`. **This is a defect, not a shape** ([D12]). `/phil:groom-issues` reports it, quoting both
feature names; the wave label takes the first in roster order and the roster's Notes column carries `⚠
also in flight` on the second. The card should become two feature cards under a goal.

### 4. Boundary — a feature that declares no story

`aws-bedrock-setup` extracted and worked on its own, with no `Story:` line in its delta. **It stays a
feature card, unchanged, with the shipped block.** Nothing about the single-feature path moves; the story
tier is reachable only by declaring membership. This is what [D2]'s *MAY* buys, and it is the reason no
existing fixture should need rewriting.

## Wave: DISCUSS / [REF] The failure is silent in three directions at once

Issue #36's own framing, and it is why this is a feature rather than a note. A multi-feature card today
is **malformed everywhere and flagged nowhere**:

| Surface | What it does with a multi-feature card |
|---|---|
| `/phil:groom-issues` | Reports it **clean** — it is demonstrable, so the oversized rule correctly passes it |
| `/phil:rank-issues` | **Stops the session** (`SKILL.md:47-50`) — the card is not one feature |
| The block generator | **Cannot render it** — `nwave-issue-board:247` allows exactly two tables, and there is nowhere to put N rosters |
| `nwave-slice-status` | **Has no fold across features** (`SKILL.md:173-221`), so the card has no derivable column |

Three of the four fail loudly at the moment of use and the fourth — the one whose whole job is noticing
what a board gets wrong — reports success. **A shape that one tool refuses and another certifies is worse
than one both refuse**, because the certification is the record people read.

## Wave: DISCUSS / [REF] Resolved before authoring

- **The two positions the reader needs.** The owner's framing: help the developer see (a) where they are
  in the **current nWave feature**, and (b) where the current feature sits in the **overall story**.
  Today only (a) exists. [D6]'s two tables are these two positions and nothing else — the layout is
  derived from the requirement rather than chosen and justified afterwards.
- **The fold is the feature fold with its input type changed.** `nwave-slice-status`'s feature-level fold
  (`SKILL.md:181-189`) tests over slices; the story fold tests the identical predicates over features,
  with `current` reading as `in progress` and `next` dropped — features have no `next`. **Because it is
  the same fold, it inherits the empty-roster guard for free**, and that guard is the costliest cell in
  the table: an unguarded fold answers `done` over an empty roster, `done` maps to the Done column, and
  auto-close turns the rendering into a closed issue. At story scale that closes a card holding N
  features. Fixtures 14 and 15's lesson transfers and must be re-pinned, not assumed.
- **Two glyph vocabularies now render in one block, and they are not the same set.** The slice table
  renders seven step statuses; the feature table renders the fold's **six** — `blocked · done ·
  in progress · deferred · unknown · to do`, with no `next`. `in progress` has no glyph today. The
  property `nwave-issue-board/SKILL.md:106-109` protects — *every value the owner can return has a
  glyph* — now has to hold over two vocabularies, and a value with no glyph gets downgraded to `·`, which
  is the unknown-published-as-not-started defect at feature scale.
- **The one-way rule is preserved, not stretched.** Membership is declared in `docs/feature/`, so
  rendering a story roster reads artifacts and writes a forge. Nothing is read back. The alternative that
  would have broken it — the story's membership living in the issue body — is recorded as rejected under
  *Alternatives considered*.
- **`issue-board`'s concurrency clause is reused, not amended.** The rule that licenses a story card is
  the same rule that limits it ([D12]). That is worth stating because it means the new shape needs no new
  granularity rule — it needs the existing one read at a new scale.

## Wave: DISCUSS / [REF] Open (→ authoring)

- ~~**Is #26 open?**~~ **RESOLVED 2026-09-04 by probing the board: #26 is CLOSED** (closedAt
  2026-08-14T21:42:28Z, milestone `null`). So [D14]'s skeleton creates **no transient duplicate** — the
  story card on #36 declares a member whose own card is already closed, and grooming only reads open
  cards. The closed card stands as the record of how that work went, which is the predecessor's own slice
  01 finding 4 applied rather than merely cited. **Removed from Pre-requisites; the risk it named does
  not exist.**
- **Where does the membership declaration get validated?** Nothing writes deltas mechanically in this
  repo, so `Story: <slug> · position NN` is hand-authored and nothing checks it until slice 05's grooming
  class fires. `scripts/check-invariants.py` is the natural home for a probe — a declared story slug with
  no card, a position collision, a member directory that does not exist — and adding one is route 2 per
  `CLAUDE.md`. **Recorded as a candidate, not committed**, because it is a script and this feature's
  deliverable is prose.
- **GitLab rendering is still unverified**, inherited verbatim from the predecessor. Two stacked tables
  render as tables in both forges' web UIs — the mechanism the hard constraints name — but the *read* has
  only ever been measured on GitHub. KPI-1 is measured on the wrong forge again, and says so.
- **Can a story span features in more than one repository?** Out of scope below, but the question is not
  absurd — a plugin and its consumer are two repos. Left open rather than answered, because nothing in
  the artifacts crosses a repo boundary today and inventing a cross-repo membership syntax with no
  demand is speculative design.

## Wave: DISCUSS / [REF] Scope assessment

**OVERSIZED** — two signals fire; two is the threshold this repo set on 2026-08-14.

| Signal | Reading |
|---|---|
| >3 modules | **5** — `nwave-issue-board`, `nwave-slice-status`, `issue-board`, `groom-issues` (+`groom-set`), `rank-issues` |
| Multiple independently shippable outcomes | **3** — the story tier in the block, the fold across features, the grooming/ranking adaptation |
| Estimated effort | ~5 days, under the 2-week signal — does **not** fire |
| >10 stories | 6 — does **not** fire |

Split into **five** slices. Taste tests are per slice, in a table at the foot of each brief.

**This feature is the first candidate for its own mechanism, and declining that is deliberate.** Five
surfaces and three outcomes would cut cleanly into two or three features under a story — which is exactly
what the feature proposes. **Refused because the mechanism does not exist yet**, and building the first
story out of the work that builds stories makes every slice's failure ambiguous between the design and
its first use. The self-hosting that *is* taken is [D14]'s, which renders a story card over two features
without decomposing this one.

## Wave: DISCUSS / [REF] Story map — backbone

Morgan's activities, left to right in the order they occur. **A1-A7 are the predecessor's backbone and
are unchanged** — this feature changes what a card *is*, not what Morgan does with one. Two activities
gain a second half, and they are the two the owner named:

| # | Activity | What changes at the story tier |
|---|---|---|
| A1 | **Find the work** | One card per story instead of per feature; the wave label now moves backwards (D10) |
| A2 | **Understand a feature's state** | **Gains a second position** — where the current feature sits in the story (D6) |
| A3 | **Take it on** | The routing line names a feature as well as a command (D11) |
| A4 | **Work it** | Unchanged — served by shipped work, as it was |
| A5 | **Handle a diversion** | Unchanged — the stack is the developer's, so a story card carries exactly one |
| A6 | **Put it down** | Unchanged; the refresh regenerates a deeper block |
| A7 | **Keep the board honest** | **Gains a new defect class and loses none** (D12, D13) |

Slices against activities:

| Slice | Activities it serves |
|---|---|
| 01 One story as one card (walking skeleton) | **A2** — both halves, measured |
| 02 The fold across features | **A1** — the column is how the work is found |
| 03 The mapping becomes normative | A2, A3 — the layout and the refusal list become rules |
| 04 The wave label under mixed waves | A1, A3 — the label and the routing line |
| 05 Grooming and ranking recognise the story | **A7** |

**A5 is the activity that did NOT change, and saying so is the point.** A diversion stack belongs to a
person, not to a unit of work, so a story card carries one stack and not one per feature. A backbone
activity that survives a paradigm change unaltered has to be named as surviving, or the next reader
invents a per-feature stack to fill the gap.

## Wave: DISCUSS / [REF] Slices and order

Ordered by **learning leverage** — riskiest assumption first, so a failure costs least.

| # | Slice | Disproves if it fails |
|---|---|---|
| 01 | One real story as one card (walking skeleton) | That two stacked rosters read in seconds at all — the whole premise |
| 02 | The fold across features lands with its owner | That derivation-stays-with-its-owner (C5) survives a fold whose input is a set of features |
| 03 | The mapping becomes normative | That the bound holds as a written rule rather than as one careful hand-build |
| 04 | The wave label under mixed waves | That one single-valued label can serve a multi-wave card |
| 05 | Grooming and ranking recognise the story | That the shipped oracles need only extension, not loosening |

Briefs at `docs/feature/story-spans-features/slices/slice-NN-*.md`.

**Order: slice number — final; `/nw-roadmap` does not run in this repo.** Written in that form rather
than as `provisional until /nw-roadmap`, per `nwave-issue-board/SKILL.md:210-213`, because a promise of a
correction that will never arrive misinforms every future reader.

No standalone SSOT or convention slice. The membership declaration [D9] lands inside slice 02, which is
the first slice that cannot work without it.

**Three briefs exceed the ≤100-line guideline, and say so here rather than being trimmed into
inaccuracy** — slice 01 at 108, slice 02 at 106, slice 05 at 102, against slice 03 at 92 and slice 04 at
95. Each carries the carpaccio taste-test table the wave mandates *on top of* a standard brief; that
table is 8 lines, so excluding it every brief is at or under 100. Same accounting the predecessor gave
for its two overlong briefs.

**Peer review flagged this as its only finding, and it is being declared rather than fixed.** Slices 01
and 02 grew *after* the review, and every line added was a correction that the review's own standard
demands: the probed state of #26, the milestone KPI-5 needs and did not have, the back-propagation slice
02 performs on the predecessor's delta, and a dogfood claim in slice 04 corrected from a live observation
to a reconstruction. **Trimming to hit 100 would remove the accuracy the count was proxying for**, which
is the guideline eating its own purpose. The trim the reviewer suggested — condensing the taste-test
tables — targets the one section the wave mandates verbatim.

## Wave: DISCUSS / [REF] WS strategy

**C — real local resources.** Slice 01 writes a real block to the real board (`pmvanev/phil-claude-plugin`,
user project 3) rather than to a faked forge adapter, for the reason the predecessor gave: the whole
uncertainty is *how a rendered page reads to a human in seconds*, and a faked adapter answers a question
nobody asked.

The cost is a real card, mitigated by [D14] — the subject is this feature's own card plus a completed
predecessor, so nothing in flight is disturbed.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Change |
|---|---|---|
| `phil:nwave-issue-board` | Skill (knowledge-only) | Mapping gains the story tier; the two-table layout and its refusal list; the second glyph vocabulary; the wave-label and routing rules |
| `/phil:nwave-slice-status` | Command + skill | Gains `--story-state`, the fold across features, and membership discovery |
| `phil:issue-board` | Skill (knowledge-only) | *Choosing what becomes an issue* gains the story tier; the milestone-is-a-goal statement gains the story discriminator |
| `/phil:groom-issues`, `/phil:groom-set` | Commands | New set-level class; the oversized protection extended; the ungrouped-effort supersession extended |
| `/phil:rank-issues` | Command | The ranked unit becomes the card — a feature **or** a story |

No new command. Every surface is an existing one, which is why [D4]'s extensions are the honest record
rather than a new job standing alone.

## Wave: DISCUSS / [REF] Journey

Full journey at `docs/product/journeys/story-spans-features.yaml`. The predecessor's journey
(`journeys/single-issue-per-feature.yaml`) is scoped to feature cards and gains one dated comment
pointing here; its steps are otherwise untouched.

Morgan opens a story card and, above the prose, reads a generated block: the story's name and feature
count, the wave of the feature currently in flight, a routing line naming both the command and the
feature it applies to, then two tables — the feature roster with its own state glyphs, and the current
feature's slice roster. Nothing else is enumerated; every sibling links. Morgan names both positions
inside thirty seconds, and can say without being told which grouping is the story and which is the goal
the card sits under.

Arc: `uncertain → oriented (story) → oriented (feature) → committed → trust` (upward).

**The two `oriented` beats are distinct, and the order is story-first on purpose.** The half that does
not exist today is the one that reframes the half that does — knowing the current feature is one of four
changes what *"where am I"* means. Rendering the feature position first and the story position beneath it
reads as an appendix, which is the layout failure this arc is the test for.

**The accepted cost, recorded in the journey's error paths:** the block shows one expanded path, so a
reader who wants a non-current feature's slices opens its brief. That is a click the single-feature card
did not cost. Accepted because the alternative is the wall, and stated so it is not rediscovered as a
defect.

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: make-in-flight-work-transferable` unless marked otherwise.

### S1 — Read both positions from one card

As Morgan, I open a story card and know both where the current feature stands and where that feature
sits in the whole story.

#### Elevator Pitch — S1

Before: the card tells me where I am in *a* feature, and nothing tells me where that feature sits in the
larger effort — that grouping exists only in someone's head, or in a milestone that also holds unrelated
work.
After: open the story issue in the forge → sees a delimited block with
`Story: the-boards-unit-of-work · 2 features`, a feature roster carrying a state glyph and a two-line
description per feature, and below it the current feature's slice roster, above a generation timestamp.
Decision enabled: whether to pick this story up, and if so which feature inside it is the live one.

AC1 — The block renders the feature roster, the current feature's slice roster, and a timestamp; a
reader unfamiliar with the story names both positions within 30 seconds (KPI-1).
AC2 — No feature but the current one has its slices enumerated, and no slice but the current one has its
steps enumerated ([D6]). Siblings appear as rows with links.
AC3 — The feature roster is a flat table of features. Slices never appear as indented sub-rows ([D7]).
AC4 — Feature-state glyphs cover all six values the fold can return; a value with no glyph is a gate
failure, never a `·`.

### S2 — Know which command to run when the features are in different waves

As Morgan, I read a story card whose features sit in three waves and still know exactly what to run next
and against what.

#### Elevator Pitch — S2

Before: the wave label answers for one feature and the card holds several, so either the label lies or
the card carries four labels and the record becomes unreadable.
After: open the story issue → sees one wave label naming the wave of the feature in flight, and
`Work this with: /nw-design · feature payment-capture` — a command and the feature it applies to.
Decision enabled: which command to run, against which feature, without opening the repo to find out.

AC1 — The wave label is single-valued and equals the current feature's wave ([D10]).
AC2 — The routing line names a feature as well as a command; no line ever names a command for the story
([D11]).
AC3 — A wave label that steps backwards when the next feature begins is correct, and the block says so
rather than leaving a reader to read it as an error.
AC4 — Where the current feature's wave has no row in the routing table — this repo's own build path —
no line is emitted and the block states that the table does not cover it, per the shipped rule.

### S3 — Place a story card in a column without inventing its state

As Morgan, I put a story card in the right column, and the state comes from the same skill that already
owns every other derivation over these files.

#### Elevator Pitch — S3

Before: no story-level state exists, so a publisher placing a story card either folds one locally — the
mapping skill's documented recurring defect — or guesses.
After: run `/phil:nwave-slice-status --story-state the-boards-unit-of-work` → sees
`Story: the-boards-unit-of-work — in progress · 1 of 2 features done · current feature story-spans-features`.
Decision enabled: which column the card belongs in, and whether this story is what to pick up next.

AC1 — The fold lives in `phil:nwave-slice-status`; `phil:nwave-issue-board` consumes and renders it and
never computes it ([D8]).
AC2 — Over an empty roster the fold returns `unknown`, never `done`. A story whose features are all
`unknown` leaves the card's column untouched rather than being coerced into one the board offers.
AC3 — The state line carries a count beside it, and the empty-roster case carries no count — `0 of 0
done` reads as completion.
AC4 — Membership is read from each feature's own delta header ([D9]); nothing is read back from the
forge.

### S4 — Groom a board of story cards without false positives, and catch the real defect `@infrastructure`-adjacent

As Robin, I run grooming against story cards: every correctly-shaped one passes, and the one genuinely
wrong shape is reported. `job_id: keep-a-backlog-trustworthy` (paradigm facet).

#### Elevator Pitch — S4

Before: a story card is large, holds several demonstrable things, and passes the demonstrability rule —
so grooming reports it clean whether it is correct or not, including when two people are working two of
its features at once.
After: run `/phil:groom-issues` → sees zero findings against a correctly-shaped story card, and a
reported *two features in flight* finding against one whose block shows two `▶` rows.
Decision enabled: whether this story should stay one card or become N feature cards under a goal.

AC1 — A correctly-shaped story card produces no oversized finding and no split proposal, verified
without loosening the rule's text ([D13]).
AC2 — A story card whose fold shows two features in progress is reported, with the two feature names as
quoted evidence ([D12]).
AC3 — Several open cards that are *features of one story* are reported as a set, and the offered
resolution is a story card — never a milestone, which is a goal ([D5]).
AC4 — The two checks resolve opposite ways on adjacent inputs, in the style of fixtures 04/11: getting
one right by a rule that gets the other wrong is a gate failure.

### S5 — Rank a board whose unit may be a story

As Robin, I rank a board holding both feature cards and story cards, and the session neither stops
wrongly nor ranks a unit that is going away. `job_id: keep-a-backlog-trustworthy`.

#### Elevator Pitch — S5

Before: the ranked unit is the feature card, so a story card is either stopped on as unrecognised or
ranked as if it were a feature, and its member features could each take a position too.
After: run `/phil:rank-issues` → sees one position per card, where a card is a feature **or** a story,
and its member features hold none.
Decision enabled: which unit of work to start next, over a board with both shapes on it.

AC1 — The ranked unit is the card; a card is one feature or one story; a slice is never a card.
AC2 — The stop condition narrows to slice cards. A story card does not stop the session.
AC3 — Where a story card and a member-feature card are both open, the session says so and stops, naming
`/phil:groom-set` as what comes first — reusing grooming's oracle rather than duplicating it.

### S6 — Tell a story from a goal on sight

As Morgan, I look at one card and one milestone and can say which grouping each is, without being told.

#### Elevator Pitch — S6

Before: two groupings would arrive on one board with no stated discriminator, and *"which of these is
the thing that holds the other?"* is answered differently by each reader.
After: read the card and its milestone → sees the story as a table of feature directories inside one
issue, and the goal as a milestone holding a list of issues with a due date.
Decision enabled: whether to open the card or the milestone's issue list to find the work being looked
for.

AC1 — A reader shown one story card and one milestone names which is which, first time, no prompt
(KPI-5).
AC2 — The discriminator is stated where a reader meets it: `phil:issue-board`'s milestone-is-a-goal
statement, and `groom-issues`'s ungrouped-effort class.
AC3 — Grooming never offers a milestone where the right container is a story card, and never the
reverse.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Measurement |
|---|---|---|---|
| KPI-1 | Time to comprehension — **both** positions | ≤ **30 s** to name the current feature's position **and** where it sits in the story | Owner's timed read of the slice 01 card. Baseline: the second half is unavailable at any time cost today |
| KPI-2 | Cards and positions per story | Exactly **1** card and **1** rank position (from N of each) | Board read plus a `/phil:rank-issues` dry pass |
| KPI-3 | Rows rendered vs rows that exist | Rendered ≤ features + current feature's slices + current slice's steps — **never the product**. ≤ **12** rows on slice 01's card | Count on the rendered card |
| KPI-4 | Grooming: false positives **and** true positives | **0** correct story cards flagged; **1 of 1** two-in-flight cards flagged | A scan against a correct card and against a deliberately wrong one |
| KPI-5 | Story/goal confusion | **0** misidentifications, n=1, honestly labelled | Slice 01's reader is asked which grouping is which, unprompted — **requires a milestone in view; #36 has none today** |

**KPI-4 is deliberately two-sided, and that is the correction the predecessor's KPI set needed.** Its
KPI-4 counted false positives only, which a rule loosened to silence would score perfectly — the exact
hazard the `keep-a-backlog-trustworthy` facet records as anxiety (F): *"An oracle loosened to stop the
false positives stops catching the real ones."* A one-sided measure cannot see that failure.

**KPI-1 is scoped to this slice set, not borrowed from the feature.** The predecessor's slice 01 finding
7 is the lesson: a measure written for the feature over-claims against the slice carrying part of it, and
fails silently because the slice looks like it missed. KPI-1 names the two facts this feature actually
delivers and excludes *why work stopped*, which the predecessor's slice 04 owns and this feature does not
touch.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `morgan-feature-owner`, **extended** not added; the reason the house pattern was not followed is stated in *Persona ID* |
| 2 | Job traceability | ✓ | Every story carries a `job_id`; `make-in-flight-work-transferable` extended, `keep-a-backlog-trustworthy` gains a second facet |
| 3 | Journey mapped | ✓ | `journeys/story-spans-features.yaml`, arc upward, error paths including [D6]'s accepted cost |
| 4 | Stories with elevator pitches | ✓ | S1-S6, each naming a real invocable entry point (the forge page, `/phil:nwave-slice-status`, `/phil:groom-issues`, `/phil:rank-issues`) |
| 5 | ACs testable | ✓ | Each AC names an observable; KPI-1, KPI-3 and KPI-5 supply numbers for the three that would otherwise be vibes |
| 6 | Scope assessed | ✓ | OVERSIZED on two signals; five slices; the self-decomposition refusal stated rather than skipped |
| 7 | Slice briefs exist | ✓ | Five briefs under `slices/`, each ≤100 lines with a learning hypothesis, IN/OUT scope, a dogfood moment and a taste-test table |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..5, each with a target and a method; KPI-4 two-sided by construction |
| 9 | Out-of-scope explicit | ✓ | Below |
| 10 | 3+ domain examples with real data | ✓ | Four, under *Domain examples* — happy path, mixed states, the defect case, and the boundary. Real feature ids from issue #36, not `feature-a` |

**Item 10 is new, and the predecessor's absence of it was a real gap.** That pass authored nine items
because no canonical list is recorded in this repo; the DISCUSS wave's own list carries a
concrete-examples item, and the predecessor's delta reasoned entirely in the abstract about a
`22-phase feature` that does not exist. **An abstract bound is untestable** — KPI-3's number came out of
writing example 1 down, and could not have been written without it.

**Still self-graded.** Stated so a reader does not mistake a ticked table for an external gate — the
weakness `docs/evolution/2026-08-10-issue-board.md:352` names about `nw-skill-reviewer`.

## Wave: DISCUSS / [REF] Out-of-scope

- **Epics and any GitLab Premium mechanism.** Inherited verbatim and re-affirmed: Premium and
  group-scoped; the design must work on Free. [D3] rejects even the *word*.
- **A third tier above the story.** Two tiers of grouping on one board is already the confusion risk
  [D5] exists to answer; a third is not proposed and should be refused on the same grounds.
- **Cross-repository stories.** Nothing in the artifacts crosses a repo boundary today. Left open under
  *Open (→ authoring)* rather than designed for.
- **Bidirectional sync.** Unchanged. The forge remains a projection; membership is declared in
  `docs/feature/` and never read back.
- **Retiring the feature card.** A feature that declares no story is still a card, unchanged. The story
  is an option, not a replacement — which is what [D2]'s *MAY* means.
- **Per-feature diversion stacks.** A stack belongs to a person. One card, one stack.
- **Automating the membership declaration.** Hand-authored in the delta. A validator is a candidate for
  `scripts/check-invariants.py`, recorded as open, not committed.
- **Retro-consolidating closed cards.** Inherited from the predecessor's slice 01 finding 4: closed
  cards are the record of how the work went.

## Wave: DISCUSS / [WHY] Alternatives considered

Density stays `lean` + `ask-intelligent`; this is the only Tier-2 expansion rendered, its trigger
(cross-context complexity: five modules, two forges, a fold with a new input type) having fired.

**Telemetry not emitted.** The wave mandates a `DocumentationDensityEvent` via
`scripts/shared/telemetry.py`; that helper does not exist in this install. Stated rather than faked. The
two previous waves hit the same gap.

### [D6] The block's rows — four candidates

| Candidate | Why it lost |
|---|---|
| **A per-feature roster section**, stacked — each feature gets its slice table | The literal reading of "keep what ships, repeat it per feature". Lost on arithmetic: three features of six slices is eighteen rows plus three headers before the current slice's steps, against a thirty-second budget the predecessor measured at *one* roster. It is the hundreds-of-cards argument in its third costume. |
| **One table, slices indented under features** | Looks flat, reads compact. Lost because it renders every slice of every feature — the same wall with better typography — and because an indented tree in a markdown table degrades badly in both forges' web UIs, which is the surface the whole requirement is about. |
| **Features only; slices link out entirely** | Cheapest and unambiguously readable. Lost on the requirement: position (a), *where am I in the current feature*, is the half that already works today, and dropping it to make room for (b) trades one missing position for another. |
| **One expanded path: features, then the current feature's slices** ✓ | Won because it *is* the two positions the owner asked for, and because it lifts the predecessor's own bound ([D9]) one level rather than inventing a new discipline. Everything not on the path is a row with a link. |

### [D9] Where story membership lives — three candidates

| Candidate | Why it lost |
|---|---|
| **The issue body** — the story roster is typed, and the deriver reads it | Simplest to author, and the membership is visible exactly where it is used. Lost on the one-way rule: a fold over `docs/feature/` whose input came from the forge is the forge deciding what the artifacts mean. |
| **A new `docs/story/<id>.md`** | Gives the roster an explicit order and a place for the story's own goal. Lost on second-authority: a story file listing members and a feature that thinks it belongs elsewhere disagree, and nothing arbitrates. It also orphans — deleting a feature leaves a member row pointing at nothing. |
| **A per-feature declaration in the feature's own delta** ✓ | One authority per fact: the feature declares its own membership. Single-valued for free — one line, one story. Never orphans. The cost is that the roster is discovered by scanning rather than read from one place, and the *order* needs an explicit `position NN` rather than falling out of a list; both are stated rather than absorbed. |

### [D10] The wave label under mixed waves — four candidates

| Candidate | Why it lost |
|---|---|
| **Multi-valued on story cards** | Honest about all the waves at once. Lost on a shipped, measured failure: `nwave-issue-board/SKILL.md:127-130` records four accumulated wave labels making the record unreadable while every command reported success. It would also break the single-valued declaration `groom-issues` rule 4 reads. |
| **No wave label on a story card** | Refuses to approximate. Lost because it takes the board's biggest cards out of wave filtering entirely, and the block is not searchable. |
| **A `wave: mixed` value** | One new enum value, single-valued, never lies. Lost because it is uninformative precisely when the card matters most — *mixed* tells a reader to open the card, which is the cost the label exists to avoid — and it needs a routing-table row that cannot exist. |
| **Single-valued, = the current feature's wave** ✓ | Won because it preserves the single-valued family untouched, keeps the routing line derivable, and degrades only in the two-features-in-flight state, **which [D12] makes a defect grooming reports.** The approximation fails only where the card is already wrong. |

### [D14] Walking-skeleton subject — three candidates

| Candidate | Why it lost |
|---|---|
| **A synthetic story over invented features** | Disturbs nothing. Lost on the taste test the predecessor's own briefs apply: synthetic data answers a question about the format and not about the read, and the read is the whole uncertainty. |
| **Consolidating two live feature cards into a story card** | The most direct before/after. Lost on disturbing real cards, and on the predecessor's finding that closed cards are the record of how the work went. |
| **The story over `single-issue-per-feature` + this feature, hosted on #36** ✓ | Real features, real artifacts, genuinely one effort — and its members differ in both state and wave, which is exactly the case [D10] and the fold must survive. Self-hosting, per the predecessor's [D12]. |

## Wave: DISCUSS / [REF] Pre-requisites

1. **Plugin skew closed, or the version stated.** Any dogfood claim in slice 01 must name the version it
   exercised, and must say whether it drove the command or the prose.
2. **`gh auth` retains the `project` scope** — needed to read the card's Status field back.
3. **#36 assigned to a goal, for KPI-5.** #36 reads `milestone: null` (probed 2026-09-04), so the
   story/goal discrimination test would have only one of its two groupings on screen and would pass
   trivially. The board carries three open milestones — `Board and session tooling` (due 2026-09-15),
   `The plugin checks what it claims` (2026-10-15), `Sharper code review` (2026-11-15). **The first is
   this work's goal**, and assigning #36 to it makes both groupings visible on one page, which is the
   only configuration in which KPI-5 measures anything.
4. **A GitLab instance, if KPI-1 is to be measured where Morgan actually reads** — otherwise slice 01's
   evidence is GitHub-only and says so, as the predecessor's did.

**Pre-requisite 1 of the original list is discharged:** #26's state was probed rather than left open, and
it is closed. See *Open (→ authoring)*.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

A card may span several nWave features. The unit of the card is the unit of ownership: a **story** where
a feature declares membership in one, a feature otherwise. The card's generated block renders one
expanded path — a feature roster, then the current feature's slice roster, then the current slice's steps
where a roadmap exists — and refuses every sibling section. The story-level state is a fold across
features, owned by `phil:nwave-slice-status`. The wave label stays single-valued and carries the current
feature's wave, non-monotonically. A story and a goal coexist: a goal holds cards, a story holds feature
directories.

### Constraints established

C1-C7 are inherited from `make-in-flight-work-transferable` and all still bind. Three are added:

- **C8** One expanded path. The block enumerates exactly one feature's slices and one slice's steps;
  everything else is a row with a link. The bound does not multiply with the roster.
- **C9** Two grouping tiers, one discriminator, stated where a reader meets it. A goal holds cards; a
  story holds feature directories.
- **C10** A shipped oracle is extended at the new scale, never loosened. Where a new shape would pass an
  existing check vacuously, add a check that fires — do not weaken the one that passes.

### Upstream changes

Both quoted verbatim under *Changed Assumptions* rather than edited silently.

1. **`nwave-issue-board/SKILL.md:30`** — the mapping table's feature row.
2. **`nwave-issue-board/SKILL.md:247`** — *"the only tables in the block"*.
3. **`rank-issues/SKILL.md:29-32`** — the ranked unit.

**Each of issue #36's four questions is pinned by a self-test fixture**, per the card's own *Done when*.
The four land as: Q1 → the two-table bound and its refusal list (slice 03); Q2 → the story fold and its
empty-roster guard (slice 02); Q3 → the single-valued label under mixed waves plus the routing line
(slice 04); Q4 → the story/goal discriminator and grooming's container choice (slice 05). Each slice
brief names its fixtures in its acceptance criteria.

`docs/product/jobs.yaml` and `docs/product/personas/morgan-feature-owner.yaml` are **extended in place**
with dated comments saying what changed and why, per the prompt's instruction and this repo's SSOT
discipline. `docs/product/journeys/single-issue-per-feature.yaml` gains one dated scoping comment; its
steps are untouched.

---

## Changed Assumptions — amending `single-issue-per-feature`, 2026-09-04

Recorded here per the back-propagation contract. **Nothing under
`docs/feature/single-issue-per-feature/` is edited.**

### 1. "One issue = one feature" becomes "one issue = one unit of ownership"

**Original, verbatim** from that feature's delta, [D2]:

> **One issue = one feature.** Slice and step both become rows; the feature is the card.

And from `skills/nwave-issue-board/SKILL.md:30`:

> | Feature — `docs/feature/<id>/` | **One issue. This is the card that moves.** Carries the wave. |

**New assumption.** The card is the unit of ownership. Where a feature declares
`Story: <slug> · position NN`, the *story* is the card and the feature is a row; otherwise the feature is
the card, exactly as shipped. Slice and step are unchanged — still rows, never cards.

**Rationale.** The original's own justification was *"the feature is the card because the feature is what
somebody owns."* That is true of a developer working one feature and false of one carrying a
multi-feature effort — **the identical scope error the original corrected one level down**, where *"nWave
is worked one feature at a time"* turned out to describe a developer rather than a repo. A premise
correction that fixes one level and leaves the level above it unexamined will be repeated.

### 2. KPI-2 changes what it counts

**Original, verbatim:**

> | KPI-2 | Cards per feature | Exactly **1** (from 1 + N) | **MET 2026-08-14** …

**New assumption.** Cards per *story* is exactly 1. Cards per *feature* becomes **0 or 1** — zero when
the feature is a story member. The original target is still met by every feature that declares no story,
so the measurement is not invalidated, only rescoped.

### 3. The ranked unit

**Original, verbatim** from `skills/rank-issues/SKILL.md:29-31`:

> **In an nWave repo the ranked unit is the FEATURE card, not a slice.** One issue is one feature there
> (`phil:nwave-issue-board`), so a feature holds one position and its slices hold none — they are rows in
> its roster.

**New assumption.** The ranked unit is the *card*: a feature or a story. A story holds one position and
its member features hold none — the same sentence, one level up. **The stop condition is narrowed rather
than widened:** it fires on slice cards, and a story card is not one.

### 4. The oversized rule holds, and gains a sibling rather than a clause

**Original, verbatim** from `skills/groom-issues/SKILL.md:283-287`:

> **Demonstrability, not size, and the distinction is load-bearing.** A card holding a whole feature is
> large and demonstrable, so it passes — and on a board where one issue *is* one feature, it is the
> intended shape. Judging by size instead would report every correctly-formed card, and worse: it would
> propose splitting a consolidated feature back into slices every run, because this family stores no
> marker, so a declined split returns forever and only has to be accepted once. **Do not "fix" this rule
> toward size.**

**New assumption.** Every word of that stands at story scale, and the paragraph is extended rather than
edited: a story card is large, holds several demonstrable things, and passes. The defect a story card can
actually carry is **concurrency, not size** ([D12]), and it gets its own check with its own oracle. This
is C10 in its first application — **the rule that passes correctly is left alone, and the gap it leaves
is closed by a rule that fires.**

### 5. "The only tables in the block" gains a third, conditionally

**Original, verbatim** from `skills/nwave-issue-board/SKILL.md:247-250`:

> **The roster and the current slice's steps are the only tables in the block.** Header lines precede
> them: `Wave:`, the generation timestamp, `Work this with:` where the routing table has a row, and
> `Order:`.

**New assumption.** On a story card the block carries **the feature roster, the current feature's slice
roster, and — only where `roadmap.json` exists — the current slice's step table.** On a feature card the
original sentence is unchanged.

**Rationale, and it is the whole of [D6].** The rule's purpose was never a table count; it was **one
expanded path**, and the count was the shape that purpose took at one tier. Rewriting it as "three tables"
would preserve the number and lose the reason, and the next tier would then need "four". The rule is
restated as the bound it always was: *exactly one feature's slices and one slice's steps are enumerated;
every sibling is a row with a link.* At the feature tier that sentence produces the original two tables
verbatim, which is the test that the restatement is faithful.

Also amended by the same paragraph: **`SKILL.md:81`'s `no epics`** stays true and stops being load-bearing.
It records that the design removed a Premium mechanism, not that the design removed grouping — a
distinction issue #36 makes explicitly, and one the line's placement in a list of removals obscures.

### 6. What did NOT change, said out loud

The predecessor's C1-C7 all bind unchanged; `issue-board`'s concurrency clause is reused rather than
amended; A4-A6 of the backbone are untouched; and the diversion stack stays one per person rather than
one per feature. **A paradigm change that lists only its amendments invites the next reader to assume
everything else moved too.**
