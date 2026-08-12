# Slice 02 — Entry-point routing

Feature: session-handoff · Job: `carry-work-across-session-boundaries` · Persona: `kai-session-relay`
Forge: **absorbs issue #10** (folded in per user decision, 2026-08-12)

## Goal

A session picking up work is routed to the command that owns it, instead of performing the work
inline.

## Learning hypothesis

**Disproves that a written instruction is sufficient** — if the agent still freelances the work after
the card and the snapshot both name the owning command, then routing cannot be requested in prose and
needs a mechanism (a hook, a gate) rather than a line in a document.

**Confirms** that "the how" is a recordable category of lost state — if naming the entry-point stops
the inline freelancing, category 2 of the design axis is validated and the correction the user
currently repeats on every nWave pickup disappears.

## IN scope

Two halves, deliberately in one slice because they are the same claim from two directions:

- **Card-side** — the driving command named where a reader lands. `phil:nwave-issue-board` already
  writes the wave label on the feature issue and already generates a delimited, timestamped block; a
  `Work this with: <command>` line inherits those properties and cannot drift. This is the fix
  originally filed as issue #10.
- **Session-side** — read-back names the entry-point and invokes it, rather than describing the work
  and proceeding to do it.
- **Live wave wins.** Where a recorded entry-point disagrees with the feature's current wave label,
  the live label is preferred and the disagreement is surfaced, never silently resolved.
- **Unknown owner is stated, not defaulted.** No entry-point and no determinable wave means saying so
  and asking — never falling through to inline work.

## OUT scope

- The wave → command mapping being *verified against a run*. The table in `feature-delta.md` is
  assembled from command descriptions and must be checked in DESIGN before it is written into a skill.
- Non-nWave cards. Whether a card with no wave label gets a routing line at all is an open question
  carried from #10; v1 covers the wave-labelled case.
- Enforcement. If prose proves insufficient, the mechanism is a follow-on slice, not this one — that
  is precisely what the hypothesis is testing.

## Acceptance criteria

1. Given a feature issue carrying `wave: <w>`, when the status block is generated, then it names the
   command that owns work in wave `<w>`.
2. Given a snapshot recording an entry-point, when read-back runs, then it names that command and
   invokes it rather than performing the work described.
3. Given a recorded entry-point that disagrees with the current wave label, when read-back runs, then
   the live wave label is used and the disagreement is reported.
4. Given no entry-point and no determinable wave, when read-back runs, then it states that the owner
   is unknown and asks — and does not begin the work.
5. Given `phil:nwave-issue-board`'s one-way rule, when the routing line is written, then nothing is
   read from the issue back into `docs/feature/` — the projection stays one-directional.

**Production data**: exercised against this repo's real board — issue #9 carrying a real
`wave: discuss` label, with a real slice card as the routed target.

## Dogfood moment

Same day: pick up a slice card of *this* feature in a fresh session and observe whether it routes or
freelances. The failure mode is the one the user reported, so the test is authentic rather than
constructed.

## Dependencies

- **Slice 01** for the session-side half — the snapshot carries `entry_point`.
- The **card-side half is independent** and can land first if slice 01 slips. Noted because it is the
  half that removes the user's repeated correction, and it does not need the snapshot to work.

## Effort and reference class

≤1 day (≤6h). Reference class: a rule/line added to an existing skill plus a self-test fixture —
comparable to the `nwave-issue-board` wave-label-swap behavior (fixture 06), which is one rule and one
fixture.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one line in an existing generated block, one routing step in read-back. |
| Depends on a new abstraction? | Consumes slice 01's snapshot format; introduces none. |
| Disproves a pre-commitment? | Yes — that routing can be *requested* in prose rather than enforced. |
| Synthetic data only? | No — real board, real wave label. |
| Duplicate of another slice at different scale? | No. |

## Absorbed issue

Issue #10 was filed standalone on the argument that a one-line fix to a shipped skill should not wait
on this feature's DISCUSS wave. That argument was sound when "the how" was thought to be outside this
job. It is not — the user named it as a fifth category of lost state (D5), which makes it one of this
feature's three independent outcomes and therefore a slice. The counter-argument is preserved in
`feature-delta.md` § Scope Assessment, and the card-side/session-side dependency split above is what
keeps the original speed argument alive: the card-side half can still ship first.
