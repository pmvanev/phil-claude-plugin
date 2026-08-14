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

## Result — 2026-08-14

**Authored; not yet exercised.** The stack format, the projection step, the ADR amendment and two fixtures
landed. No run has produced a projection, so ACs 1-6 are unverified and **KPI-1b is not measured.**

### What landed

1. **The stack in the snapshot** — a new recordable category alongside the why and the next action, and it
   earned its own row rather than folding into the why: the why is reasoning, the stack has a **shape**
   (what to return to, and in what order). Frames are innermost-last, numbered, each carrying what it is,
   why it was pushed, and when. **A frame is popped by deleting its line**, so the file is the stack rather
   than a log of stack operations — which is what keeps it from growing without bound.
2. **The projection step in CAPTURE**, ordered local-write-first, plus `PROJECTED` /
   `PROJECTION-UNREFRESHED` as additional outcomes. A `CAPTURE` carrying neither, on work that has a card,
   is a run that skipped the card silently — and nothing else would reveal it, because the snapshot is
   written either way.
3. **`nwave-issue-board` gained *Project the reasoning, not just the position*** — the publisher's half.
   Everything the block carried until now says *where*; this says *why it stopped there*.
4. **ADR-013 amended, not superseded**, quoting its own deferral line and its own consequence line as the
   trigger. AC7 met.
5. **Fixtures 11 and 12.**

### The bug I introduced and caught in the same pass

I numbered the stack collection **6b** — after step 6, which writes the file. **A stack collected after the
write is a stack the snapshot does not contain.** Moved to 3c, with the other payload collection, and the
step now says why it lives there. Worth recording because the ordering read as plausible: 6b sat directly
above the projection step, which is where the stack is *used*, and the write between them was invisible.
**Appending a step next to where its output is consumed rather than where its input is gathered is how this
class of bug looks from inside.**

### Dogfooded 2026-08-14 — the first live run, at 0.47.0

`/phil:handoff` ran through the command (not by hand) after the merge and push closed the skew. Reported
`CAPTURE` · `PROJECTED` · `REFUSE-DERIVABLE`. **KPI-1b MET**: the owner named the wave, the current slice,
why work stopped, and what is next, in under 30 s.

`owner:` was omitted because #26 carries no `wave:` label — step 3b's rule firing live, and slice 01's
finding 1 in action: this repo's build path has no row in the routing table.

**Three things the run exercised, and three it did not.**

| Exercised | Not exercised |
|---|---|
| Local write before the forge call | The forge **failure** path — `PROJECTION-UNREFRESHED` (fixture 11) never fired, because the forge was reachable |
| Whole-block markers surviving a refresh with human prose above them | The **stack rendering** — no diversion was open, so there was nothing to render |
| `Stack — none` as distinct from `unknown` | `unknown` itself (fixture 12) — a snapshot existed |

**The stack was empty, and that is the honest result.** The session ended at a slice boundary rather than
inside a detour, so the first ever run of the stack feature had no stack to record — it exercised the
*omit-rather-than-render-empty* rule instead of the rendering. Worth stating plainly: **the feature's
headline mechanism is still unexercised**, and the run that was supposed to prove it proved its degenerate
case instead.

### The defect the run exposed — fold-back, route 1

The reasoning went **inside** the `nwave:status` markers, appended, with the position content preserved by
hand. It worked, and it worked for the wrong reason: **the region had two writers and only care kept them
from colliding.** A later position-only refresh, done properly from its own single source, would have
silently deleted the why, the next action and the stack — the only record of reasoning no artifact holds,
erased by a routine boundary refresh reporting success.

Fixed in `nwave-issue-board`: **one writer owns the whole block and regenerates it entire from two sources**
(`nwave-slice-status` for position, `.session-handoff.md` for reasoning), on every refresh, even when only
one source changed. A missing source renders `unknown`, which is what makes whole-block regeneration
incapable of destroying anything. Fixture `19` pins it, including the tempting optimisation and the
inverted-one-way-rule variant that copies the old reasoning back out of the rendered block.

### Not done
- **`plugin-dev:command-development` could not be consulted.** It fails to load: its frontmatter injects
  `bash .../scripts/test.sh`, which is absent from the installed copy. That is issue #23 reproducing, with
  a detail worth adding to it — `skill-development` loads fine, so the fault is specific to this skill's
  script reference. `commands/handoff.md` was edited on `skill-development`'s guidance instead, and the
  deviation is recorded here rather than left invisible.
- **`skill-reviewer` has not run** over `session-handoff` or the publisher's new section.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a stack format in an existing file, a refresh step in an existing command, an ADR amendment, a `jobs.yaml` facet. |
| Depends on a new abstraction? | No. Reuses slice 01's delimiters and ADR-013's existing snapshot surface, which is the whole point of [D7]. |
| Disproves a pre-commitment? | Yes — [D7]'s local-authoritative surface. If a teammate cannot resume from the projection alone, the authority has to move to the forge. |
| Synthetic data only? | No. The stack is exercised on real work in this repo, and the teammate read is the real test. |
| Duplicate of another slice at scale? | No. 01 projects *position*; this projects the *why*, which no artifact holds. Different sources, different failure modes. |
