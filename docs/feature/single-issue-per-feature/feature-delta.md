# Feature Delta — single-issue-per-feature

Forge: not yet carded · Wave: DISCUSS ✓ (2026-08-14)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed — stated rather than implied)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is prose across six skills, and this repo settled twice that skills are authored rather
than waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path `groom-issues` and `session-handoff` took.

**This feature inverts shipped, self-tested decisions.** It is not a fold-back. Route 3 per `CLAUDE.md`
*Where a finding about a standard goes* — the work exceeds a paragraph, and the motivating finding is a
premise correction, recorded as [D2] below.

---

## Wave: DISCUSS / [REF] Persona ID

**`morgan-feature-owner`** — Morgan owns a whole feature end-to-end on a board that other feature
owners also work from, and is both the person who hands one over and the person who inherits one.
Registered at `docs/product/personas/morgan-feature-owner.yaml`.

Distinct from the two adjacent personas, and the distinction is the reason for a new file. Kai
(`session-handoff`) hands the baton to their *own* next session — every recorded frustration is
solo-session. Robin (`groom-issues`) curates cards without working them, a boundary that persona file
draws explicitly against Quinn. Neither is the developer who picks up a colleague's half-done feature.

## Wave: DISCUSS / [REF] JTBD one-liner

When a feature Morgan owns is in flight on a shared board, Morgan wants the issue itself to carry the
whole feature — where it stands, what is next, and why work stopped where it did — so the work can be
put down at night and picked up in the morning, and a teammate can take it over without asking a
question.

Registered as a new validated job `make-in-flight-work-transferable` in `docs/product/jobs.yaml`, with
refinement facets added to `keep-a-backlog-trustworthy` and `carry-work-across-session-boundaries`.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **cross-cutting**. Six skills, two ADR-level reversals, one board
  convention. Wider than `groom-issues` (one surface plus a mapping). (Session)
- **[D2]** **One issue = one feature.** Slice and step both become rows; the feature is the card.
  This inverts `nwave-issue-board/SKILL.md:28-36`, and the motivating finding is that its stated
  rationale was **scoped wrong**: "nWave is worked one feature at a time" is a property of a
  *developer*, not of a repo. With several developers each owning a feature, every conclusion drawn
  from the single-card premise needs re-deriving. (User)
- **[D3]** **Board columns = the nWave waves, plus a generic to-do/in-progress/blocked/done family**
  for work nWave is not driving. One board. This reverses the wave-as-label-not-column decision at
  `docs/evolution/2026-08-10-issue-board.md:130-134`, whose only stated reason was the premise [D2]
  corrects. (User)
- **[D4]** **The wave remains a label as well as a column.** Redundant except in exactly one case —
  a blocked card that has left its wave column — which is the case that matters. Whether it leaves is
  open, see slice 03.
- **[D5]** **One new job plus refinement facets on both adjacent jobs.** The transferability outcome
  is owned by neither existing job, and both existing jobs genuinely change: grooming's defect oracle
  and handoff's surface. First feature in this repo to touch two jobs at once. (User)
- **[D6]** **New persona**, not an extension of Kai or Robin. (User)
- **[D7]** **The diversion stack's authority is `.session-handoff.md`; the issue carries a one-way,
  delimited, timestamped projection of it.** This is ADR-013's deferred *partitioned local + board*
  option adopted exactly as that ADR wrote it, so the amendment is small. It preserves four shipped
  rules simultaneously: the one-way projection, ADR-013's snapshot surface, *Refresh at boundaries*,
  and one-system-of-record. (User)
- **[D8]** **Per-step indicators are generated glyphs — `✓` done, `▶` current, `·` not started —
  never markdown checkboxes.** Fixture 15 forbids hand-ticked state: a checkbox is ticked by hand
  while work completes on its own, so the two diverge the first time anyone forgets, and what the
  issue displays is the state of the checkboxes rather than the state of the work.
- **[D9]** **The projection is bounded: the slice roster, plus the step table for the current slice
  only.** The "a 22-phase feature would mint hundreds of issues" argument (`:36`) inverts rather than
  disappearing — every step of every slice in one description is unreadable in a different way.
  Everything outside the current slice links to its slice file.
- **[D10]** **A feature-level state is a fold over its slices, and `phil:nwave-slice-status` owns that
  derivation.** Not folded here. Two derivations over the same files drift apart, which is the
  documented reason `nwave-issue-board` exists as a separate skill at all (`:20-21`).
