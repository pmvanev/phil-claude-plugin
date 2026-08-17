# Slice 03 — Claimed-card link

> **NOT BUILT 2026-08-13 — hypothesis confirmed, slice closed by evidence.** This supersedes the
> `DEFERRED 2026-08-12` note. The learning hypothesis — *the board already carries enough* — was
> tested and held, so the slice did its job by not shipping. Card #12 closed; the one residual gap the
> investigation found is carded separately. Findings in *Verdict* below.
>
> The 2026-08-12 deferral read "pending evidence, not cancelled." That framing turned out to be the
> flaw: **the evidence it waited for cannot arrive.** `.session-handoff.md` is git-ignored, so no
> history of past snapshots exists and no retrospective run can answer whether a resume ever failed
> for want of a claimed card. A deferral pending evidence needs to name the run that would produce it,
> or it defers forever while looking patient.
>
> Everything below this note is the original brief, kept as written. Read it as the proposal that was
> tested, not as an agenda.

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

---

## Verdict — 2026-08-13

**Hypothesis confirmed. The board plus this repo's ranking convention already carry enough, and the
snapshot's prose carries the rest.** Four findings.

**1. `In Progress` is not used in this workflow.** The slice is built around a session claiming a card
and the board recording it as In Progress. On 2026-08-13 no card was In Progress; #15 and #5 went to
Done and #23 to Todo without passing through it. The one observed instance the original brief cites
(#3 and #9) had already been diagnosed as hygiene — #3 was left there. **A slice whose central state
transition the workflow does not perform has no population.**

**2. The board answers *what is next* deterministically.** `CLAUDE.md` fixes the convention: the top
Todo card in board-position order is what to work on next, and `phil:rank-issues` maintains that
order. Verified live: this session selected #15 from board position without reading the snapshot at
all, and it was correct.

**3. The claim's basis is already recorded, in prose.** The live snapshot's `Why` carried five bullets
of reasoning and ruled-out alternatives; `Next` and `owner` carried the work identity. A structured
`claimed_card:` field would duplicate that, against **KPI-5** — facts duplicated between the snapshot
and an artifact that owns them, target 0. The category-4 row of the design axis says the board owns
this "partially"; what it does not own turned out to be what `Why` was already for.

**4. The competing-claim case cannot arise in this setup.** Fixture 10 needs two snapshots naming one
card. There is one snapshot per repository root and `git worktree list` shows a single worktree. The
two other snapshots on this machine are in *different repositories*, which this brief scopes OUT under
*multi-repo or cross-forge claims*.

### The residual, which is real and much narrower

Findings 2 and 3 hold only while the board's top Todo **is** the in-flight card. On 2026-08-13 they
diverged: the snapshot's `Next` named a dogfood run while the board's top Todo was #15. It was
harmless — the dogfood had happened in an intervening session — but **nothing detected the
divergence**, and `RESUME-STALE` would not have: it compares the snapshot against the *tree* and never
against the *board*.

That gap is not "record which card was claimed." It is "notice when the two records of what is in
flight disagree." Carded separately.

**Carded as #24 and shipped 2026-08-17** as the board divergence check in `SKILL.md` — outcomes
`BOARD-AGREES` · `BOARD-DIVERGES` · `BOARD-UNREADABLE`, pinned by fixtures `13`–`15`. It detects and
never resolves, and records nothing, so it does not reopen this slice: no claimed card is stored, no
board state is written, and the comparison is made fresh at read-back from sources that already own
their answers. **Finding 1 above was falsified in passing** — `In Progress` *is* used in this workflow
as of 2026-08-17, so the check reads it where present and falls back to the top Todo card otherwise.
That is a widening of #24's literal done-when, which named only the top Todo and would have reported
a false divergence against a correctly-claimed card.

### What happens to the fixtures

`self-test/09-claim-and-basis/` and `10-competing-claim/` pin a slice that was tested and deliberately
not built. They stay, marked as such — a fixture for unbuilt work is a standing claim about what the
skill would have to do, and deleting it would erase the reasoning along with the test.
