# Slice 01 — One real feature as one card (walking skeleton)

**Goal:** Build, by hand, a single-card projection for this feature on the real board, and measure
whether a reader understands where the work stands in under thirty seconds.

**Stories:** S1 (read a feature's state in seconds)
**WS strategy:** C — real local resources (the real board; not a faked adapter)

## Learning hypothesis

**Disproves** the whole paradigm if the block reads as an unreadable wall, or if the column tells a
teammate nothing they can act on — for the price of one issue and no skill edits.
**Confirms**, if it passes, that the projection format is worth making normative in slice 02.

This is the highest-uncertainty slice, which is why it is first: everything downstream assumes a
rendered single card is legible, and nothing has ever rendered one.

## IN scope

- One new issue on `pmvanev/phil-claude-plugin`, subject = **this feature** ([D12]).
- A hand-built `nwave:status` block containing, in this order:
  - `Wave:` line and a generation timestamp
  - `Work this with:` routing line, derived from the wave label
  - the **slice roster** — the five slices from `feature-delta.md`, in array order, as bare rows
  - the **current slice's step table** — `Step | What it does | Status | Notes`, with `✓ ▶ ·` glyphs
    and a two-line description per row
  - `Order: slice number, provisional until /nw-roadmap`
- Wave columns added to user project 3, plus the generic family ([D3]) — enough to place this card.
- The timed read: a reader who has not seen the feature names wave, current slice, current step, and
  why work stopped. Result recorded in this brief, pass or fail.

## OUT scope

- Any edit to any skill or command. The block is hand-built on purpose — this slice tests the
  **design**, not an implementation of it.
- The diversion stack (slice 04) and the `why` projection. The block carries position only.
- Grooming (slice 05). Running `/phil:groom-issues` against this card will produce false positives,
  and that is expected rather than a defect to chase here.
- GitLab. See the limitation below.

## Acceptance criteria

1. The card exists on the board, in a wave column, with the block rendered.
2. **KPI-1:** the timed read completes in ≤30 s and names all four facts. Recorded with the time.
3. No indicator in the block is a markdown checkbox ([D8]).
4. Steps outside the current slice are not enumerated ([D9]).
5. Because there is no `roadmap.json`, the roster carries the provisional-order line verbatim —
   exercising the path `nwave-issue-board/SKILL.md:110-114` describes and nothing has run.
6. The block is delimited by `<!-- nwave:status:begin -->` / `<!-- nwave:status:end -->` markers, so
   slice 04 can replace its contents without touching prose added around it.

## Stated limitation (do not let this pass as covered)

Morgan's requirement is to open the issue **in GitLab**; this board is GitHub. This slice therefore
verifies the projection's **format and legibility**, not its GitLab rendering, and KPI-1 is measured on
the wrong forge. Two things follow: the evidence must say "GitHub, `gh` <version>" explicitly, and a
GitLab re-measurement stays on the open list in `feature-delta.md`.

## Dependencies

- `groom-issues` slice 04 committed ([D11]).
- `gh auth` holds the `project` scope.
- Plugin skew: this slice is hand-driven, so it exercises **the prose, not the command** — which must
  be said in the evidence, per `CLAUDE.md`.

## Effort

~2-3 hours. Reference class: `nwave-issue-board`'s original three-sub-issue verification pass
(2026-08-12), which built real cards on the real board and read back GraphQL counters in one sitting.

## No pre-slice SPIKE

The uncertainty is entirely about how a rendered page reads, which is what the slice itself answers.
A SPIKE would build the same card and call it a probe.

## Result — card built 2026-08-14 as issue #26

`https://github.com/pmvanev/phil-claude-plugin/issues/26` · project 3, Status=Todo · labels
`documentation` + `enhancement` (both, per the multi-valued declaration) · `subIssuesSummary {0, 0}`,
confirming no sub-issues, which is the paradigm.

**PASS on what this slice shipped.** Measured by the owner, 2026-08-14: **under 30 s**, naming the wave
(*"a big check by the wave"*) and the current slice (*"the right icons in the slice/status table"*).

**Volunteered, and not in any AC:** *"I like that the artifacts are all linked **and summarized**."* The
summarising is what made the links useful — a bare list of six URLs would have cost the reader the thirty
seconds the KPI is about. Worth promoting into slice 02's normative projection contract, because nothing
currently requires it.

**Not measured by the author.** The grader problem the `nwave-issue-board` suite already names about
itself — *"the grader was also the author"* — applies to the card, so the read was the owner's, not mine.

### Finding 7 — KPI-1 was mis-scoped as this slice's oracle

KPI-1 asks a reader to name **four** facts: wave, current slice, current step, and why work stopped. This
slice was only ever going to ship **two** of them:

| Fact | On the card? | Why |
|---|---|---|
| Wave | ✓ | |
| Current slice | ✓ | |
| Current step | **never** | No `roadmap.json`; DELIVER does not run here (finding 2) |
| Why work stopped | not yet | The `why` and the stack are **slice 04**, explicitly in this slice's OUT scope |

So a strict reading of KPI-1 fails a slice that did everything it promised. The KPI is a **whole-feature**
measure and was borrowed as a per-slice oracle without being cut down. Restate it as:

- **Slice 01's oracle** — wave and current position, under 30 s. **Met.**
- **Slice 04's oracle** — the same read, plus *why work stopped*, under 30 s. Not yet attempted.
- **Drop "current step" in this repo**, or make it conditional on a roadmap existing. It stands for real
  nWave product repos and is unreachable here.

The lesson matches finding 2's shape: **a measure written for the feature will over-claim against the
slice that carries only part of it**, and the failure is silent, because the slice looks like it missed.

### Six findings, five of which the design could not have predicted

1. **No `Work this with:` line is possible for this feature.** The wave→command table covers DISCOVER
   through DELIVER. This repo authors prose with `plugin-dev` instead of running DESIGN/DISTILL/DELIVER,
   and **that path has no row** — so the rule *no label, no line* fires and the card carries no routing.
   The routing table does not cover the build path of the repo that owns it.
2. **The step table never arrives, so promising it would lie.** *Fill in two stages* defers step rows
   until `/nw-roadmap` writes `roadmap.json`, and fixture 07 requires the card to *say* the table is
   coming. **DELIVER never runs here**, so that sentence would be an unkeepable promise. The card says so
   instead, and the slice roster carries the two-line descriptions the step table would have. **Fixture 07
   assumes the roadmap eventually arrives** — true in an nWave product repo, false in this one.
3. **Absolute links 404 until the branch merges.** The artifacts exist only on
   `board-paradigm-and-groom-foldbacks`, and `phil:issue-board` requires absolute `blob/main` URLs because
   relative paths 404 on GitHub. Linked to `main` anyway — a branch URL rots when the branch is deleted —
   with one line saying where they live meanwhile. **Any card created before its artifacts merge has this
   problem, and nothing in either skill mentions it.**
4. **Slice 06 may be nearly empty, and this is the sharpest finding.** The design assumed the board holds
   live feature-plus-slice groups. It does not: `session-handoff` #9, `groom-issues` #5, and **every slice
   card (#10-#15) are CLOSED.** No open feature on this board has slice children. So consolidation has
   almost nothing live to consolidate, and the hazard slice 06 was built around — closing children
   inflating a parent's rollup to 100% — **is moot for parents that are already closed and done.**
   Re-scope slice 06 before starting it; the likely answer is that closed cards are the record of how the
   work went and must not be retro-consolidated at all.
5. **The board has three Status options — `Todo`, `In Progress`, `Done` — and no `blocked`.** Slice 03's
   framing assumes blocked is already a column; it is not. Adding the wave family takes the field from 3
   options to about 11, which is a larger and more disruptive change to existing cards than the brief
   implied.
6. **`gh project item-add` exited 0 with no output**, exactly as `phil:issue-board` records under *Verify
   the end state*. The GraphQL read-back is what established the item landed. The documented behaviour
   held; noted because it is the first time this repo has exercised it rather than cited it.

**Not a finding, but worth stating:** the projection was hand-built, so this exercised **the prose, not the
command** — and `/phil:*` loads 0.27.0 while this tree is 0.40.0. No claim here is a claim about a command.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one issue, one hand-built block, board columns. No skill or command touched. |
| Depends on a new abstraction? | **This slice IS the abstraction.** The projection format ships here first, before any slice assumes it — which is the taste test's own prescribed remedy. |
| Disproves a pre-commitment? | Yes, the largest one: that a single card can carry a feature legibly at all. KPI-1 is a number, not a judgement. |
| Synthetic data only? | No — the real board, this repo's own feature, and a real timed read. |
| Duplicate of another slice at scale? | No. 02 makes the format normative; this discovers whether the format is worth asserting. |