- **[D11]** **`groom-issues` slice 04 lands and commits first.** Its five uncommitted fixtures (25-29)
  concern body content, which survives this change largely intact. (User)
- **[D12]** **The walking skeleton's subject is this feature's own card** — self-hosting, disturbs no
  in-flight card, and since DELIVER never runs in this repo there is no `roadmap.json`, so it also
  exercises the provisional-order path for real. (User)
- **[D13]** **Glanceability is a measured KPI, not a claim.** "Understand where we are in seconds" is
  the requirement Morgan actually stated; it is recorded with a number and a measurement method under
  *Outcome KPIs*, and it is slice 01's oracle.

## Wave: DISCUSS / [REF] Resolved before authoring

- **The premise.** Teammates are real or imminent (User, 2026-08-14). This was the load-bearing
  assumption and it had **no validated persona or job behind it** — all seven jobs and all seven
  personas in the SSOT are written for one developer working with AI agents. [D5] and [D6] close that
  gap rather than leaving the feature designed for a hypothetical team.
- **The one-way rule is preserved, not inverted.** The rule at `nwave-issue-board/SKILL.md:23-24`
  forbids writing forge content back into `docs/feature/`. Under [D7] nothing is: the stack's
  authority is a local file, the issue holds a generated projection, and the projection is never read
  back. The rule that was genuinely at risk — a broad reading in which the forge stores nothing —
  turns out not to be needed. The operative rule is **single-authority-per-fact**.
- **A roster table is now legitimate, and the ban does not transfer.** `:51-52` forbids hand-writing
  a slice roster *because the forge already computes it from sub-issues*. Once slices stop being
  issues nothing computes it, and a generated, delimited, timestamped roster is the same instrument as
  the step table that already ships.
- **Two SSOT conflicts must be reversed, not worked around.** `docs/product/journeys/groom-issues.yaml:99-102`
  currently makes session state in an issue body a **body defect**, citing ADR-013; and
  `jobs.yaml:301-303` records "session scratch published to a board is visible to everyone who reads
  the board" as validated anxiety C. Both are addressed in slice 05 and in the facets, quoted verbatim
  rather than silently edited.

## Wave: DISCUSS / [REF] Open (→ authoring)

- **Does a blocked card leave its wave column?** It must if blocked is a column, and then the board no
  longer shows which wave it is in — which is what [D4] exists for. Settled in slice 03.
- **Can one Projects v2 Status field hold both column families?** One field holds one enum. Whether
  that reads as one board or two boards wearing one is slice 03's question.
- **GitLab rendering is unverified.** Morgan's stated requirement is to open the issue *in GitLab*,
  while this repo's board is GitHub (user project 3). The skeleton therefore verifies the projection's
  **format** but not its GitLab rendering, and the glanceability KPI would be measured on the wrong
  forge. Recorded as a limitation of slice 01's evidence, not as covered.
- **Do two-line step descriptions change `nwave-slice-status`'s table?** Morgan asked for two lines per
  row; that skill renders "What it does" as one. Either the cell grows or a column is added — and the
  choice belongs to that skill, per [D10].

## Wave: DISCUSS / [REF] Scope assessment

**OVERSIZED** — four signals fire; two are the threshold.

| Signal | Reading |
|---|---|
| >3 modules | **6** — `nwave-issue-board`, `issue-board`, `nwave-slice-status`, `groom-issues`, `rank-issues`, `session-handoff` |
| Multiple independently shippable outcomes | **4** — the card paradigm, the in-issue projection, the transferable stack, the grooming/ranking adaptation |
| Estimated effort | >2 weeks: ~40 fixtures plus two ADR-level reversals |
| >10 stories | Likely across that surface |

Split into **six** slices — five user-confirmed 2026-08-14, plus slice 06 added by the amendment pass
that same day when the backbone exposed a missing migration.

**Taste tests are now per slice**, in a table at the foot of each brief, per Phase 2.5 step 5. The
original pass applied them collectively here, which is why slice 02's failure was legible and the rest
were assertions. One documented failure stands: **slice 02 is ~1.5 days, over the one-day test**, kept
whole because the rules and their fixtures must ship together — this repo's fold-back rule requires the
fixture that would have caught the gap, and fixture 15 caught its own skill in the same commit.

