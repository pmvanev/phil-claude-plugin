# Slice 03 — Claimed-card link

> **DEFERRED 2026-08-12 — pending evidence, not cancelled.** Slices 01 and 02 shipped; this one's
> learning hypothesis (*the board already carries enough*) is so far holding: the snapshot's `Next`
> field carried the work identity in prose on every dogfood run, and the two-cards-In-Progress
> evidence below proved to be board hygiene rather than a design gap — #3 had simply been left there.
> Card #12 stays open as the standing follow-up. Note this brief carries a `DEFERRED` marker, which
> `phil:nwave-issue-board` treats as "not a card"; the card is retained deliberately, because this
> feature no longer publishes through that flow.

Feature: session-handoff · Job: `carry-work-across-session-boundaries` · Persona: `kai-session-relay`

## Goal

A session records which board card it claimed and why that card was next, so the next session resumes
against the same card rather than re-deciding.

## Learning hypothesis

**Disproves that the board already carries enough** — if resuming works fine from the card's own
status without a recorded claim, then category 4 of the design axis collapses into the board and this
slice should not ship.

**Confirms** that the session→card link is real missing state — the board knows a card is
*In Progress*; it does not know which session claimed it, or that the claim was made mid-stream while
another card was already in flight.

That case is not hypothetical: this board currently shows **two** cards In Progress (#3 and #9), and
nothing records that #9 was claimed in a later session than #3.

## IN scope

- Record the **claimed card** (issue number) and the **basis** for it being next, at capture.
- Surface both at read-back, so resumption targets the same card.
- **Detect** a competing claim — another snapshot naming the same card, or a card whose board status
  contradicts the recorded claim — and report it.
- Respect the **one-system-of-record** partition: the board stays the authority on card *status*; the
  snapshot carries only the session→card link, which the board cannot express.

## OUT scope

- **Resolving** a competing claim. Detection without resolution is the honest v1 boundary; arbitrating
  between two live sessions is named out-of-scope for the whole feature.
- Writing session scratch into the issue body. Anxiety C — the board is world-readable, and in-flight
  detail belongs on the local surface.
- Changing card status automatically. Moving a card is a deliberate act, and `phil:issue-board` treats
  a position and a status as claims someone made.
- Multi-repo or cross-forge claims.

## Acceptance criteria

1. Given a session working a card, when capture runs, then the snapshot records the issue number and
   the stated basis for it being next.
2. Given a snapshot recording a claimed card, when read-back runs, then resumption targets that card
   and states its basis.
3. Given a recorded claim whose card status on the board contradicts it (e.g. recorded as claimed but
   now closed), when read-back runs, then the contradiction is reported and the board is treated as
   authoritative on status.
4. Given two snapshots naming the same card, when read-back runs, then the competing claim is reported
   and neither is silently discarded.
5. Given the snapshot writes a claim, when the board is inspected, then no session scratch was written
   into the issue body.

**Production data**: this repo's real board, including the real two-cards-In-Progress state described
above.

## Dogfood moment

Same day: claim a card, end the session, resume, and confirm the same card is picked up with its basis
intact — against the live board rather than a fixture.

## Dependencies

- **Slice 01** — extends the snapshot format with the claim.
- Independent of slice 02; routing and claiming are separate facts about the same pickup.

## Effort and reference class

≤1 day (≤6h). Lowest-uncertainty slice of the three: mostly a field on an existing format plus board
reads. Reference class: the board read-back mechanics already exercised in this feature's own DISCUSS
wave (`gh api graphql` item/field reads), which are known-good.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one field on slice 01's format, one read-back check. |
| Depends on a new abstraction? | Consumes slice 01's format; introduces none. |
| Disproves a pre-commitment? | Yes — that the board already carries the session→card link. |
| Synthetic data only? | No — real board, real conflicting-claim state. |
| Duplicate of another slice at different scale? | No. |

## Why last

Lowest learning leverage of the three and the most mechanical. Ordered by the Phase 2.5 rule
(highest-uncertainty first): slice 01 tests the feature's central bet, slice 02 tests whether prose
routing works at all, and this slice tests the narrowest claim against the surface most likely to
already cover it.
