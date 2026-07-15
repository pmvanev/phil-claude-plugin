# Slice 01 — Triage & Off-ramp (walking skeleton)

**Goal (one sentence):** `/phil:edd "<intent>"` captures the intent as discrete expectations,
classifies each, and when they're all engine-checkable, recommends the right engine and exits —
adding zero ceremony.

**WS strategy:** A — thinnest end-to-end slice, run against a real repo. This is the honest
"get out of the way" spine; it is shippable value on its own (it prevents ceremony).

## IN scope
- `/phil:edd "<intent>"` command + skill loader (command→skill split, per plugin convention).
- CAPTURE: restate intent as an itemized expectations list; confirm/edit with the developer.
- CLASSIFY: per-expectation `engine-checkable` vs `qualitative`, biased to engine-checkable.
- OFF-RAMP: when ALL expectations are engine-checkable, emit the classification table + a
  specific engine recommendation (`/nw-...` or `/phil:work "<...>"`) and EXIT with no trail.
- A self-test fixture proving a fully-checkable intent off-ramps and writes zero trail files.

## OUT of scope
- The qualitative-evidence gate (slice 02).
- Delegating an actual build to an engine (slice 02).
- Cross-domain multi-initiative sequencing + seam-level expectations (slice 03, deferred).
- Physically extracting the gate into a shared skill (DESIGN decision).

## Learning hypothesis
- **Disproves** "phil:edd can't tell when it should get out of the way" if the classifier
  wraps a fully-checkable intent in a gate, or mis-recommends the engine.
- **Confirms** the central off-ramp is real and the anti-ceremony value lands, if a
  fully-checkable intent exits cleanly with an accurate engine recommendation and no trail.

## Acceptance criteria
- Given an intent whose expectations are all engine-checkable, when I run `/phil:edd`, then it
  emits a classification table (each row: expectation → engine + native oracle), recommends the
  specific engine command, and exits **without** creating any `docs/edd/<slug>/` trail.
- Given classification is ambiguous for an expectation, then it defaults to engine-checkable and
  asks me to confirm before marking anything qualitative.
- Given a would-be qualitative expectation with no stated concrete reason it resists cheap
  assertion, then it is treated as engine-checkable (no unjustified ceremony).

## Dependencies
nwave present; phil:work present (as off-ramp targets). No engine internals modified.

## Effort estimate
≤1 day (≤6h crafter dispatch). Reference class: `phil-work` slice-01 walking skeleton.

## Production data
Exercised against a real intent on this repo (e.g. a genuine refactor/feature ask), not synthetic.

## Dogfood moment
Run `/phil:edd` on a real, fully-checkable intent the same day and confirm it off-ramps.