## Wave: DISCUSS / [REF] Story map — backbone

Added by the amendment pass (2026-08-14). Phase 2.5 requires this **before** slicing, and the original
pass went from scope assessment straight to slices — cutting vertically through a backbone nobody had
written down. Producing it late is worth doing anyway, because it surfaced two things the slice set had
not accounted for.

Morgan's activities, left to right in the order they occur:

| # | Activity | What Morgan is doing |
|---|---|---|
| A1 | **Find the work** | See which features exist, which are in flight, who owns them, what is next |
| A2 | **Understand a feature's state** | Open one card and read position *and* why, in seconds |
| A3 | **Take it on** | Claim it, and know which command owns the work |
| A4 | **Work it** | Advance the feature under that command rather than inline |
| A5 | **Handle a diversion** | Push and pop without losing the thread |
| A6 | **Put it down** | Capture what a fresh session cannot derive; refresh the projection |
| A7 | **Keep the board honest** | Groom and rank a board whose unit is the feature |

Slices against activities:

| Slice | Activities it serves |
|---|---|
| 01 One card as walking skeleton | **A2** (the core read) |
| 02 The mapping becomes normative | A2, A3 — the projection format and the routing line become rules |
| 03 Wave columns and blocked | **A1** — columns are how the work is found |
| 04 The diversion stack, projected | **A5, A6**, and completes A2's *why* half |
| 05 Grooming and ranking adapt | **A7** |
| 06 Consolidate the existing board | **A1** — the board must actually hold feature cards |

**A4 is served by shipped work, not by a slice.** The `Work this with:` routing line already exists
(`nwave-issue-board/SKILL.md:186-212`, from `session-handoff` slice 02). An activity covered by existing
capability is not a hole, but it has to be named as covered — otherwise the next reader sees a backbone
activity with no slice and invents one.

**The finding the backbone produced: A1 is broken for the whole feature until slice 06 lands.** Slice 06
sits last on learning leverage, and A1 sits first on the backbone. So through slices 01-05 the board
holds old-paradigm slice cards *and* the new single card side by side, and "find the work" is answered
inconsistently the entire time.

Keeping 06 last anyway, and recording the mixed board as an **accepted transient** rather than
discovering it mid-flight. Two reasons it is tolerable, and one reason it is actively useful: the
migration cannot safely precede the mapping (02), the columns (03), or a projection with content in it
(04) — and a board showing both shapes in the same columns during slice 03 is the most direct comparison
available of whether the new shape reads better. Backbone order is journey order; execution order is
learning-leverage order. A reader must not mistake one for the other.

## Wave: DISCUSS / [REF] Slices and order

Ordered by **learning leverage** — the riskiest assumption first, so a failure costs least.

| # | Slice | Disproves if it fails |
|---|---|---|
| 01 | One real feature as one card (walking skeleton) | That one card can carry a feature legibly at all |
| 02 | The mapping becomes normative | That the change is containable in one skill |
| 03 | Wave columns and the blocked question | The one-board design |
| 04 | The diversion stack, projected (carries the ADR-013 amendment) | The local-authoritative surface [D7] |
| 05 | Grooming and ranking hold (carries the `jobs.yaml` facets) | That the shipped defect oracle needs no change |
| 06 | Consolidate the existing board | That consolidation is possible without the parent lying about completion |

Briefs at `docs/feature/single-issue-per-feature/slices/slice-NN-*.md`.

**Two briefs exceed the ≤100-line guideline and say so here rather than being trimmed into inaccuracy.**
Slice 05 is 122 lines and slice 06 is 113; both carry sections the wave mandates *on top of* a standard
brief — the carpaccio taste-test table in both, plus a `Changed Assumptions` section in 05 required by the
back-propagation contract. Excluding those, each is at or under 100. One real trim was made rather than
tolerated: slice 05's `Changed Assumptions` originally restated the delta's account of the same
correction, and now references it — the restate-versus-reference fault this repo has caught twice before
(`docs/evolution/2026-08-10-issue-board.md:199-201`).

No standalone ADR/SSOT slice: the composition hard gate rejects a slice of only `@infrastructure`
stories, so those land inside the slices that motivate them.

**Order: slice number, provisional until `/nw-roadmap`** — which never runs in this repo, so the
provisional order is the final one. That is itself slice 01's test of the provisional-order path.

## Wave: DISCUSS / [REF] WS strategy

