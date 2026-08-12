# Slice 01 — Snapshot and resume (WALKING SKELETON)

Feature: session-handoff · Job: `carry-work-across-session-boundaries` · Persona: `kai-session-relay`

## Goal

A session can record the state a fresh session cannot derive, and the next session can read it back
with an honest freshness verdict.

## Learning hypothesis

**Disproves that recording beats reconstructing** — if the next session still needs a re-briefing
after reading the snapshot, then the snapshot is not carrying the load and the feature should pivot
to extending reconstruction (`/nw-continue`) instead.

**Confirms** that the why and the next action are the irreducible payload — if resumption works from
those two plus derived context, the design axis in `feature-delta.md` is correct.

This is the pre-commitment the whole feature rests on, which is why it is slice 01.

## IN scope

- Capture of the **why** (decisions made, approaches ruled out, why work stopped) and the
  **intended next action**.
- A **tree fingerprint** (commit SHA + dirty-state) written at capture.
- A **freshness verdict** at read-back: `current` or `stale`, computed from the fingerprint, stated
  before any resume content is presented.
- **Refusal to capture derivable state** — the *where* (file, step, branch) is derived at read-back,
  never copied into the snapshot.
- **No-op path**: a session that advanced nothing writes no snapshot and says so.
- A **local** snapshot surface. Local is chosen for the WS specifically to keep the forge out of the
  walking skeleton (see WS strategy).

## OUT scope

- Entry-point routing → slice 02.
- Board / card linkage → slice 03.
- Lifecycle hooks (`Stop`, `SessionEnd`, `PreCompact`). The WS is explicitly invoked; automatic
  capture is deferred until the payload is proven worth capturing. See SPIKE below.
- Multi-session arbitration. Detection of a competing snapshot is in; resolving it is not.
- Migrating or subsuming `continue.md` / `todo.md`.

## Acceptance criteria

1. Given a session that made a decision and named a next action, when capture runs, then the
   snapshot contains both, plus a timestamp and a tree fingerprint.
2. Given a snapshot whose fingerprint matches the current tree, when read-back runs, then the
   verdict is `current` and the resume briefing is presented.
3. Given a snapshot whose fingerprint no longer matches, when read-back runs, then the verdict is
   `stale` **with the delta**, and the briefing is **not** presented as current — the anxiety-A
   failure mode is gated here, not documented as a caveat.
4. Given no snapshot exists, when read-back runs, then it falls back to reconstruction and labels
   the briefing as reconstructed rather than recorded.
5. Given a session that advanced nothing, when capture runs, then no snapshot is written and the
   no-op is stated.
6. Given state that an artifact already owns, when capture is offered it, then it is not copied into
   the snapshot.

**Production data, not synthetic** (carpaccio taste test): the acceptance run reads *this* repo's
real state — a real commit SHA, real dirty-state, and the genuinely stale `continue.md` as the
worked example of the failure mode.

## Dogfood moment

Same day: end a real session on this feature with capture, then open a fresh session and resume from
it. If the fresh session asks a question the snapshot should have answered, that is the hypothesis
failing, and it is worth more than a green fixture.

## Dependencies

None. This slice ships the snapshot format that slices 02 and 03 consume.

## Pre-slice SPIKE (conditional)

Only if the design chooses the hook path: **can a hook reliably fire at session end and at
compaction, and does it see enough context to capture the why?** Timeboxed. The WS avoids needing
this answer by being explicitly invoked — that is deliberate, so an unknown about the mechanism
cannot block proving the payload.

## Effort and reference class

≤1 day (≤6h crafter dispatch). Reference class: `edd-loop` slice 01 (walking-skeleton off-ramp) and
`adversarial-review` slice 01 (no-oracle soft review) — both prose skill + thin command, both landed
as single slices.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | **No — 3**: capture entry point, read-back entry point, snapshot format. Adding a hook would make it 4 and force a split; hence the hook is OUT. |
| Depends on a new abstraction? | It *is* the abstraction (snapshot format), shipped first, which is the rule's prescribed shape. |
| Disproves a pre-commitment? | Yes — record-vs-reconstruct, the feature's central bet. |
| Synthetic data only? | No — AC pins real repo state. |
| Duplicate of another slice at different scale? | No. |
