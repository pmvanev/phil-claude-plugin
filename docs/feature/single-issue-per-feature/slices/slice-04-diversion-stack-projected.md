# Slice 04 — The diversion stack, projected

**Goal:** Record the work stack and the why in `.session-handoff.md`, and project both into the issue
as a generated, timestamped block a teammate can read.

**Stories:** S2 (inherit a colleague's feature), S3 (put it down, pick it up), S4 (record a diversion)
**Carries:** the ADR-013 amendment.

## Learning hypothesis

**Disproves** [D7]'s local-authoritative surface if a teammate reading only the projection cannot
actually resume — in which case the authority has to move to the forge, and the one-way rule takes the
inversion this design was arranged to avoid.
**Confirms**, if it holds, that ADR-013's deferred partition was the right call and needed only
triggering.

## IN scope

- **The stack in `.session-handoff.md`**: frames innermost-first, each with what it is, why it was
  pushed, and when. Push and pop are local operations.
- **`/phil:handoff` refreshes the projection** after writing the local snapshot — local first, always,
  so a failed forge call never costs the authority.
- **The projected block** carries the stack, the why, and the intended next action, each with its
  capture timestamp, inside the same delimiters slice 01 established.
- **`/phil:resume` is unchanged**: it reads the local file. The projection is never read back, which is
  what keeps [D7] legal.
- **ADR amendment**: `adr-013-session-handoff-snapshot-surface.md` gains an amendment section adopting
  its own *partitioned local + board* alternative. Amended, not superseded — the git-ignored local
  surface is still the decision; what changes is that the deferred second half now ships.
- **The `jobs.yaml` facet** on `carry-work-across-session-boundaries`: anxiety C becomes a stated trade
  rather than a force avoided, quoting the original.

## OUT scope

- **Arbitration between two live claims.** Detected, not resolved — inherited verbatim from
  `session-handoff` v1. More likely now, and still out.
- A `Stop` hook. Still behind the payload-visibility SPIKE that ADR-014 deferred it behind.
- Per-push forge writes. Forbidden by *Refresh at boundaries*, and the reason comments were not chosen
  as the stack's authority.
- Retiring `.session-handoff.md`.

## Acceptance criteria

1. Local write precedes the projection refresh; a forge failure leaves the snapshot intact and says so.
2. **Absent renders as `unknown`.** Where no snapshot was projected, the stack section says `unknown`
   — never renders empty, which a reader would take as "no diversions". This is the slice's sharpest
   assertion and needs its own fixture.
3. A frame open longer than one boundary is marked, so a never-popped push is visible rather than
   quietly stale.
4. `/phil:resume` reads no forge content. A fixture asserts the projection is write-only.
5. A human edit inside the markers is replaced and the replacement noted, per the shipped 04/11 rule.
6. A session that advanced nothing writes no snapshot and refreshes nothing.
7. The ADR amendment quotes ADR-013's own deferral line rather than paraphrasing it.

## The accepted cost, stated plainly

A teammate sees only what the last `/phil:handoff` projected. If Morgan never ran it, there is no
projection — and the honest rendering is `unknown`, not a clean-looking empty stack. This is the same
shape as a declined grooming candidate returning next run: a real cost of having exactly one authority,
and the report should say so rather than let it read as the tool forgetting.

## Dependencies

Slice 01's delimiters exist. Slice 03's column state is independent — this slice can follow 02.

## Effort

~1 day. The local stack format and the projection are small; the fixtures are most of the work, and
AC2 and AC4 are the two that must not be waved through.

Reference class: `session-handoff` slices 01-03, which shipped the snapshot, the routing line, and the
claimed-card link at roughly this size each.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a stack format in an existing file, a refresh step in an existing command, an ADR amendment, a `jobs.yaml` facet. |
| Depends on a new abstraction? | No. Reuses slice 01's delimiters and ADR-013's existing snapshot surface, which is the whole point of [D7]. |
| Disproves a pre-commitment? | Yes — [D7]'s local-authoritative surface. If a teammate cannot resume from the projection alone, the authority has to move to the forge. |
| Synthetic data only? | No. The stack is exercised on real work in this repo, and the teammate read is the real test. |
| Duplicate of another slice at scale? | No. 01 projects *position*; this projects the *why*, which no artifact holds. Different sources, different failure modes. |