**C — real local resources.** The skeleton writes to the real board (`pmvanev/phil-claude-plugin`,
user project 3) rather than a faked forge adapter. Strategy letters per ADR-013's usage, which is the
only definition this repo records.

Justified because the whole uncertainty in slice 01 is *how a real rendered issue reads to a human in
seconds* — a faked adapter answers a question nobody asked. The cost is a real card on a real board,
mitigated by [D12]: the subject is this feature's own new card, so nothing in flight is disturbed.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Change |
|---|---|---|
| `phil:nwave-issue-board` | Skill (knowledge-only, no command) | Mapping table, ordering, two-stage fill rewritten; fixtures realigned |
| `phil:issue-board` | Skill (knowledge-only) | *Choosing what becomes an issue* gains the concurrency reading; per-project template gains the column families |
| `/phil:nwave-slice-status` | Command + skill | Gains the feature-level fold [D10]; possibly the two-line description |
| `/phil:groom-issues`, `/phil:groom-ask`, `/phil:groom-fix`, `/phil:groom-set` | Commands | Oversized-card heuristic becomes paradigm-aware; session-state-as-defect reversed |
| `/phil:rank-issues` | Command | Ranked unit changes from slice to feature |
| `/phil:handoff`, `/phil:resume` | Commands | Handoff refreshes the projection; resume reads the local authority as it already does |

No new command. Every surface is an existing one, which is why [D5]'s facets are the honest record
rather than a new job standing alone.

## Wave: DISCUSS / [REF] Journey

Full journey at `docs/product/journeys/single-issue-per-feature.yaml`.

Morgan opens a feature issue — their own, or a colleague's — and within seconds reads the wave, the
current slice, which steps are done, which one is in flight, and why work stopped. The reasoning and
the diversion stack arrive as a projection of the last handoff, honestly timestamped. Morgan claims
the card, and the routing line names the command that owns the work rather than inviting inline work.
A mid-work diversion is pushed onto the local stack and reaches the issue at the next boundary. At
session end the snapshot is written locally and the projection refreshed.

Arc: `uncertain → oriented → informed → committed → trust → unbothered → relief` (upward).

