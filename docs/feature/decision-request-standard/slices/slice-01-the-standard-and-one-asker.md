# Slice 01 — The standard, one asker, one countable fixture (walking skeleton)

**Goal:** Write the standard as a shared fragment, reference it from one real ask site, and prove the
200-word ceiling is countable on a real request.

**Stories:** S1 (answer without spending a turn on what it means) · S2 (get the detail without the wall)
**WS strategy:** C — real local resources (the real `groom-issues` skill, this repo's real board)

## Learning hypothesis

**Disproves [D8] — the shape** — if a referenced fragment does not change how the question actually comes
out. The fragment is read at authoring time, not at ask time; if the ask that ships still opens with a
bare option list, then the standard needs to be closer to the call site than a reference can put it, and
slices 02–04 are all built on a shape that does not work.

**Confirms**, if it passes, that one fragment plus a reference is enough to change output — which is the
premise every later slice inherits, and the premise E6 puts in doubt (`spirit-walk` wrote the rule locally
and it propagated nowhere).

**Second, smaller hypothesis:** that the hardest asker is survivable. `groom-ask` is the repo's only
*elicitation* ask — it asks what an issue is *for* — so it is the worst input a 200-word ceiling will ever
get. If [D4] breaks anywhere it breaks here, and here is where it is cheapest to find out.

## IN scope

- `skills/shared/decision-request.md` — the standard: C1–C8 from the feature delta, with the ask/detail
  split ([D5]) and the placement clause ([D9]).
- A reference to it by name from `skills/groom-issues/SKILL.md` at its ask site, following the
  `test-runner-detection.md` referencing pattern exactly.
- One fixture asserting the word count of a **real** request produced by that site — not a synthetic one.
- A dogfood run against this repo's board, with the version named or the hand-driven path stated, per
  `CLAUDE.md`'s *Which copy is under test*.

## OUT of scope

- The other 7 ask sites and the other 12 command grants — slice 03.
- The bare-list, jargon-wall and buried-ask fixtures — slice 02. This slice pins **only** the count,
  because the count is the one thing that must work before the rest is worth building.
- Any check script. Conformance is checked by eye here; mechanising it is [D10] and slice 03.
- The conversational half — slice 04, and [D11] already declares it out of reach.
- `plugin-dev` consultation is **not** out of scope: the build path requires
  `plugin-dev:skill-development` before the fragment is written, and the commit must say it ran.

## Acceptance criteria

- **AC1** `skills/shared/decision-request.md` exists and states C1–C8, including that the ceiling applies
  to the ask alone and that a buried conforming ask still fails.
- **AC2** `skills/groom-issues/SKILL.md` references it by name at its ask site.
- **AC3** A real ask from that site is ≤200 words, counted mechanically, and the count is recorded in this
  brief's Result section as a number.
- **AC4** That ask states what is being decided and what turns on it before its first option, and contains
  no wave label, issue number, slice id, skill name or artifact path.
- **AC5** The same ask carries a separated detail section that does carry those tokens — proving [D5] is a
  real clause and not an escape hatch nobody uses.
- **AC6** Each option in that ask names its own cost, not only its benefit.
- **AC7** `plugin-dev:skill-development` was consulted before the fragment was written, and the commit
  says so. Per `CLAUDE.md`, a sibling file is not a template.

## Dependencies

None blocking. The groom family is complete and installed.

## Effort · reference class

**≤1 day.** Reference class: `board-setup-block` slice 01 (one script + one skill + one command, one day)
and `live-work-stack` slice 01. This slice is smaller than both — one fragment, one reference, one
fixture, no new command and no new grant.

## Pre-slice SPIKE

**Not needed.** The uncertainty is whether a reference changes output, and that is answered by doing the
slice rather than by probing first — the slice *is* the probe, which is what makes it the skeleton.
