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

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one issue, one hand-built block, board columns. No skill or command touched. |
| Depends on a new abstraction? | **This slice IS the abstraction.** The projection format ships here first, before any slice assumes it — which is the taste test's own prescribed remedy. |
| Disproves a pre-commitment? | Yes, the largest one: that a single card can carry a feature legibly at all. KPI-1 is a number, not a judgement. |
| Synthetic data only? | No — the real board, this repo's own feature, and a real timed read. |
| Duplicate of another slice at scale? | No. 02 makes the format normative; this discovers whether the format is worth asserting. |