**The accepted cost of [D7]**, recorded in the journey's error paths: a teammate sees only what the
last `/phil:handoff` projected. If Morgan never ran it, the projection is absent — and **absent must
render as "unknown", never as "no diversions"**. This is the same discipline as `unknown` never being
published as `not started` (`nwave-issue-board/SKILL.md:135-137`), and the same accepted-cost shape as
a declined grooming candidate returning next run.

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: make-in-flight-work-transferable` unless marked otherwise.

### S1 — Read a feature's state in seconds

As Morgan, I open the feature issue and understand where the work stands without opening the repo.

**Elevator Pitch**
Before: understanding a feature's state means cloning the repo and running a status command, or asking
the owner in chat.
After: open the feature issue → sees a delimited block with `Wave: DELIVER`, `Work this with:
/nw-execute`, a slice roster, and the current slice's step table with `✓ ▶ ·` indicators and a
two-line description per step, above a generation timestamp.
Decision enabled: whether to pick this feature up, or leave it for its owner.

AC1 — The block renders wave, current slice, per-step glyph state, and a timestamp; a reader
unfamiliar with the feature names all four within 30 seconds (KPI-1).
AC2 — No indicator is a markdown checkbox ([D8]); the table is `✓ ▶ ·` glyphs generated from
`nwave-slice-status`.
AC3 — Steps outside the current slice are not enumerated; the roster links their slice files ([D9]).

### S2 — Inherit a colleague's in-flight feature

As Morgan, I take over a feature someone else started without asking them a question.

**Elevator Pitch**
Before: the reasoning lives in `.session-handoff.md` on someone else's laptop, git-ignored — ADR-013
states the consequence outright: "Nothing is shared with a teammate."
After: open the issue → sees the projected why, the intended next action, and the diversion stack as
of the last handoff, each stamped with when it was captured.
Decision enabled: resume, or ask the owner one specific question instead of "what's the state of this?"

AC1 — The projection carries the why, the next action, and the stack, each with a capture timestamp.
AC2 — Where no snapshot was projected, the block says `unknown` for the stack — never renders empty as
"no diversions".
AC3 — Nothing in the block was typed by a human; a human edit inside the markers is replaced and the
replacement noted, per the shipped 04/11 rule.

### S3 — Put a feature down and pick it up tomorrow

As Morgan, I end a session mid-feature and resume the next morning without re-briefing.

**Elevator Pitch**
Before: `/phil:handoff` records the state locally, and nothing outward-facing changes.
After: run `/phil:handoff` → sees the snapshot written locally **and** the issue's projection block
refreshed with a new timestamp.
Decision enabled: whether tomorrow's session can trust the issue, or must reconstruct.

AC1 — Handoff writes the local authority first, then refreshes the projection ([D7]).
AC2 — A session that advanced nothing writes no snapshot and refreshes nothing (inherited anxiety D).
AC3 — `/phil:resume` reads the local file, not the issue — the projection is never read back.

### S4 — Record a diversion without losing the thread

As Morgan, I get diverted from task A to B to a devops script C, and the detour is recorded rather
than remembered.

**Elevator Pitch**
Before: the diversion stack exists in no artifact, by design, and dies with the session.
After: push the diversion → sees the stack in the issue at the next boundary, innermost first, with
each frame's open-since time.
Decision enabled: what to return to, and in what order, after the detour closes.

AC1 — Pushes and pops go to the local authority; the issue is refreshed at boundaries, never per push
(`Refresh at boundaries`, which forbids per-step forge writes).
AC2 — A frame open longer than one boundary is marked, so a never-popped push is visible rather than
silently stale.

### S5 — Groom a board of feature-cards without false positives `@infrastructure`

As Robin, I run grooming against the new paradigm and every correctly-shaped card passes.
`job_id: keep-a-backlog-trustworthy` (elicitation-adjacent facet).

**Elevator Pitch**
Before: a feature card's projected session state trips the session-state-is-a-body-defect rule, so
grooming reports a finding against a correctly-shaped card.
After: run `/phil:groom-issues` → sees zero findings against a correctly-shaped feature card.
Decision enabled: whether the board is actually clean, rather than noisy by construction.

AC1 — A correctly-shaped feature card produces no session-state finding, and **no oversized finding
under the rule's existing text** — verified without modifying that text.
AC2 — A generated region is still refused for editing, per the shipped error path.
AC3 — The reversal is recorded in `journeys/groom-issues.yaml` with the original quoted verbatim.

Amended 2026-08-14: the original pitch claimed grooming flags a correct card **twice**, on oversized and
on session state. Only the second is real — see *Changed Assumptions*.

This story is `@infrastructure`-adjacent but **not** `@infrastructure`: Robin observes a changed
output. Slice 05 also carries S6, so the composition gate is satisfied regardless.

### S6 — Rank a board whose unit is the feature

As Robin, I rank features rather than slices. `job_id: keep-a-backlog-trustworthy`.

**Elevator Pitch**
Before: ranking orders slice cards, so a feature's position is implied by N cards that may disagree.
After: run `/phil:rank-issues` → sees one position per feature, ordered within its goal.
Decision enabled: which feature to start next.

AC1 — The ranked unit is the feature card; no slice card is expected or required.
AC2 — A dependency uncovered during ranking is written as a real forge link, as it already is.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Measurement |
|---|---|---|---|
| KPI-1 | Time to comprehension | ≤ **30 s** to name wave, current slice, current step, and why work stopped | Timed read of the slice-01 card by a reader who has not seen the feature; n≥1, self-reported and recorded in the slice brief |
| KPI-2 | Cards per feature | Exactly **1** (from 1 + N) | Board query: items whose parent is the feature |
| KPI-3 | Projection staleness | Block timestamp within **one boundary** of the last artifact change | Compare block timestamp to the last commit touching the feature's artifacts |
| KPI-4 | Grooming false positives | **0** correct cards flagged oversized or session-state-bearing | Run `/phil:groom-issues` after slice 05 and count |
| KPI-5 | Questions asked on inherit | **0** clarifying questions before resuming | Counted the first time a teammate inherits a card; n=1, honestly labelled |

KPI-1 is slice 01's oracle and the reason [D13] exists. KPI-5 is the premise's own test: if teammates
never inherit anything, the number is never measured, and that absence is itself the finding.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `morgan-feature-owner`, new; distinguished from Kai and Robin in *Persona ID* |
| 2 | Job traceability | ✓ | New job `make-in-flight-work-transferable` + two facets, [D5] |
| 3 | Journey mapped | ✓ | `journeys/single-issue-per-feature.yaml`, arc upward, error paths incl. the [D7] cost |
| 4 | Stories with elevator pitches | ✓ | S1-S6, each naming a real invocable entry point |
| 5 | ACs testable | ✓ | Each AC names an observable; KPI-1 supplies the number for the one that was a vibe |
| 6 | Scope assessed | ✓ | OVERSIZED; five slices user-confirmed, sixth added by the amendment pass |
| 7 | Slice briefs exist | ✓ | Six briefs under `slices/`, each with a carpaccio taste-test table |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..5, each with a target and a method |
| 9 | Out-of-scope explicit | ✓ | Below |

Requirements completeness: **0.97**, up from 0.96 once the backbone and the per-slice taste tests landed.
The shortfall is named rather than rounded away — the four items under *Open (→ authoring)*, of which the
GitLab rendering gap is the one that could invalidate KPI-1's measurement.

**These nine items were authored for this feature, not taken from a canonical list**, because none is
recorded in this repo. The validation is therefore self-graded, which is the weakness
`docs/evolution/2026-08-10-issue-board.md:352` names about `nw-skill-reviewer` — "treat it as a structure
check, not a quality gate." Stated so a reader does not mistake a ticked table for an external gate.

## Wave: DISCUSS / [REF] Out-of-scope

- **Bidirectional sync.** The forge remains a projection. `phil:issue-board`'s *One system of record
  per scope* is unchanged by this feature.
- **Multi-session and multi-person arbitration.** Competing claims are **detected, not resolved** —
  inherited verbatim from `session-handoff`'s v1 boundary. Two people claiming one feature is now more
  likely, and the honest boundary is still detection.
- **GitLab child work items.** `rolledUpCountsByType` is marked Experiment on 18.9.1-ee and was never
  run; nothing here depends on it.
- **Epics and any GitLab Premium mechanism.** Premium and group-scoped; the design must work on Free.
- **Assignment automation.** Who takes which feature stays a human decision; the board makes ownership
  legible and stops there.
- **Retiring `.session-handoff.md`.** [D7] keeps it as the authority. This feature adds a projection.
- **A wave column family for non-nWave work beyond the generic four.** Non-nWave stories get to-do /
  in-progress / blocked / done and nothing more.

## Wave: DISCUSS / [WHY] Alternatives considered

Rendered by the amendment pass. This is the **only** Tier-2 expansion rendered — density stays
`lean` + `ask-intelligent`, its trigger (cross-context complexity: six modules, two forges plus Projects
v2 plus local files) fired in the original pass, and the user accepted it. The other seven catalog items
stay unrendered.

**Telemetry not emitted.** The wave mandates a `DocumentationDensityEvent` via
`scripts/shared/telemetry.py` and forbids writing JSONL directly. That helper does not exist in this
install — `~/.claude/skills/nw-discuss/` ships only `SKILL.md`. Stated rather than faked, and rather than
worked around. The previous wave hit the same gap and recorded it as noticed, not carded.

### [D7] The diversion stack's surface — three candidates

| Candidate | Why it lost |
|---|---|
| **Forge comments are the authority**, description renders them | Append-only and time-ordered exactly as a stack is, attributed and timestamped for free — the best *fit*. Lost on a shipped rule: `nwave-issue-board/SKILL.md:238-241` forbids per-step forge writes ("a per-step write turns each TDD cycle into a forge round-trip, and a missed one is invisible"), and a push or pop is finer-grained than a step. It is the only candidate with real history, which is why it is recorded rather than dismissed. |
| **The description block is the authority**, typed by the command | Simplest, and reachable by a teammate with no dependency on anyone's laptop. Lost on inverting *generated, never typed*, and on having no history: a description rewrite loses the prior stack with nothing to recover it from. |
| **Local file authoritative, issue carries a one-way projection** ✓ | Won because it preserves four shipped rules simultaneously — the one-way projection, ADR-013's snapshot surface, *Refresh at boundaries*, and one-system-of-record — and reduces the ADR change to adopting its own deferred option. The projection can only be stale if work continued after handing off, which is self-contradictory. |

The reframe that made the winner legal: **the operative rule is single-authority-per-fact, not "the forge
stores nothing."** A diversion stack is not in `docs/feature/` and never will be, so the forge holding a
projection of it inverts nothing.

### [D5] Job structure — three candidates

| Candidate | Why it lost |
|---|---|
| **Facets only, no new job** | Matches the dominant house pattern (`redesign-tests`, `mobile-web-standards` both refined rather than added). Lost because the transferability outcome would be owned by no job, and DoR requires every story to trace to a `job_id` — the stories would have had nowhere to point. |
| **New job only** | Fastest. Lost because grooming's defect oracle and handoff's surface both genuinely change, and leaving those unrecorded is the SSOT drift the repo's standing check exists to catch. |
| **New job plus facets on both** ✓ | Honest about all three changes. First feature in this repo to touch two jobs at once, which is stated rather than smuggled. |

### [D6] Persona — three candidates

| Candidate | Why it lost |
|---|---|
| **Extend Kai (`kai-session-relay`)** | Closest fit, and the reuse pattern the house prefers. Lost because all four of Kai's recorded frustrations are solo-session, and the role reads "one session to the next" — extending it to "one person to the next" would have meant rewriting the persona rather than widening it. |
| **Extend Robin (`robin-backlog-curator`)** | Robin already owns a board other people file into. Lost on the curator/owner boundary that persona file draws explicitly against Quinn: Robin curates cards without working them. |
| **New persona `morgan-feature-owner`** ✓ | The reader who inherits a colleague's half-done feature is neither of the above, and the confirmed premise makes them real rather than hypothetical. |

### Slice 03 — the blocked column, three candidates, still open

Lifted here from that brief so the decision record sits in one place. A blocked card must leave its wave
column, because blocked is a column and a card holds one position — and the moment it does, the board
stops showing which wave it is in.

| Candidate | Standing |
|---|---|
| The wave label carries it ([D4]) | Cheapest; relies on a label being read, which is what the wave-as-column reversal was meant to stop relying on. |
| Blocked is not a column — a label or a dependency link | Keeps the wave visible; loses the at-a-glance "what is stuck" read. |
| Blocked is a column, wave restated in the generated block | **Current lean.** The block exists either way and is generated rather than typed, so the information is moved rather than lost. |

Deliberately unresolved: slice 03 decides it against the rendered board, because that is how the
2026-08-10 wave-column decision was reversed the first time.

### [D12] Walking-skeleton subject — three candidates

| Candidate | Why it lost |
|---|---|
| `session-handoff` #9 with slices #11/#10/#12 | The most direct before/after, and it genuinely exercises the sub-issue collapse. Lost on disturbing a real card set. |
| `groom-issues` #5 | Richest current-slice projection. Lost because slice 04 must land against a stable card, which the user sequenced first. |
| **This feature's own card** ✓ | Self-hosting, disturbs nothing in flight, and since DELIVER never runs here it also exercises the provisional-order path for real. |

## Wave: DISCUSS / [REF] Pre-requisites

1. **`groom-issues` slice 04 committed** ([D11]) — five fixtures (25-29) and a slice brief currently
   uncommitted.
2. **Plugin skew closed, or the version stated.** `/phil:*` commands load 0.27.0 while this tree is
   0.36.0; any dogfood claim in slice 01 must name the version it exercised.
3. **`gh auth` retains the `project` scope** — required to add wave columns to user project 3.
4. **A GitLab instance, if KPI-1 is to be measured where Morgan actually reads** — otherwise slice 01's
   evidence is GitHub-only and says so.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

One issue per nWave feature or story, self-contained: a generated projection carrying the wave, the
slice roster, the current slice's step table with glyph indicators and two-line descriptions, the
diversion stack, and the why — read in seconds, by its owner tomorrow or a teammate today. Board
columns become the waves plus a generic family for non-nWave work. Slices and steps stop being cards.

### Constraints established

- **C1** Single-authority-per-fact, not "the forge stores nothing" — the reframe that makes [D7]
  legal without inverting the one-way rule.
- **C2** Generated, delimited, timestamped, never read back. Every projection in this feature.
- **C3** No hand-ticked state anywhere ([D8]).
- **C4** Bounded description ([D9]) — the inverted form of the hundreds-of-issues argument.
- **C5** Derivation stays with its owner ([D10]).
- **C6** Absent state renders as `unknown`, never as a benign default.
- **C7** No per-push forge writes; refresh at boundaries only.

### Upstream changes

Two SSOT items change, both quoted verbatim in the artifacts that carry them rather than edited
silently:

1. **`jobs.yaml`, job `carry-work-across-session-boundaries`, anxiety (C)** — "Session scratch
   published to a board is visible to everyone who reads the board." Now a **deliberate trade** rather
   than a force the design avoids: the projection carries what a teammate needs and the local file
   keeps in-flight scratch. Recorded as a facet, not a deletion.
2. **`journeys/groom-issues.yaml:99-102`** — session state in a body is currently a **body defect**.
   Reversed for a generated, delimited projection; still a defect for typed scratch outside the
   markers. Slice 05.

**ADR-013 is amended, not superseded.** Its *partitioned local + board* alternative — "the likely end
state … deferred, not rejected" — is adopted as written, and its consequence line "Nothing is shared
with a teammate. Accepted for v1; the partitioned option above is the documented path if that need
appears" is the trigger this feature fires.

### Also found, out of scope

`docs/product/architecture/brief.md:379` reports `session-handoff` as "DESIGNED (2026-08-12) — not yet
implemented", while `skills/session-handoff/SKILL.md`, `acceptance.feature`, `self-test/`,
`commands/handoff.md` and `commands/resume.md` all exist and `CLAUDE.md` documents both commands as
operational. SSOT drift, and a standing check per `CLAUDE.md`. Flagged, not fixed here.

---

## Changed Assumptions — amendment pass, 2026-08-14 (same day)

Three changes to this wave's own output, recorded per the back-propagation contract rather than edited in
silently. The prompt was the user asking whether grooming and ranking had been accounted for, and whether
the next groom would end up recombining tickets it had previously split.

### 1. Slice 05 proposed a change that would have caused a defect

**Original, verbatim** from `slice-05-grooming-and-ranking-adapt.md`:

> The oversized heuristic gains the structured/unstructured discriminator, with the reasoning.

**New assumption.** `skills/groom-issues/SKILL.md:268` defines oversized as *"a card carrying work that
cannot be demonstrated on its own"* — **demonstrability, not size.** A feature is precisely a thing that
can be demonstrated on its own, so a feature card already passes and no discriminator is needed. Slice 05
now **verifies** the rule holds, with a fixture, and is renamed
`slice-05-grooming-and-ranking-hold.md`.

**Rationale.** The original was not merely unnecessary. A size-aware heuristic is the mechanism by which
grooming would propose splitting a large feature card back into slices — and because `groom-issues` stores
no marker by design, a declined split returns every run and only has to be accepted once. That is the
consolidate → split oscillation the user asked about, and the wave would have introduced it.

**This feature's own `jobs.yaml` facet predicted it.** The `keep-a-backlog-trustworthy` paradigm facet,
written in the same pass as the original brief, records anxiety **(F)**: *"An oracle loosened to stop the
false positives stops catching the real ones."* Four files apart, in one wave, the hazard was named and
then committed. The lesson kept is not "check the rule text" — it is that **a hazard recorded in one
artifact does not defend the artifact written beside it.**

### 2. Story S5's elevator pitch overstated the collision

**Original, verbatim:**

> Before: a whole feature in one issue trips the oversized-card heuristic, and its projected session
> state trips the session-state-is-a-body-defect rule — so grooming flags every correct card twice.

**New assumption.** Only the session-state half is real. The pitch and AC1 are corrected; the oversized
half becomes a verification rather than a fix.

### 3. Slice 06 was missing, and out-of-scope did not cover it

**Original:** the *Slices and order* table listed five slices, and *Out-of-scope* did not mention
migrating the existing board — so consolidation was absent rather than deferred.

**New assumption.** The board holds `session-handoff` #9 with slices #11/#10/#12, `groom-issues` #5 with
its slices, and others, and **nothing will flag them**: against the four set-level classes they are not
duplicates, not oversized, not overcome by events, not ungrouped. Grooming reports the old-paradigm board
clean, correctly. Consolidation is a one-time migration, not a grooming operation, and it is now slice 06.

**Rationale for its position.** Last on learning leverage, though it serves the *first* backbone activity
— which is why the mixed board is recorded as an accepted transient under *Story map — backbone* rather
than discovered mid-flight.

### Also closed by this pass

Two Phase 2.5 gate items the original pass skipped: the **story-map backbone** (which is what exposed
change 3) and **per-slice carpaccio taste-test tables** on all six briefs. The `alternatives-considered`
Tier-2 expansion was rendered, its trigger having fired in the original pass and been accepted here.
